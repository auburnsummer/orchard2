import { Popover, PopoverButton, PopoverPanel } from "@headlessui/react";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Header } from "./Header";

export type ShellProps = {
  children: React.ReactNode;
  navbar?: React.ReactNode;
  aside?: React.ReactNode;
};

export function Shell({ children, navbar, aside }: ShellProps) {
  return (
    <div className="flex flex-col h-screen bg-slate-300 dark:bg-slate-600">
      <Header />
      <div className="relative flex flex-grow items-stretch justify-stretch min-h-0">
        { /* sidebar visible alway past sm */}
        {navbar && <div className="hidden sm:flex min-w-72 flex-col items-stretch overflow-y-auto">{navbar}</div>}
        { /* sidebar as overlay on small screens */}
        {
          navbar && (
            <Popover className="sm:hidden relative">
              <PopoverButton className="absolute top-12 left-0 bg-violet-300 rounded-tr-lg rounded-br-lg opacity-60 hover:opacity-100 hover:cursor-pointer">
                <FontAwesomeIcon icon={faBars} className="text-xs text-violet-600" />
              </PopoverButton>
              <PopoverPanel className="fixed top-12 left-0 z-20 h-full w-72 flex flex-col overflow-y-auto">
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
