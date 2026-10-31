
from cafe.bridge.response import Response
from cafe.views.rdlevels.peerreview.pr_levels import get_pr_pending_levels
from cafe.views.types import AuthenticatedHttpRequest
from cafe.webhooks import is_allowed_webhook_url
from cryptography.fernet import Fernet
from django import forms
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from rules.contrib.views import permission_required


class WebhookForm(forms.Form):
    webhook_url = forms.URLField()

@permission_required('cafe.peerreview_rdlevel')
def pr_make_webhook(request: AuthenticatedHttpRequest):
    pr_levels = get_pr_pending_levels()
    if request.method == 'POST':
        form = WebhookForm(request.POST)
        if form.is_valid():
            webhook_url = form.cleaned_data['webhook_url']

            if not is_allowed_webhook_url(webhook_url):
                messages.error(request, "Invalid webhook URL domain")
                return Response(request, request.resolver_match.view_name, {
                    "levels": [level.to_dict() for level in pr_levels]
                })
            
            try:
                # Encrypt the webhook URL
                cipher = Fernet(settings.WEBHOOK_ENCRYPTION_KEY.encode())
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