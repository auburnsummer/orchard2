import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter/ShellDramaticCenter";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";
import { Button, Paper, Text, Title, Stack } from "@mantine/core";
import { ReactNode } from "react";

type ClubSettingsRedeemInviteProps = {
    invite: {
        club: Club
    } | null,
    code: string,
    expiry: string,
    role: 'owner' | 'admin'
}


export function ClubSettingsRedeemInvite(props: ClubSettingsRedeemInviteProps) {
    const input = useCSRFTokenInput();

    let content: ReactNode;
    if (props.invite === null) {
        content = (
            <>
                <Text>The invite is invalid or has expired.</Text>
                <Text>Please ask the person who invited you to send a new invite.</Text>
                <Text>If it keeps happening, please ping Auburn for help.</Text>
            </>
        )
    } else {
        content = (
            <Form method="post">
                {input}
                <Stack gap="xs">
                    <Title order={2}>Redeem Invite</Title>
                    <Text>You are being invited to the group <b>{props.invite.club.name}</b></Text>
                    <Button type="submit">Join {props.invite.club.name}</Button>
                </Stack>
            </Form>
        )
    }
    return (
        <ShellDramaticCenter>
            <Paper shadow="md" p="xl">
                {content}
            </Paper>
        </ShellDramaticCenter>
    )
}