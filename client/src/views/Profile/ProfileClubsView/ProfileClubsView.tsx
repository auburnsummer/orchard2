import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "../ProfileNavbar/ProfileNavbar";

import styles from "./ProfileClubsView.module.css";
import { Club } from "@cafe/types/club";
import { Stack, Title, List, Button, Anchor } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { CreateClubForm } from "@cafe/components/CreateClubForm/CreateClubForm";
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";

type ProfileClubsViewProps = {
  clubs: {
    club: Club;
    role: "owner" | "admin";
  }[];
};
function LinkToClub({ club }: { club: Club }) {
  return (
    <Anchor component={Link} href={`/groups/${club.id}/settings/`}>
      {club.name}
    </Anchor>
  );
}

export function ProfileClubsView({ clubs }: ProfileClubsViewProps) {
  const { pathname } = useAtomValue(locationAtom);

  const [createClubFormOpen, { open: openCreateClub, close: closeCreateClub }] =
    useDisclosure(false);

  const ownerClubs = clubs.filter((c) => c.role === "owner");
  const adminClubs = clubs.filter((c) => c.role === "admin");

  return (
    <Shell navbar={<ProfileNavbar />}>
      <CreateClubForm
        opened={createClubFormOpen}
        onClose={closeCreateClub}
        redirectTo={pathname}
      />
      <Stack className={styles.base} align="start">
        <Title order={2}>Groups</Title>
        {ownerClubs.length > 0 && (
          <>
            <Title order={3}>Owner</Title>
            <List>
              {ownerClubs.map((c) => (
                <List.Item key={c.club.id}>
                  <LinkToClub club={c.club} />
                </List.Item>
              ))}
            </List>
          </>
        )}
        {adminClubs.length > 0 && (
          <>
            <Title order={3}>Admin</Title>
            <List>
              {adminClubs.map((c) => (
                <List.Item>
                  <LinkToClub club={c.club} />
                </List.Item>
              ))}
            </List>
          </>
        )}
        <Button onClick={openCreateClub}>Create group</Button>
      </Stack>
    </Shell>
  );
}
