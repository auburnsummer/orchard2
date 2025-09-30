"""
1. a level creation is instantiated from the /add Discord command, see server/cafe-backend/cafe/views/discord_bot/handlers/add.py
    - this generates a URL to the level creation page cafe:level_portal (i.e. prefill_stage_one) with a signed code
2. the user selects if it's a new level or update to existing level. a form POST occurs to the same URL with prefill_type=new or prefill_type=update
3. an RDLevelPrefillResult is created to store the prefill data and the run_prefill task is triggered
4. the user is redirected to the cafe:level_from_prefill page (i.e. prefill_stage_two) immediately
5. the prefill hasn't finished yet (presumably), so the user sees a loading screen. the loading screen polls for updates and reloads the page once prefill is ready.
6. if prefill_type=new:
    a. the user sees a form to create a new level. the fields are prefilled with the data from the RDLevelPrefillResult.
    b. the user submits the form, and a new level is created with the prefilled data.
7. if prefill_type=update:
    a. the user must select the level id corresponding to the existing level they want to update.
    b. the user submits the form, and the existing level is updated with the prefilled data.
        - note that in update, the prefilled data only contains fields relating to file URLs etc
"""
