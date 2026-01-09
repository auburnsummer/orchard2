import { ReactNode } from "react";

type TableCellProps = {
  children: ReactNode;
  className?: string;
  align?: "left" | "center" | "right";
  firstColumn?: boolean;
  lastColumn?: boolean;
};

export function TableCell({
  children,
  className = "",
  align = "left",
  firstColumn = false,
  lastColumn = false,
}: TableCellProps) {
  const alignClass = align === "right" ? "text-right" : align === "center" ? "text-center" : "text-left";
  const paddingClass = firstColumn
    ? "py-4 pr-3 pl-4 sm:pl-6"
    : lastColumn
    ? "py-4 pr-4 pl-3 sm:pr-6"
    : "px-3 py-4";

  return (
    <td className={`${paddingClass} ${alignClass} text-sm whitespace-nowrap ${className}`}>
      {children}
    </td>
  );
}
