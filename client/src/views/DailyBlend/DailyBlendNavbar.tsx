
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";
import { Surface } from "@cafe/components/ui/Surface";
import { NavEntry } from "@cafe/components/ui/NavEntry";

export function DailyBlendNavbar() {
  const { pathname } = useAtomValue(locationAtom);

  const links = [
    {
      label: "Configuration",
      href: `/daily-blend/config/`,
    },
    {
      label: "Random Pool",
      href: `/daily-blend/random-pool/`,
    },
    {
      label: "Scheduled Blends",
      href: `/daily-blend/schedule/`,
    },
    {
      label: "Blend Now!!",
      href: `/daily-blend/blend-now/`,
    },
  ];

  return (
    <Surface className="flex-grow m-3 flex flex-col gap-1">
      <div className="flex flex-col mt-4">
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
    </Surface>
  );
}
