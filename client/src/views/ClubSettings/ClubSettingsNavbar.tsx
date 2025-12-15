import { Club } from "@cafe/types/club";
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { NavEntry } from "@cafe/components/ui/NavEntry";

type ClubSettingsNavbarProps = {
  club: Club;
};

export function ClubSettingsNavbar({ club }: ClubSettingsNavbarProps) {
  const { pathname } = useAtomValue(locationAtom);

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
  ];

  return (
    <Surface className="flex-grow m-3 flex flex-col gap-1">
      <div className="flex flex-row items-center pt-2 px-2">
        <Words variant="header" as="h2" className="pl-1 py-2">{club.name}</Words>
      </div>
      <div className="flex flex-col">
        {links.map((link) => (
          <NavEntry 
            key={link.href}
            as={Link} 
            href={link.href}
            active={pathname === link.href}
          >
            {link.label}
          </NavEntry>
        ))}
      </div>
      <div className="flex-grow"/>
      <Words className="px-3 pb-3 text-xs" as="span" variant="muted">
        Club ID: {club.id}
      </Words>
    </Surface>
  );
}
