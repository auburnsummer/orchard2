import { ReactNode } from "react";

type TableRowProps = {
  children: ReactNode;
  className?: string;
};

export function TableRow({ children, className = "" }: TableRowProps) {
  return <tr className={className}>{children}</tr>;
}
