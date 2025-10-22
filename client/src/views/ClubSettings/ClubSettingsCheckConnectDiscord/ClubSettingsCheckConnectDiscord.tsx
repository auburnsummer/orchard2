import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "../ClubSettingsNavbar";
import {
  Alert,
  Anchor,
  Box,
  Button,
  Group,
  Text,
  TextInput,
} from "@mantine/core";
import { DiscordGuild } from "@cafe/types/discordGuild";
import { Form } from "@cafe/minibridge/components/Form";

type ClubSettingsCheckConnectDiscordProps = {
  club: Club;
  discord_guild: DiscordGuild | null;
  did_check: boolean;
};

export function ClubSettingsCheckConnectDiscord({
  club,
  discord_guild,
  did_check,
}: ClubSettingsCheckConnectDiscordProps) {
  return (
    <Shell navbar={<ClubSettingsNavbar club={club} />}>
      <Box pt="md">
        <Text>
          Connecting a Discord server is done from the Discord server itself!
        </Text>
        <Text>
          Please refer to{" "}
          <Anchor href="https://github.com/auburnsummer/orchard2/wiki/Instructions-for-Server-Owners">
            Instructions for Server Owners
          </Anchor>{" "}
          for how to connect.
        </Text>
        <Text>
          You can use this page to check if your server is connected, by
          entering the Server ID below:
        </Text>
        <Form method="GET">
          <Group align="end">
            <TextInput
              type="text"
              label="Server ID"
              name="guild_id"
            ></TextInput>
            <Button type="submit">Check</Button>
          </Group>
        </Form>
        {did_check && (
          <Alert mt="md" mr="md">
            {discord_guild === null ? (
              <Text>Your server is not connected to this group.</Text>
            ) : (
              <Text>Your server is connected to this group!</Text>
            )}
          </Alert>
        )}
      </Box>
    </Shell>
  );
}
