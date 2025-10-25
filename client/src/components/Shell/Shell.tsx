import { Logo } from "./Logo";
import { useUser } from "@cafe/hooks/useUser";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useRef } from "react";
import { Link } from "@cafe/minibridge/components/Link";
import { useLocation, useSearchParams } from "@cafe/minibridge/hooks";
import { SearchBar } from "./SearchBar";
import { Menu, MenuButton, MenuItem, MenuItems, Popover, PopoverButton, PopoverPanel } from "@headlessui/react";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import { Avatar } from "../ui/Avatar";
import { NavEntry } from "../ui/NavEntry";

export type ShellProps = {
  children: React.ReactNode;
  navbar?: React.ReactNode;
  aside?: React.ReactNode;
};

export function Shell({ children, navbar, aside }: ShellProps) {
  const user = useUser();
  const csrfInput = useCSRFTokenInput();
  const logOutForm = useRef<HTMLFormElement>(null);
  const [location, navigate] = useLocation();
  const [searchParams] = useSearchParams();

  const onSearch = (query: string) => {
    const url = new URL(
      `/levels/?q=${encodeURIComponent(query)}`,
      window.location.origin,
    );
    navigate(url);
  };

  const menuItems = [
    { name: "Profile", href: "/accounts/profile/" },
    user.authenticated && user.is_superuser
      ? { name: "Admin", href: "/adminnn/" }
      : null,
    { name: "Log out", onClick: () => logOutForm.current?.submit() },
  ].filter((a) => a !== null);

  return (
    <div className="flex flex-col min-h-screen bg-slate-300 dark:bg-slate-600">
      <header className="fixed top-0 left-0 right-0 z-30 flex h-12 items-stretch bg-violet-300 dark:bg-violet-950 shadow-sm">
        <Logo className="z-10"/>
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
                          <NavEntry as={Link} href={item.href}>{item.name}</NavEntry>
                        ) : (
                          <NavEntry as="button" onClick={item.onClick}>{item.name}</NavEntry>
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
      <div className="relative flex-grow flex items-stretch justify-stretch pt-12">
        { /* sidebar visible alway past sm */}
        {navbar && <div className="hidden sm:flex w-72 flex-col">{navbar}</div>}
        { /* sidebar as overlay on small screens */}
        {
          navbar && (
            <Popover className="sm:hidden relative">
              <PopoverButton className="absolute top-12 left-0 bg-violet-300 rounded-tr-lg rounded-br-lg opacity-60 hover:opacity-100 hover:cursor-pointer">
                <FontAwesomeIcon icon={faBars} className="text-xs text-violet-600" />
              </PopoverButton>
              <PopoverPanel className="fixed top-12 left-0 z-20 h-full w-72 flex flex-col">
                {navbar}
              </PopoverPanel>
            </Popover>
          )
        }
        <main className="flex-grow overflow-y-auto">
          {children}
        </main>
        {aside && <aside className="flex-shrink-0 overflow-y-auto sticky top-12 h-screen">{aside}</aside>}
      </div>
    </div>
  );
}
