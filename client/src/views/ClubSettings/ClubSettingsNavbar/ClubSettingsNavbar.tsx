import { Spacer } from "@cafe/components/Spacer/Spacer";
import { Stack, Group,  NavLink, Text } from "@mantine/core";
import styles from "./ClubSettingsNavbar.module.css";
import { Club } from "@cafe/types/club";
import { Link } from "@cafe/minibridge/components/Link";
import { useLocation } from "@cafe/minibridge/hooks";

type ClubSettingsNavbarProps = {
    club: Club
}

export function ClubSettingsNavbar({club}: ClubSettingsNavbarProps){
    const [{ pathname }] = useLocation();

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
                            href={link.href}
                            label={link.label}
                            active={pathname === link.href}
                        />
                    ))
                }
            </Stack>
            <Spacer />
            <Text c="dimmed" className={styles.navbarId}>Club ID: { club.id }</Text>
        </Stack>
    );
}
