import { useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import { Menu, MenuButton, MenuItem, MenuItems, Popover, PopoverButton, PopoverPanel } from "@headlessui/react";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useUser } from "@cafe/hooks/useUser";
import { useLocation, useSearchParams } from "@cafe/minibridge/hooks";
import { Link } from "@cafe/minibridge/components/Link";
import { Avatar } from "../ui/Avatar";
import { NavEntry } from "../ui/NavEntry";
import { Logo } from "./Logo";
import { SearchBar } from "./SearchBar";

export function Header({ navbar }: { navbar?: React.ReactNode }) {
  const user = useUser();
  const csrfInput = useCSRFTokenInput();
  const logOutForm = useRef<HTMLFormElement>(null);
  const [location, navigate] = useLocation();
  const [searchParams] = useSearchParams();

  const onSearch = (query: string) => {
    const currPeerReviewQ = searchParams.get("peer_review");
    const params = new URLSearchParams();
    params.set("q", query);
    if (currPeerReviewQ) {
      params.set("peer_review", currPeerReviewQ);
    }
    const url = new URL(
      `/levels/?${params.toString()}`,
      window.location.origin,
    );
    navigate(url);
  };

  const menuItems = [
    { name: "Settings", href: "/accounts/profile/settings/" },
    user.authenticated && user.is_superuser
      ? { name: "Admin", href: "/adminnn/" }
      : null,
    user.authenticated && user.is_peer_reviewer
      ? { name: "Peer Review Dashboard", href: "/peer-review/" }
      : null,
    // NB: currently permissions for peer review and daily blend are
    // tied together in the same thing (pharmacists)
    user.authenticated && user.is_peer_reviewer
      ? { name: "Daily Blend Dashboard", href: "/daily-blend/" }
      : null,
    { name: "Log out", onClick: () => logOutForm.current?.submit() },
  ].filter((a) => a !== null);

  return (
    <header className="flex-shrink-0 flex h-12 items-stretch bg-violet-300 dark:bg-violet-950 shadow-sm">
      {navbar && (
        <Popover className="sm:hidden relative flex flex-col">
          <PopoverButton className="ml-2 px-2 hover:bg-violet-400 dark:hover:bg-violet-900 rounded hover:cursor-pointer flex-grow">
            <FontAwesomeIcon icon={faBars} className="text-violet-700 dark:text-violet-300 flex-grow" />
          </PopoverButton>
          <PopoverPanel className="fixed top-12 left-0 bottom-0 z-20 w-72 flex flex-col overflow-y-auto">
            {navbar}
          </PopoverPanel>
        </Popover>
      )}
      <Logo className="z-10 hidden sm:block" />
      <SearchBar
        className="ml-4"
        initialValue={searchParams.get("q") || ""}
        placeholder="Search levels..."
        onSearch={onSearch}
      />
      <div className="flex-grow" />
      <div className="flex items-stretch">
        {user.authenticated ? (
          <>
            <form method="post" action="/accounts/logout/" ref={logOutForm}>
              {csrfInput}
            </form>
            <Menu as="div" className="relative">
              <MenuButton>
                <div>
                  <Avatar
                    username={user.displayName}
                    className="hover:cursor-pointer hover:border-violet-200"
                    src={user.avatarURL || undefined}
                  />
                </div>
              </MenuButton>
              <MenuItems
                transition
                className="absolute right-0 z-10 mt-1 mr-2 w-56 origin-top-right divide-y divide-slate-100 rounded-md bg-white shadow-lg outline-1 outline-black/5 transition data-closed:scale-95 data-closed:transform data-closed:opacity-0 data-enter:duration-100 data-enter:ease-out data-leave:duration-75 data-leave:ease-in dark:divide-white/10 dark:bg-slate-800 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10"
              >
                <div className="px-4 py-3">
                  <p className="text-sm text-slate-700 dark:text-slate-400">
                    {user.displayName}
                  </p>
                </div>
                <div className="py-1">
                  {menuItems.map((item) => (
                    <MenuItem key={item.name}>
                      {item.href ? (
                        <NavEntry as={Link} href={item.href}>
                          {item.name}
                        </NavEntry>
                      ) : (
                        <NavEntry as="button" onClick={item.onClick}>
                          {item.name}
                        </NavEntry>
                      )}
                    </MenuItem>
                  ))}
                </div>
              </MenuItems>
            </Menu>
          </>
        ) : (
          <form
            method="post"
            action="/accounts/discord/login/"
            className="flex"
          >
            <input type="hidden" name="next" value={location.pathname} />
            {csrfInput}
            <button
              className="my-1 mr-3 flex items-center rounded-lg bg-violet-500 px-3 text-violet-50 hover:cursor-pointer hover:bg-violet-600"
              type="submit"
            >
              <FontAwesomeIcon icon={faDiscord} className="mr-2" />
              <span>Log in</span>
            </button>
          </form>
        )}
      </div>
    </header>
  );
}
