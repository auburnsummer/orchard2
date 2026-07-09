
import { Navbar } from "@cafe/components/ui/Navbar";

export function DailyBlendNavbar() {
  const links = [
    {
      label: "Configuration",
      href: `/daily-blend/config/`,
    },
    {
      label: "Random Pools",
      href: `/daily-blend/random-pools/`,
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

  return <Navbar links={links} />;
}
