import { ReactNode } from "react";

import cc from "clsx";

type TableProps = {
  children: ReactNode;
  className?: string;
};

export function Table({ children, className = "" }: TableProps) {
  return (
    <div className={cc("flow-root", className)}>
      <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div className="overflow-hidden shadow-sm outline-1 outline-black/5 sm:rounded-lg dark:shadow-none dark:-outline-offset-1 dark:outline-white/10">
            <table className={`relative min-w-full divide-y divide-gray-300 dark:divide-white/15 ${className}`}>
              {children}
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
