from django.contrib import messages

from django import forms
from django.http import JsonResponse
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required

from cafe.bridge.response import Response

from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.user import User

class PharmacyBulkTransferForm(forms.Form):
    level_ids = forms.CharField()
    user_id = forms.CharField()

@permission_required('cafe.peerreview_rdlevel')
def pharmacy_bulk_transfer(request: HttpRequest) -> JsonResponse:
    """
    Transfer levels from one submitter to another.
    """
    if request.method == "POST":
        form = PharmacyBulkTransferForm(request.POST)
        if form.is_valid():
            level_ids = form.cleaned_data.get("level_ids", "").splitlines()
            user_id = form.cleaned_data.get("user_id")

            try:
                new_submitter = User.objects.get(id=user_id)
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
            else:
                levels = RDLevel.objects.filter(id__in=level_ids)
                # we need to call save() to trigger typesense
                for level in levels:
                    level.submitter = new_submitter
                    level.save()
                messages.success(request, f"Transferred {levels.count()} levels to {new_submitter.display_name}.")
        else:
            messages.error(request, "Invalid form submission.")

    return Response(request, request.resolver_match.view_name, {})