import { Spacer } from "@cafe/components/Spacer/Spacer";
import { useLoggedInUser } from "@cafe/hooks/useUser";
import { Stack, Group, Avatar, NavLink, Text } from "@mantine/core";
import styles from "./ProfileNavbar.module.css";
import { Link } from "@cafe/minibridge/components/Link";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";

export function ProfileNavbar() {
  const user = useLoggedInUser();
  const { pathname } = useAtomValue(locationAtom);

  const links = [
    {
      label: "Profile",
      href: "/accounts/profile/",
    },
    {
      label: "Settings",
      href: "/accounts/profile/settings/",
    },
    {
      label: "Groups",
      href: "/accounts/profile/groups/",
    },
  ];

  return (
    <Stack className={styles.navbarBase}>
      <Group className={styles.navbarTitle}>
        <Avatar size="lg" src={user.avatarURL} />
        <h2>{user.displayName}</h2>
      </Group>
      <Stack className={styles.navbarLinks} gap={0}>
        {links.map((link) => (
          <NavLink
            key={link.href}
            component={Link}
            href={link.href}
            label={link.label}
            active={pathname === link.href}
          />
        ))}
      </Stack>
      <Spacer />
      <Text c="dimmed" className={styles.navbarId}>
        User ID: {user.id}
      </Text>
    </Stack>
  );
}
