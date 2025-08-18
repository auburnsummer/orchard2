from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.db import transaction
from django.contrib import messages

from cafe.models import ClubMembership
from cafe.models.clubs.club_invite import ClubInvite
from django_bridge.response import Response


class RedeemInviteView(View):
    @method_decorator(login_required)
    def get(self, request, code):
        invite = ClubInvite.objects.filter(code=code).first()
        
        if invite is not None and invite.has_expired():
            invite = None

        if invite:
            membership = ClubMembership.objects.filter(
                user=request.user,
                club=invite.club
            ).first()
        else:
            membership = None

        context = {
            "invite": invite.to_dict() if invite else None,
            "code": code,
            "membership": membership.to_dict() if membership else None
        }

        return Response(request, request.resolver_match.view_name, context)
    
    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, code):
        invite = get_object_or_404(ClubInvite, code=code)

        if invite.has_expired():
            return HttpResponseForbidden("Invite has expired")

        # Check if user is already in the club
        existing_membership = ClubMembership.objects.filter(
            user=request.user,
            club=invite.club
        ).first()
        
        created = False
        upgraded_to_owner = False
        if existing_membership is not None:
            # User is already in the club
            if existing_membership.role != "owner":
                # Only update role if they're not already an owner
                existing_membership.role = invite.role
                existing_membership.save()
                # Check if they were upgraded to owner
                if invite.role == "owner":
                    upgraded_to_owner = True
        else:
            # User is not in the club, create new membership
            new_membership = ClubMembership.objects.create(
                user=request.user,
                club=invite.club,
                role=invite.role
            )
            created = True
            
        if created or upgraded_to_owner:
            invite.delete()
            if created:
                messages.success(request, f"You have successfully joined the group {invite.club.name}!")
            elif upgraded_to_owner:
                messages.success(request, f"You have been promoted to owner of {invite.club.name}!")

        return HttpResponseRedirect(reverse('cafe:club_settings_members', args=[invite.club.id]))
    
redeem_invite = RedeemInviteView.as_view()