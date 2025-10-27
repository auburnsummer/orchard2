import cc from "clsx";

import { ReactNode, useMemo } from "react";

const formatter = new Intl.ListFormat("en", {
  style: "short",
  type: "conjunction",
});

type ConjunctionListProps = React.HTMLAttributes<HTMLUListElement> & {
  items: string[];
  elementRender: (v: string) => ReactNode;
  literalRender: (v: string) => ReactNode;
};

export function ConjunctionList({
  className,
  items,
  elementRender,
  literalRender,
  ...rest
}: ConjunctionListProps) {
  const fragments = useMemo(() => {
    const formatted = formatter.formatToParts(items);
    return formatted;
  }, [items]);

  return (
    <ul className={cc(className, "flex flex-row items-center")} {...rest}>
      {fragments.map((f) => (
        <li>
          {f.type === "element"
            ? elementRender(f.value)
            : literalRender(f.value)}
        </li>
      ))}
    </ul>
  );
}
