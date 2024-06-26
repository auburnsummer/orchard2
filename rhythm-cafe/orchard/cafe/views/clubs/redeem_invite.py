from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.db import transaction

from cafe.models import ClubInvite, ClubMembership

class RedeemInviteView(View):
    @method_decorator(login_required)
    def get(self, request, code):
        invite = ClubInvite.objects.filter(code=code).first()
        print(invite)
        if invite.has_expired():
            invite = None

        context = {
            "invite": invite,
            "code": code
        }
        
        return render(request, "cafe/clubs/redeem_invite.jinja", context)
    
    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, code):
        invite = get_object_or_404(ClubInvite, code=code)

        if invite.has_expired():
            return HttpResponseForbidden("Invite has expired")

        # if they're already in the club, it just sets their role in that club.
        existing_membership = ClubMembership.objects.filter(
            user=request.user,
            club=invite.club
        ).first()
        if existing_membership is not None:
            existing_membership.role = invite.role
            existing_membership.save()
        else:
            new_membership = ClubMembership(
                user=request.user,
                club=invite.club,
                role=invite.role
            )
            new_membership.save()

        invite.delete()

        return HttpResponseRedirect(reverse('cafe:club_settings_members', args=[invite.club.id]))
    
redeem_invite = RedeemInviteView.as_view()