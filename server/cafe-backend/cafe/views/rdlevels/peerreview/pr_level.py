from django import forms
from django.shortcuts import get_object_or_404
from django_bridge.response import Response
from django.contrib import messages

from cafe.models import RDLevel
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required
from allauth.socialaccount.models import SocialAccount

class PeerReviewLevelPayload(forms.Form):
    approval_intent = forms.IntegerField()
    public_comment = forms.CharField(required=False)
    private_comment = forms.CharField(required=False)

@permission_required('cafe.peerreview_rdlevel')
def pr_rdlevel(request: HttpRequest, level_id: str):
    if request.method == 'POST':
        form = PeerReviewLevelPayload(request.POST)
        if form.is_valid():
            rdlevel = get_object_or_404(RDLevel, id=level_id)
            rdlevel.approval = form.cleaned_data.get("approval_intent")
            rdlevel.approval_notes_public = form.cleaned_data.get("public_comment")
            rdlevel.approval_notes_private = form.cleaned_data.get("private_comment")
            rdlevel.save()
            messages.add_message(request, messages.SUCCESS, "Peer review submitted successfully.")

    rdlevel = get_object_or_404(RDLevel, id=level_id)
    submitter = rdlevel.submitter

    # other levels?
    other_levels = RDLevel.objects.filter(submitter=submitter).exclude(id=rdlevel.id)
    is_first_level = not other_levels.exists()

    # also resolve their discord id if possible
    social_account = SocialAccount.objects.filter(user=submitter, provider='discord').first()

    # we want the oldest level first
    pr_levels = RDLevel.objects.filter(approval=0).order_by('last_updated')
    props = {
        "levels": [level.to_dict() for level in pr_levels],
        "rdlevel": rdlevel.to_dict(),
        "is_first_level": is_first_level,
        "discord_id": social_account.uid if social_account else None,
    }

    return Response(request, request.resolver_match.view_name, props)