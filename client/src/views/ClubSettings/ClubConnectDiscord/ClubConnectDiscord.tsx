import { Shell } from "@cafe/components/Shell"
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken"
import { Club } from "@cafe/types/club"
import { Form } from "@django-bridge/react"
import { Button, Center, Paper, Select, Stack, Text } from "@mantine/core";

import styles from "./ClubConnectDiscord.module.css";
import { CreateClubForm } from "@cafe/components/CreateClubForm/CreateClubForm";
import { useState } from "react";

type ClubConnectDiscordProps = {
    clubs: Club[],
    guild_id: string | null
}

function ClubConnectDiscordNotOwned() {
    const [createClubFormOpen, setCreateClubFormOpen] = useState(false);

    return (
        <>
            <CreateClubForm
                opened={createClubFormOpen}
                onClose={() => setCreateClubFormOpen(false)}
                redirectTo={window.location.pathname}
            />
            <Stack>
                <Text>You are not an owner of any clubs.</Text>
                <Text>Create a club first to get started.</Text>
                <Button onClick={() => setCreateClubFormOpen(true)}>Create a club</Button>
            </Stack>
        </>
    )
}

function ClubConnectDiscordForm({clubs}: {clubs: Club[]}) {
    const csrfInput = useCSRFTokenInput();
    const [selectedClub, setSelectedClub] = useState<Club | null>(null);    

    return (
        <Form
            method="POST"
        >
            { csrfInput }
            <Stack>
                <Text>Select a club to connect to the Discord server:</Text>
                <Select
                    clearable
                    label="Club"
                    value={selectedClub?.id || ""}
                    data={clubs.map(club => ({
                        value: club.id,
                        label: `${club.name} (${club.id})`
                    }))}
                    name="club_id"
                    onChange={(e) => {
                        const club = clubs.find(c => c.id === e);
                        setSelectedClub(club || null);
                    }}
                >
                </Select>
                <Button
                    disabled={!selectedClub}
                    type="submit"
                >
                    Connect
                </Button>
            </Stack>
        </Form>
    )

}

export function ClubConnectDiscord({clubs, guild_id}: ClubConnectDiscordProps) {
    let content;

    if (guild_id === null) {
        content = (
            <>
                <p>Signature not valid or has expired. Try running the command again.</p>
                <p>If it still doesn't work, it's a bug; please ping auburn!</p>
            </>
        )
    } else if (clubs.length === 0) {
        content = <ClubConnectDiscordNotOwned />;
    } else {
        content = <ClubConnectDiscordForm clubs={clubs} />
    }
                        

    return (
        <Shell>
            <Center className={styles.base}>
                <Paper shadow="md" p="xl">
                    {content}
                </Paper>
            </Center>
        </Shell>
    )
}