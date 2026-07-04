import { useUser } from "@cafe/hooks/useUser";
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";
import { Avatar } from "@cafe/components/ui/Avatar";
import { NavEntry } from "@cafe/components/ui/NavEntry";

import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { Navbar } from "@cafe/components/ui/Navbar";

export function ProfileNavbar() {
  // you CAN reach this page without being logged in.
  // how??????
  // if you delete your account, there is a brief period where you have no account
  // but are still on this page while the page reloads to the homepage.
  const user = useUser();
  const { pathname } = useAtomValue(locationAtom);

  const links = [
    {
      label: "Settings",
      href: "/accounts/profile/settings/"
    },
    {
      label: "Your levels",
      href: "/accounts/profile/levels/"
    },
    {
      label: "Groups",
      href: "/accounts/profile/groups/"
    },
    {
      label: "API Key",
      href: "/accounts/profile/api-key/"
    },
    {
      label: "Delete account",
      href: "/accounts/profile/delete/"
    }
  ];

  const avatarUrl = user.authenticated ? user.avatarURL || undefined : undefined;
  const displayName = user.authenticated ? user.displayName : "Unknown";
  
  return (
    <Navbar
      links={links}
      beforeLinks={
        <div className="flex flex-row items-center pt-3 px-3">
          <Avatar src={avatarUrl} className="w-14 h-14 border-violet-400 border-2" />
          <Words className="ml-3" as="h2">{displayName}</Words>
        </div>
      }
      afterLinks={
        <>
          <div className="flex-grow"/>
          {
            user.authenticated && (
              <Words className="px-3 pb-3 text-xs" as="span" variant="muted">
                User ID: {user.id}
              </Words>
            )
          }
        </>
      }
    />
  )
}
