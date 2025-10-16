import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Club } from "@cafe/types/club";
import { Alert, Button, Paper, Select, Stack, Text } from "@mantine/core";

import { CreateClubForm } from "@cafe/components/CreateClubForm/CreateClubForm";
import { useState } from "react";
import { DiscordGuild } from "@cafe/types/discordGuild";
import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter/ShellDramaticCenter";
import { Form } from "@cafe/minibridge/components/Form";

type ClubConnectDiscordProps = {
  clubs: Club[];
  guild_id: string | null;
  existing_guild: DiscordGuild | null;
};

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
        <Text>You are not an owner of any groups.</Text>
        <Text>Create a group first to get started.</Text>
        <Button onClick={() => setCreateClubFormOpen(true)}>
          Create a group
        </Button>
      </Stack>
    </>
  );
}

function ClubConnectDiscordForm({
  clubs,
  existing_guild,
}: Pick<ClubConnectDiscordProps, "clubs" | "existing_guild">) {
  const csrfInput = useCSRFTokenInput();
  const [selectedClub, setSelectedClub] = useState<Club | null>(null);

  return (
    <Form method="POST">
      {csrfInput}
      <Stack justify="start" align="start">
        {existing_guild !== null && (
          <Alert>
            <Text>This Discord server is already connected to a group!</Text>
            <Text>
              A Discord server can only be connected to one group at a time.
            </Text>
            <Text>
              If you connect a new group, the existing group (
              {existing_guild.club.name}) will be disconnected.
            </Text>
          </Alert>
        )}
        <Text>Select a group to connect to the Discord server:</Text>
        <Select
          clearable
          label="Group"
          value={selectedClub?.id || ""}
          data={clubs.map((club) => ({
            value: club.id,
            label: `${club.name} (${club.id})`,
          }))}
          name="club_id"
          onChange={(e) => {
            const club = clubs.find((c) => c.id === e);
            setSelectedClub(club || null);
          }}
        ></Select>
        <Button disabled={!selectedClub} type="submit">
          Connect
        </Button>
      </Stack>
    </Form>
  );
}

export function ClubSettingsConnectDiscord({
  clubs,
  guild_id,
  existing_guild,
}: ClubConnectDiscordProps) {
  let content;

  if (guild_id === null) {
    content = (
      <>
        <p>
          Signature not valid or has expired. Try running the command again.
        </p>
        <p>If it still doesn't work, it's a bug; please ping auburn!</p>
      </>
    );
  } else if (clubs.length === 0) {
    content = <ClubConnectDiscordNotOwned />;
  } else {
    content = (
      <ClubConnectDiscordForm clubs={clubs} existing_guild={existing_guild} />
    );
  }

  return (
    <ShellDramaticCenter>
      <Paper shadow="md" p="xl">
        {content}
      </Paper>
    </ShellDramaticCenter>
  );
}
