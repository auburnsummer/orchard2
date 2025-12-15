import { useLoggedInUser } from "@cafe/hooks/useUser";
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";
import { Avatar } from "@cafe/components/ui/Avatar";
import { NavEntry } from "@cafe/components/ui/NavEntry";

import cc from "clsx";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";

export function ProfileNavbar() {
  const user = useLoggedInUser();
  const { pathname } = useAtomValue(locationAtom);

  const links = [
    {
      label: "Profile",
      href: "/accounts/profile/",
    },
    {
      label: "Settings",
      href: "/accounts/profile/settings/",
    },
    {
      label: "Groups",
      href: "/accounts/profile/groups/",
    },
    {
      label: "API Key",
      href: "/accounts/profile/api-key/"
    }
  ];

  return (
    <Surface className="flex-grow m-3 flex flex-col gap-1">
      <div className="flex flex-row items-center pt-3 px-3">
        <Avatar src={user.avatarURL || undefined} className="w-14 h-14 border-violet-400 border-2" />
        <Words className="ml-3" as="h2">{user.displayName}</Words>
      </div>
      <div className="flex flex-col">
        {links.map((link) => (
          <NavEntry as={Link} href={link.href} active={pathname === link.href}>
            {link.label}
          </NavEntry>
        ))}
      </div>
      <div className="flex-grow"/>
      <Words className="px-3 pb-3 text-xs" as="span" variant="muted">
        User ID: {user.id}
      </Words>
    </Surface>
  );
}
