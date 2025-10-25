import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Club } from "@cafe/types/club";

import { CreateClubForm } from "@cafe/components/CreateClubForm";
import { useState } from "react";
import { DiscordGuild } from "@cafe/types/discordGuild";
import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter";
import { Form } from "@cafe/minibridge/components/Form";
import { Dialog } from "@cafe/components/ui/Dialog";
import { Words } from "@cafe/components/ui/Words";
import { Button } from "@cafe/components/ui/Button";
import { Alert } from "@cafe/components/ui/Alert";
import Select from "@cafe/components/ui/Select";

type ClubConnectDiscordProps = {
  clubs: Club[];
  guild_id: string | null;
  existing_guild: DiscordGuild | null;
};

function ClubConnectDiscordNotOwned() {
  const [createClubFormOpen, setCreateClubFormOpen] = useState(false);

  return (
    <>
      <Dialog
        open={createClubFormOpen}
        onClose={() => setCreateClubFormOpen(false)}
      >
        <CreateClubForm
          onSubmit={() => setCreateClubFormOpen(false)}
          redirectTo={window.location.pathname}
        />
      </Dialog>
      <div>
        <Words as="p">You are not an owner of any groups.</Words>
        <Words as="p">Create a group first to get started.</Words>
        <Button onClick={() => setCreateClubFormOpen(true)} className="mt-2" variant="primary">
          Create a group
        </Button>
      </div>
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
      <div className="flex flex-col gap-2">
        {existing_guild !== null && (
          <Alert variant="warning">
            <Words as="p">This Discord server is already connected to a group!</Words>
            <Words as="p">
              A Discord server can only be connected to one group at a time.
            </Words>
            <Words as="p">
              If you connect a new group, the existing group (
              {existing_guild.club.name}) will be disconnected.
            </Words>
          </Alert>
        )}
        <Words as="p">Select a group to connect to this Discord server:</Words>
        <Select
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
        <Button disabled={!selectedClub} type="submit" className="mt-4" variant="primary">
          Connect
        </Button>
      </div>
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
        <Words as="p">
          Signature not valid or has expired. Try running the command again.
        </Words>
        <Words as="p">If it still doesn't work, it's a bug; please ping auburn!</Words>
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
      {content}
    </ShellDramaticCenter>
  );
}
