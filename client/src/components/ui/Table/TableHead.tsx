import { ReactNode } from "react";

type TableHeadProps = {
  children: ReactNode;
  className?: string;
};

export function TableHead({ children, className = "" }: TableHeadProps) {
  return (
    <thead className={`bg-gray-50 dark:bg-gray-800/75 ${className}`}>
      {children}
    </thead>
  );
}
