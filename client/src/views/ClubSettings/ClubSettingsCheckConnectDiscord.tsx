import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "./ClubSettingsNavbar";
import { DiscordGuild } from "@cafe/types/discordGuild";
import { Form } from "@cafe/minibridge/components/Form";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Button } from "@cafe/components/ui/Button";
import { Alert } from "@cafe/components/ui/Alert";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faExternalLink } from "@fortawesome/free-solid-svg-icons";
import { ExternalLink } from "@cafe/components/ui/ExternalLink";

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
      <Surface className="m-3 p-6 flex-grow">
        <div>
          <Words as="p">
            Connecting a Discord server is done from the Discord server itself!
          </Words>
          <Words as="p">
            Please refer to{" "}
            <ExternalLink
              href="https://github.com/auburnsummer/orchard2/wiki/Instructions-for-Server-Owners"
            >
              Instructions for Server Owners
            </ExternalLink>
            for how to connect.
          </Words>
          <Words as="p">
            You can use this page to check if your server is connected, by
            entering the Server ID below:
          </Words>
          <Form method="GET" className="mt-4">
            <div className="flex items-end gap-3">
              <TextInput
                type="text"
                label="Server ID"
                name="guild_id"
                className="flex-grow max-w-64"
              />
              <Button type="submit" variant="primary">Check</Button>
            </div>
          </Form>
          {did_check && (
            <Alert className="mt-4" variant={discord_guild === null ? "error" : "success"}>
              {discord_guild === null ? (
                <Words>Your server is not connected to this group.</Words>
              ) : (
                <Words>Your server is connected to this group!</Words>
              )}
            </Alert>
          )}
        </div>
      </Surface>
    </Shell>
  );
}
