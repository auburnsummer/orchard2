import cc from "clsx";
import { useAtomValue } from "jotai";

import { Surface } from "@cafe/components/ui/Surface";
import { NavEntry } from "@cafe/components/ui/NavEntry";
import { Link } from "@cafe/minibridge/components/Link";
import { locationAtom } from "@cafe/minibridge/atoms";

export type NavbarLink = {
  label: React.ReactNode;
  href: string;
};

type NavbarProps = {
  links: NavbarLink[];
  beforeLinks?: React.ReactNode;
  afterLinks?: React.ReactNode;
  className?: string;
  linksClassName?: string;
};

export function Navbar({
  links,
  beforeLinks,
  afterLinks,
  className,
  linksClassName,
}: NavbarProps) {
  const { pathname } = useAtomValue(locationAtom);

  return (
    <Surface className={cc("m-3 flex-grow flex flex-col", className)}>
      {beforeLinks}
      <div className={cc("flex flex-col", linksClassName)}>
        {links.map((link) => (
          <NavEntry
            key={link.href}
            as={Link}
            href={link.href}
            active={pathname === link.href}
          >
            {link.label}
          </NavEntry>
        ))}
      </div>
      {afterLinks}
    </Surface>
  );
}
