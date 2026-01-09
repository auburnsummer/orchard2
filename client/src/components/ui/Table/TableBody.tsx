import { ReactNode } from "react";

type TableBodyProps = {
  children: ReactNode;
  className?: string;
};

export function TableBody({ children, className = "" }: TableBodyProps) {
  return (
    <tbody className={`divide-y divide-gray-200 bg-white dark:divide-white/10 dark:bg-gray-800/50 ${className}`}>
      {children}
    </tbody>
  );
}
