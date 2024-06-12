from django.shortcuts import render

def members(request, group_id):
    return render(request, "cafe/club_settings/members.jinja")
