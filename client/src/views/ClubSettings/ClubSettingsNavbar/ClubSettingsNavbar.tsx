import { Spacer } from "@cafe/components/Spacer/Spacer";
import { useNavigationContext, usePathName } from "@cafe/hooks/useNavigationContext";
import { Stack, Group,  NavLink, Text } from "@mantine/core";
import styles from "./ClubSettingsNavbar.module.css";
import { Link } from "@django-bridge/react";
import { Club } from "@cafe/types/club";

type ClubSettingsNavbarProps = {
    club: Club
}

export function ClubSettingsNavbar({club}: ClubSettingsNavbarProps){
    const path = usePathName();

    const links = [
        {
            label: "Settings",
            href: `/groups/${club.id}/settings/`
        },
        {
            label: "Members",
            href: `/groups/${club.id}/settings/members/`
        },
        {
            label: "Connected Discord servers",
            href: `/groups/${club.id}/settings/connections/discord/`
        }
    ]

    return (
        <Stack className={styles.navbarBase}>
            <Group className={styles.navbarTitle}>
                <h2>{club.name}</h2>
            </Group>
            <Stack className={styles.navbarLinks} gap={0}>
                {
                    links.map(link => (
                        <NavLink
                            key={link.href}
                            component={Link}
                            skipDirtyFormCheck={true}
                            href={link.href}
                            label={link.label}
                            active={path === link.href}
                        />
                    ))
                }
            </Stack>
            <Spacer />
            <Text c="dimmed" className={styles.navbarId}>Club ID: { club.id }</Text>
        </Stack>
    );
}
