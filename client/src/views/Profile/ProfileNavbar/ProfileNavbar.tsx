import { Spacer } from "@cafe/components/Spacer/Spacer";
import { useLoggedInUser } from "@cafe/hooks/useUser";
import { Stack, Group, NavLink, Text } from "@mantine/core";
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";
import { Avatar } from "@cafe/components/ui/Avatar";
import { NavEntry } from "@cafe/components/ui/NavEntry";

import cc from "clsx";

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
  ];

  return (
    <div className="flex-grow bg-slate-50 m-3 rounded-lg flex flex-col gap-1">
      <div className="flex flex-row items-center pt-3 px-3">
        <Avatar src={user.avatarURL || undefined} className="w-14 h-14 border-violet-400 border-2" />
        <h2 className="ml-3">{user.displayName}</h2>
      </div>
      <div className="flex flex-col">
        {links.map((link) => (
          <NavEntry as={Link} href={link.href} className={cc({"bg-violet-100 dark:bg-white/10" : pathname === link.href})}>
            {link.label}
          </NavEntry>
        ))}
      </div>
      <div className="flex-grow"/>
      <span className="px-3 pb-3 text-sm text-slate-500 dark:text-slate-400">
        User ID: {user.id}
      </span>
    </div>
  );
}
