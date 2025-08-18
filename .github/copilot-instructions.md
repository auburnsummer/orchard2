# Orchard2 Development Guide

Orchard2 is a Django + React application for rhythm.cafe v2, using a custom Django-Bridge architecture for seamless frontend/backend integration.

## Architecture Overview

- **Backend**: Django 5.1 with Django-Bridge for React integration
- **Frontend**: React 19 + Vite + Mantine UI + Jotai state management
  - the URL for the frontend is defined by the `DOMAIN_URL` environment variable 
- **Bridge**: Custom "minibridge" system handles routing/state between Django views and React components
- **Services**: Redis (Huey tasks), Typesense (search), MinIO (S3-compatible storage)
- **Deployment**: Multi-stage Docker build with Caddy reverse proxy

## Key Patterns

### Django-Bridge Integration
The app uses `django-bridge` to render React components from Django views:
```python
# server/cafe-backend/cafe/views/index.py
from django_bridge.response import Response
def index(request: HttpRequest) -> HttpResponse:
    return Response(request, request.resolver_match.view_name, {})
```

React components are mapped to Django URL names in `client/src/routeMap.ts`:
```typescript
export const routeMap = {
    "cafe:index": HomeView,
    "cafe:profile": ProfileIndexView,
    // ...
}
```

### Context Providers
Django contexts are automatically passed to React via `DJANGO_BRIDGE.CONTEXT_PROVIDERS` in settings.py:
- `csrf_token`: CSRF token for forms
- `user`: Authenticated user data or `{authenticated: false}`

### UV Workspace Structure
The server uses a uv workspace with multiple packages:
- `cafe-backend`: Main Django application
- `rdlevel_parse`: Rhythm Doctor level parsing
- `utils`, `vitals`, `essfree`: Supporting libraries

## Development Workflow

### Local Setup
Use `Procfile` with process manager (hivemind/foreman):
```bash
server: cd ./server/cafe-backend && uv run python manage.py runserver
client: cd ./client && npm run dev -- --clearScreen false
huey: cd ./server/cafe-backend && uv run python manage.py run_huey
typesense: ./typesense-server --api-key=key --data-dir=./data.typesense
minio: minio server ./data.minio
```

### Key Commands
- `uv sync` - Install Python dependencies (run from `/server`)
- `npm run dev` - Start Vite dev server (run from `/client`)
- `python manage.py runserver` - Django server (run from `/server/cafe-backend`)
- `python manage.py run_huey` - Background task worker

### Authentication Flow
Uses Django-Allauth with Discord OAuth:
- `SOCIALACCOUNT_ONLY = True` - No username/password login
- Custom `CafeSocialAccountAdapter` in `cafe/social_adapter.py`
- User model extends `AbstractUser` with nanoid-based IDs

### Background Tasks
Uses Huey with Redis for async processing:
- Task definitions in `cafe/tasks/`
- Priority Redis queue configured in settings.py
- Common pattern: `@task()` decorator for background operations

### Search Integration
Typesense for full-text search:
- API configured via environment variables
- Setup command: `python manage.py setuptypesense`
- Search views in `cafe/views/rdlevels/search_levels.py`

## File Organization

### Django App Structure
```
server/cafe-backend/cafe/
├── models/        # Domain models (users, clubs, rdlevels)
├── views/         # Django views organized by feature
├── contexts/      # Django-Bridge context providers
├── tasks/         # Huey background tasks
└── templates/     # Django templates (minimal, mostly for Django-Bridge)
```

### React App Structure  
```
client/src/
├── views/         # Page components mapped to Django URLs
├── components/    # Reusable UI components
├── minibridge/    # Custom Django-Bridge client implementation
├── hooks/         # Custom React hooks (useUser, useCSRFToken)
└── types/         # TypeScript type definitions
```

### Environment Configuration
Key `.env` variables (in `server/cafe-backend/`):
- Discord OAuth: `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET`  
- Services: `REDIS_HOST`, `TYPESENSE_API_KEY`, `S3_API_URL`
- Dev: `DEBUG=true`, `DOMAIN_URL` for OAuth callbacks

## Testing & Debugging

- Unit tests: Run from respective package directories
- Django admin: Available at `/adminnn/` (note triple 'n')
- User hijacking: Available at `/hijack/` for admin users
- Debug toolbar: Enabled when `DEBUG=true`

### Django-Bridge Test Response Structure
When testing Django-Bridge views with the `bridge_client` fixture, responses return a structured JSON format:

```python
# Example POST response structure
{
    "action": "render",
    "view": "cafe:profile_settings",  # Django URL name
    "overlay": false,
    "metadata": {"title": ""},
    "props": {},
    "context": {
        "csrf_token": "...",
        "user": {
            "authenticated": true,
            "id": "uABC123",
            "displayName": "User Name",
            "avatarURL": null,
            "theme_preference": "dark",
            "is_superuser": false
        }
    },
    "messages": [
        {
            "level": "success",  # or "error", "warning", "info"
            "html": "User updated!"
        }
    ]
}
```

Key testing patterns:
- **Context verification**: `response.json()['context']['user']['field_name']`
- **Message verification**: `response.json()['messages'][0]['level']` and `response.json()['messages'][0]['html']`
- **Structure validation**: Check `action`, `view`, and other top-level fields
- **Success/error flows**: Messages array indicates form validation results
- **ModelForm behavior**: Missing POST fields reset to model defaults, not preserved values

### Django-Bridge Redirect Handling
The `bridge_client` fixture (with `X-Requested-With: DjangoBridge` header) intercepts redirects and returns them as JSON responses instead of following them:

```python
# Regular Django redirect would return 302, but bridge_client returns:
{
    "action": "redirect",
    "path": "/groups/testclub/settings/members/"
}
```

**Important**: When testing views that use `HttpResponseRedirect`:
- Use `assert response.status_code == 200` (not 302)
- Check `body['action'] == 'redirect'` 
- Verify redirect path with `body['path']`
- Note: `messages` are NOT included in redirect responses

## Deployment Notes

- Uses multi-stage Docker build
- Caddy serves static files and proxies to Django
- Environment variables control production vs development paths
- `start.sh` handles migrations and Typesense setup on container start
