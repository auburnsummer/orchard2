import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "../ClubSettingsNavbar/ClubSettingsNavbar";
import { Form } from "@django-bridge/react";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Button, Stack, TextInput, Tooltip } from "@mantine/core";

type ClubSettingsInfoViewProps = {
    club: Club
    can_edit: boolean
};

export function ClubSettingsInfoView({club, can_edit: canEdit}: ClubSettingsInfoViewProps) {
    const input = useCSRFTokenInput();

    const submitButton = <Button
        type="submit"
        disabled={!canEdit}
    >
        Save
    </Button>
    
    return (
        <Shell
            navbar={<ClubSettingsNavbar club={club} />}
        >
            <h2>Group {club.name} settings</h2>
            <Form method="post">
                { input }
                <Stack align="flex-start" gap="1rem">
                    <TextInput
                        name="name"
                        label="Group name"
                        defaultValue={club.name}
                    />
                    {!canEdit && (
                        <Tooltip label="You have to be an owner of the group to edit.">
                            {submitButton}
                        </Tooltip>
                    )}
                    {
                        canEdit && (
                            <>
                                {submitButton}
                            </>
                        )
                    }
                </Stack>
            
            </Form>
        </Shell>
    )
}