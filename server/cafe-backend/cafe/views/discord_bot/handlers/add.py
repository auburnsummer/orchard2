import textwrap

from django.http import JsonResponse
from vitals.vitals import PREFILL_VERSION

from cafe.models.add_session import AddSession, AddSessionPhase
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.rdlevels.tempuser import get_or_create_discord_user
from cafe.tasks.run_prefill import run_prefill_v2

from .utils import Flags, ResponseType, action_row, button, ephemeral_response, get_club_from_guild_id, label, option, seperator, string_select, text, text_input

from orchard.settings import DOMAIN_URL
from django.urls import reverse
from cafe.signing import addlevel_signer

NO_GROUP_RESPONSE = ephemeral_response("No group found for this server (the server owner needs to use the `/connectgroup` command)")
NO_ATTACHMENTS_RESPONSE = ephemeral_response("The post doesn't have any attachments ending with .rdzip!")

def get_attachments_from_message(data):
    target_id = data['data']['target_id']
    message = data['data']['resolved']['messages'][target_id]
    attachments = [a for a in message['attachments'] if a['filename'].endswith('.rdzip')]
    return attachments

def phase_select_attachment(session: AddSession):
    """
    Phase 1: if the message has multiple attachments, we need to ask the user which one they're operating on.
    If the message only has one attachment, this phase renders nothing.
    """
    attachments = session.attachments
    if not attachments:
        return [
            text("No attachments found in the message. If you see this, it's a bug.")
        ]
    if len(attachments) == 1:
        return []
    return [
        text("This post has multiple attachments. Which one do you want to add?"),
        action_row(
            string_select(
                "p1_select_attachment",
                [option(a['filename'], a['id'], a['url'] == session.selected_attachment_url) for a in attachments],
                placeholder="Select attachment..."
            )
        )
    ]

def phase_select_type(session: AddSession):
    """
    Phase TWO: the user is asked if this is a new level or an update to an existing level.
    """
    if session.phase < AddSessionPhase.SELECTING_TYPE:
        return []
    base = [
        seperator(),
        text("Is this a new level, or an update to an existing level?"),
        action_row(
            string_select(
                "p2_type_select",
                [
                    option("New level", "new", session.add_type == "new"),
                    option("Update to existing level", "update", session.add_type == "update")
                ]
            )
        )
    ]
    if session.add_type == "new":
        # a checkbox if they want to edit the metadata first
        base.extend([
            seperator(),
            action_row(
                button("p2_new_submit", "Add level", 1),
                button("p2_new_submit_edit", "Edit level metadata before adding", 2)
            )
        ])
    if session.add_type == "update":
        # just a button to submit
        base.extend([
            seperator(),
        ])
        if session.phase == AddSessionPhase.ERROR_LEVEL_NOT_FOUND:
            base.extend([
                text("**The level ID you entered does not exist.**")
            ])
        if session.phase == AddSessionPhase.ERROR_NO_PERMISSION:
            base.extend([
                text("**You don't have permission to edit that level.**")
            ])
        base.extend([
            action_row(
                button("p2_update_submit", "Click here to continue", 1)
            )
        ])

    return base

def phase_report_results(session: AddSession):
    """
    Phase FOUR: report results
    """
    prefill = session.prefill
    if not prefill:
        # this should never happen, we should always have a prefill in phase 4.
        return [text("No prefill found in phase 4. If you see this, it's a bug.")]

    # did we make a level from it? (i.e. prepost was skipped)
    if prefill.level:
        link = DOMAIN_URL + reverse('cafe:level_view', args=[prefill.level.id])
        return [
            text(f"Level uploaded successfully! [Link here]({link})")
        ]

    # check if level already exists.
    existing_level = RDLevel.objects.filter(sha1=prefill.data['sha1']).first()
    if existing_level:
        link = DOMAIN_URL + reverse('cafe:level_view', args=[existing_level.id])
        lines = [
            text(f"This level has already been uploaded: [Link here]({link})")
        ]
        return lines
    
    # otherwise, send them a link to the prefill to finish the submission.
    prefill_url = DOMAIN_URL + reverse('cafe:level_from_prefill', args=[prefill.id])

    return [
        text(f"Please click the link to finish the submission: [Link here]({prefill_url})")
    ]

def render_add_session_components(add_session):
    if add_session.phase == AddSessionPhase.UPLOADING:
        return [text("## Uploading level, please wait... ##")]
    if add_session.phase == AddSessionPhase.COMPLETE:
        return phase_report_results(add_session)
    if add_session.phase == AddSessionPhase.ERROR_DUPLICATE:
        link_to_duplicate = DOMAIN_URL + reverse('cafe:level_view', args=[add_session.prefill.level.id])
        return [
            text(f"A level with the same file already exists in the database. The update was not applied. [Link to duplicate]({link_to_duplicate})")
        ]
    # SELECTING_ATTACHMENT, SELECTING_TYPE, and the update error states (ERROR_LEVEL_NOT_FOUND, ERROR_NO_PERMISSION)
    # all render the step-by-step form, with phase_select_type injecting inline error messages where appropriate.
    components = []
    components.extend(phase_select_attachment(add_session))
    components.extend(phase_select_type(add_session))
    return components

def render_add_session(add_session):
    return {
        # type is either 4 (send initial message) or 7 (update original message) depending on whether this is an initial response or a followup response.
        # the caller of this function is responsible for setting the correct type.
        "data": {
            "flags": Flags.IS_COMPONENTS_V2.value | Flags.EPHEMERAL.value,
            "components": render_add_session_components(add_session)
        }
    }

def add_v2(data, check_user_is_poster=True):
    club = get_club_from_guild_id(data['guild']['id'])

    if not club:
        return NO_GROUP_RESPONSE

    attachments = get_attachments_from_message(data)
    if not attachments:
        return NO_ATTACHMENTS_RESPONSE

    target_id = data['data']['target_id']
    club = get_club_from_guild_id(data['guild']['id'])
    message = data['data']['resolved']['messages'][target_id]

    is_webhook = 'webhook_id' in message
    invoker_id = data['member']['user']['id']
    # nb: poster_id is the discord user id of the user who will be credited as the submitter of the level.
    # poster_id is normally the user who posted the message,
    # but if the message was posted by a webhook, then the poster_id is the user who ran the command.
    # message['author']['id'] and invoker_id are not always the same,
    # such as in the delegated scenario where someone else is running the command on behalf of the poster.
    poster_id = message['author']['id'] if not is_webhook else invoker_id

    if check_user_is_poster:
        if is_webhook:
            return ephemeral_response("You can't add levels from webhooks.")
        if invoker_id != poster_id:
            return ephemeral_response("You can only add levels from your own messages.")
        
    user = get_or_create_discord_user(poster_id, message['author'].get('global_name') or message['author']['username'])
    
    # if there are multiple attachments, we need to ask the user which one they want to add, which means we are on phase 1
    # if there is only one attachment, we can skip straight to phase 2, which asks the user if this is a new level or an update to an existing level.
    phase = AddSessionPhase.SELECTING_ATTACHMENT if len(attachments) > 1 else AddSessionPhase.SELECTING_TYPE

    # create an AddSession to keep track of the user's progress in the add flow
    session = AddSession.objects.create(
        id = data['id'],
        user = user,
        interaction_token = data['token'],
        phase = phase,
        attachments = attachments
    )
    # if we are on phase SELECTING_TYPE, set selected_attachment_url straight away
    if phase == AddSessionPhase.SELECTING_TYPE:
        session.selected_attachment_url = attachments[0]['url']
        session.save()

    return JsonResponse({
        "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
        **render_add_session(session)
    })

def update_modal():
    url_to_mylevels = DOMAIN_URL + reverse("cafe:profile_levels")
    return {
        "type": ResponseType.MODAL.value,
        "data": {
            "custom_id": "update_modal",
            "title": "Update level",
            "components": [
                text(textwrap.dedent(f"""
                    Enter the ID of the level you want to update.
                                     
                    Click [here]({url_to_mylevels}) to go to your levels and find the ID of the level you want to update.
                    
                    Click on the name of the level to go to the level page, then the ID is displayed on the right side of the page.                                   
                """)),
                label(
                    "ID of the level to update",
                    text_input("update_level_id", style=1, placeholder="Enter level ID here...")
                )
            ]
        }
    }

def add_step(data):
    session = AddSession.objects.get(id=data['message']['interaction']['id'])

    if data['data']['custom_id'] == "p1_select_attachment":
        # the user has selected which attachment they want to add, so we save that in the session and move on to phase 2.
        selected_id = data['data']['values'][0]
        selected_attachment = next(a for a in session.attachments if a['id'] == selected_id)
        session.selected_attachment_url = selected_attachment['url']
        session.phase = AddSessionPhase.SELECTING_TYPE
        session.save()

    if data['data']['custom_id'] == "p2_type_select":
        session.add_type = data['data']['values'][0]
        session.phase = AddSessionPhase.SELECTING_TYPE  # if there was an error state, clear it when they change the type
        session.save()

    if data['data']['custom_id'] == "p2_update_submit":
        # for this specific case we now open a modal where they enter the id of the level they want to update
        return JsonResponse(update_modal())
    
    # they clicked the button
    if data['data']['custom_id'] in ["p2_new_submit", "p2_new_submit_edit"]:
        session.phase = AddSessionPhase.UPLOADING
        session.save()
        user = session.user
        club = get_club_from_guild_id(data['guild']['id'])
        go_to_prepost = data['data']['custom_id'] == "p2_new_submit_edit"
        # make a prefill object
        prefill = RDLevelPrefillResult.objects.create(
            url=session.selected_attachment_url,
            version=PREFILL_VERSION,
            user=user,
            prefill_type=session.add_type,
            club=club,
            go_to_prepost=go_to_prepost
        )
        run_prefill_v2(prefill.id, session.id)

    if data['data']['custom_id'] == "update_modal":
        # they submitted the modal to update.
        level_id = data['data']['components'][1]['component']['value']
        level = RDLevel.objects.filter(id=level_id).first()
        user = session.user
        club = get_club_from_guild_id(data['guild']['id'])
        ok_to_proceed = True
        if not level:
            session.phase = AddSessionPhase.ERROR_LEVEL_NOT_FOUND
            session.save()
            ok_to_proceed = False
        elif not user.has_perm('cafe.change_rdlevel', level):
            session.phase = AddSessionPhase.ERROR_NO_PERMISSION
            session.save()
            ok_to_proceed = False
        if ok_to_proceed:
            session.phase = AddSessionPhase.UPLOADING
            session.save()
            prefill = RDLevelPrefillResult.objects.create(
                url=session.selected_attachment_url,
                version=PREFILL_VERSION,
                user=user,
                prefill_type="update",
                level=level,
                club=club,
                go_to_prepost=False
            )
            run_prefill_v2(prefill.id, session.id)
        

    return JsonResponse({
        "type": ResponseType.UPDATE_ORIGINAL_MESSAGE.value,
        **render_add_session(session)
    })

def _add(data, check_user_is_poster):
    "Legacy entry point. TODO remove this"
    club = get_club_from_guild_id(data['guild']['id'])
    
    if not club:
        return NO_GROUP_RESPONSE

    target_id = data['data']['target_id']
    message = data['data']['resolved']['messages'][target_id]
    attachments = [a for a in message['attachments'] if a['filename'].endswith('.rdzip')]
    if not attachments:
        return NO_ATTACHMENTS_RESPONSE
    
    is_webhook = 'webhook_id' in message
    invoker_id = data['member']['user']['id']
    # nb: poster_id is the discord user id of the user who will be credited as the submitter of the level.
    # poster_id is normally the user who posted the message,
    # but if the message was posted by a webhook, then the poster_id is the user who ran the command.
    # message['author']['id'] and invoker_id are not always the same,
    # such as in the delegated scenario where someone else is running the command on behalf of the poster.
    poster_id = message['author']['id'] if not is_webhook else invoker_id

    if check_user_is_poster:
        if is_webhook:
            return ephemeral_response("You can't add levels from webhooks.")
        if invoker_id != poster_id:
            return ephemeral_response("You can only add levels from your own messages.")

    lines = []
    for attachment in attachments:
        payload = {
            "level_url": attachment['url'],
            # nb: this is the discord user id of the user who posted the message,
            # which may not be the same as the user who is running this command.
            "discord_user_id": poster_id,
            # hint for name in case we need to create an account for the submitter
            # this only can occur in the delegated scenario
            # nb: we don't need to check for the webhook scenario here, because
            # if it is a webhook scenario, then the poster_id is the user who ran the command,
            # who will always have an account by the time they reach the level submission portal, since
            # the level submission portal is only accessible to users who have an account.
            "discord_user_name_hint": message['author'].get('global_name') or message['author']['username'],
            "club_id": club.id
        }
        secret = addlevel_signer.sign_object(payload)
        url = DOMAIN_URL + reverse("cafe:level_portal", args=[secret])
        line = f"`{attachment['filename']}`: [click here]({url})"
        lines.append(line)

    content = "\n".join(f"- {line}" for line in lines)
    
    return ephemeral_response(content)

def add(data):
    return add_v2(data, check_user_is_poster=True)

def add_delegated(data):
    return add_v2(data, check_user_is_poster=False)