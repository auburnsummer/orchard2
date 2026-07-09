import { Club } from "@cafe/types/club";
import { Words } from "@cafe/components/ui/Words";
import { Navbar } from "@cafe/components/ui/Navbar";

type ClubSettingsNavbarProps = {
  club: Club;
};

export function ClubSettingsNavbar({ club }: ClubSettingsNavbarProps) {
  const links = [
    {
      label: "Settings",
      href: `/groups/${club.id}/settings/`,
    },
    {
      label: "Members",
      href: `/groups/${club.id}/settings/members/`,
    },
    {
      label: "Connected Discord servers",
      href: `/groups/${club.id}/settings/connections/discord/`,
    },
    {
      label: "Levels",
      href: `/levels?q=&club_id=${club.id}&peer_review=all&show_hidden=all`
    },
    {
      label: "Delete Group",
      href: `/groups/${club.id}/settings/delete/`,
    }
  ];

  return (
    <Navbar
      links={links}
      beforeLinks={
        <div className="flex flex-row items-center pt-2 px-2">
          <Words variant="header" as="h2" className="pl-1 py-2">{club.name}</Words>
        </div>
      }
      afterLinks={
        <>
          <div className="flex-grow"/>
          <Words className="px-3 pb-3 text-xs" as="span" variant="muted">
            Club ID: {club.id}
          </Words>
        </>
      }
    />
  );
}
