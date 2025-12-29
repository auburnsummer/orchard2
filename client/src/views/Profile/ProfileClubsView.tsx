import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "./ProfileNavbar";

import { Club } from "@cafe/types/club";
import { useDisclosure } from "@mantine/hooks";
import { CreateClubForm } from "@cafe/components/CreateClubForm";
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { Button } from "@cafe/components/ui/Button";
import { Dialog } from "@cafe/components/ui/Dialog";

type ProfileClubsViewProps = {
  clubs: {
    club: Club;
    role: "owner" | "admin";
  }[];
};
function LinkToClub({ club }: { club: Club }) {
  return (
    <Words as={Link} variant="link" href={`/groups/${club.id}/settings/`}>
      {club.name}
    </Words>
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
      <Dialog open={createClubFormOpen} onClose={closeCreateClub}>
        <CreateClubForm
          redirectTo={pathname}
          onSubmit={closeCreateClub}
        />
      </Dialog>
      <Surface className="m-3 p-6 flex-grow">
        <Words as="h2" variant="header">Groups</Words>
        {ownerClubs.length > 0 && (
          <>
            <Words as="h3" variant="subheader">Owner</Words>
            <ul className="list-disc pl-5 dark:text-slate-100">
              {ownerClubs.map((c) => (
                <li key={c.club.id}>
                  <LinkToClub club={c.club} />
                </li>
              ))}
            </ul>
          </>
        )}
        {adminClubs.length > 0 && (
          <>
            <Words as="h3" variant="subheader">Admin</Words>
            <ul className="list-disc pl-5">
              {adminClubs.map((c) => (
                <li key={c.club.id}>
                  <LinkToClub club={c.club} />
                </li>
              ))}
            </ul>
          </>
        )}
        <Button onClick={openCreateClub} variant="primary" className="mt-4">
          Create group
        </Button>
      </Surface>
    </Shell>
  );
}
