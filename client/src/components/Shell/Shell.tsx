import { Header } from "./Header";

export type ShellProps = {
  children: React.ReactNode;
  navbar?: React.ReactNode;
  aside?: React.ReactNode;
};

export function Shell({ children, navbar, aside }: ShellProps) {
  return (
    <div className="flex flex-col h-screen bg-slate-300 dark:bg-slate-600">
      <Header navbar={navbar} />
      <div className="relative flex flex-grow items-stretch min-h-0">
        {/* sidebar visible always past sm */}
        {navbar && <div className="hidden sm:flex min-w-72 flex-col overflow-y-auto">{navbar}</div>}
        <main className="flex-grow overflow-y-auto">
          {children}
        </main>
        {aside && <aside className="flex-shrink-0 overflow-y-auto sticky top-12">{aside}</aside>}
      </div>
    </div>
  );
}
