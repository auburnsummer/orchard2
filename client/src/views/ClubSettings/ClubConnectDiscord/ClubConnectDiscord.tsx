import { Shell } from "@cafe/components/Shell"
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken"
import { Club } from "@cafe/types/club"
import { Form } from "@django-bridge/react"
import { Box, Button, Center, Select, Stack, Text } from "@mantine/core";

import styles from "./ClubConnectDiscord.module.css";

type ClubConnectDiscordProps = {
    clubs: Club[],
    guild_id: string | null
}

export function ClubConnectDiscord({clubs, guild_id}: ClubConnectDiscordProps) {
    const csrfInput = useCSRFTokenInput();
    let content;

    if (guild_id === null) {
        content = (
            <>
                <p>Signature not valid or has expired. Try running the command again.</p>
                <p>If it still doesn't work, it's a bug; please ping auburn!</p>
            </>
        )
    } else if (clubs.length === 0) {
        content = (
            <>
                <p>You are not a member of any clubs.</p>
                <p>Create a club to get started.</p>
            </>
        )
    } else {
        content = (
                <Form
                    method="POST"
                >
                    { csrfInput }
                    <Stack>
                        <Text>Select a club to connect to Discord:</Text>
                        <Select
                            data={clubs.map(club => ({
                                value: club.id,
                                label: club.name
                            }))}
                            name="club_id"
                        >
                        </Select>
                        <Button type="submit">Connect</Button>
                    </Stack>
                </Form>
        )
    }
                        

    return (
        <Shell>
            <Center className={styles.base}>
                <Box className={styles.content}>
                    {content}
                </Box>
            </Center>
        </Shell>
    )
}