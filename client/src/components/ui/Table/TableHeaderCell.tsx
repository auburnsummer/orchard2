import { ReactNode } from "react";

type TableHeaderCellProps = {
  children: ReactNode;
  className?: string;
  scope?: "col" | "row";
  align?: "left" | "center" | "right";
  firstColumn?: boolean;
  lastColumn?: boolean;
};

export function TableHeaderCell({
  children,
  className = "",
  scope = "col",
  align = "left",
  firstColumn = false,
  lastColumn = false,
}: TableHeaderCellProps) {
  const alignClass = align === "right" ? "text-right" : align === "center" ? "text-center" : "text-left";
  const paddingClass = firstColumn
    ? "py-3.5 pr-3 pl-4 sm:pl-6"
    : lastColumn
    ? "py-3.5 pr-4 pl-3 sm:pr-6"
    : "px-3 py-3.5";

  return (
    <th
      scope={scope}
      className={`${paddingClass} ${alignClass} text-sm font-semibold text-gray-900 dark:text-gray-200 ${className}`}
    >
      {children}
    </th>
  );
}
