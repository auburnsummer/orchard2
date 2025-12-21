
from django import forms
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django_bridge.response import Response
from rules.contrib.views import permission_required
from cryptography.fernet import Fernet

from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.views.types import AuthenticatedHttpRequest


class WebhookForm(forms.Form):
    webhook_url = forms.URLField()

cipher = Fernet(settings.WEBHOOK_ENCRYPTION_KEY.encode())

@permission_required('cafe.peerreview_rdlevel')
def pr_make_webhook(request: AuthenticatedHttpRequest):
    # we want the oldest level first
    pr_levels = RDLevel.objects.filter(approval=0).order_by('last_updated')
    if request.method == 'POST':
        form = WebhookForm(request.POST)
        if form.is_valid():
            webhook_url = form.cleaned_data['webhook_url']
            
            try:
                # Encrypt the webhook URL
                encrypted_url = cipher.encrypt(webhook_url.encode()).decode()
                                
                messages.success(request, "Webhook encrypted successfully")
                
                return Response(request, request.resolver_match.view_name, {
                    "encrypted_url": reverse('cafe:execute_webhook', args=[encrypted_url]),
                    "levels": [level.to_dict() for level in pr_levels]
                })
            except Exception as e:
                messages.error(request, f"Failed to encrypt webhook: {str(e)}")
        else:
            messages.error(request, "Invalid form submission")
    
    return Response(request, request.resolver_match.view_name, {
        "levels": [level.to_dict() for level in pr_levels]
    })