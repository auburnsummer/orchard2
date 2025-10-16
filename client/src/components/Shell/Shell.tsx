import { Logo } from "./Logo";
import { useUser } from "@cafe/hooks/useUser";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useRef } from "react";
import { Link } from "@cafe/minibridge/components/Link";
import { useLocation, useSearchParams } from "@cafe/minibridge/hooks";
import { SearchBar } from "./SearchBar";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";

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
    <div>
      <header className="flex h-12 items-stretch bg-violet-300">
        <Logo />
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
                    <img
                      src={
                        user.avatarURL ||
                        `https://www.gravatar.com/avatar/?d=initials&name=${encodeURIComponent(user.displayName)}`
                      }
                      alt="User avatar"
                      className="m-1 h-10 w-10 rounded-full border-2 border-stone-50 hover:cursor-pointer hover:border-violet-200"
                    />
                  </div>
                </MenuButton>
                <MenuItems
                  transition
                  className="absolute right-0 z-10 mt-2 w-56 origin-top-right divide-y divide-stone-100 rounded-md bg-white shadow-lg outline-1 outline-black/5 transition data-closed:scale-95 data-closed:transform data-closed:opacity-0 data-enter:duration-100 data-enter:ease-out data-leave:duration-75 data-leave:ease-in dark:divide-white/10 dark:bg-stone-800 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10"
                >
                  <div className="px-4 py-3">
                    <p className="text-sm text-stone-700 dark:text-stone-400">
                      {user.displayName}
                    </p>
                  </div>
                  <div className="py-1">
                    {menuItems.map((item) => (
                      <MenuItem key={item.name}>
                        {item.href ? (
                          <Link
                            href={item.href}
                            className="block px-4 py-2 text-sm text-stone-700 data-focus:bg-violet-50 data-focus:text-violet-900 data-focus:outline-hidden dark:text-stone-300 dark:data-focus:bg-white/5 dark:data-focus:text-white"
                          >
                            {item.name}
                          </Link>
                        ) : (
                          <button
                            onClick={item.onClick}
                            className="block w-full px-4 py-2 text-left text-sm text-stone-700 data-focus:cursor-pointer data-focus:bg-violet-50 data-focus:text-violet-900 data-focus:outline-hidden dark:text-stone-300 dark:data-focus:bg-white/5 dark:data-focus:text-white"
                          >
                            {item.name}
                          </button>
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
      {navbar && <div>{navbar}</div>}
      {aside && <aside>{aside}</aside>}
      <main>
        <div>{children}</div>
      </main>
    </div>
  );
}
