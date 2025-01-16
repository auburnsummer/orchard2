import { Shell } from '@cafe/components/Shell';
import { Avatar, Group, NavLink, Stack, Text } from '@mantine/core';
import { Link } from "@django-bridge/react";
import { useLoggedInUser } from '@cafe/hooks/useUser';

import styles from './ProfileView.module.css';
import { useNavigationContext } from '@cafe/hooks/useNavigationContext';
import { ProfileSubpage } from '../ProfileSubpage/ProfileSubpage';
import { SettingsSubpage } from '../SettingsSubpage/SettingsSubpage';
import { Spacer } from '@cafe/components/Spacer/Spacer';

function ProfileNavbar( ){
    const user = useLoggedInUser();
    const { path } = useNavigationContext();

    const links = [
        {
            label: "Profile",
            href: "/accounts/profile/"
        },
        {
            label: "Settings",
            href: "/accounts/profile/settings/"
        }
    ]

    return (
        <Stack className={styles.navbarBase}>
            <Group className={styles.navbarTitle}>
                <Avatar size="lg" src={user.avatarURL} />
                <h2>{ user.displayName }</h2>
            </Group>
            <Stack className={styles.navbarLinks} gap={0}>
                {
                    links.map(link => (
                        <NavLink key={link.href} component={Link} href={link.href} label={link.label} active={path === link.href} />
                    ))
                }
            </Stack>
            <Spacer />
            <Text c="dimmed" className={styles.navbarId}>Your ID: { user.id }</Text>
        </Stack>
    );
}

type ProfileViewProps = {
    subpage: 'profile' | 'settings'
}

export function ProfileView({subpage}: ProfileViewProps) {
    const page = {
        profile: <ProfileSubpage />,
        settings: <SettingsSubpage />
    }
    return (
        <Shell
            navbar={<ProfileNavbar />}
        >
            <div className={styles.mainArea}>
                { page[subpage] }
            </div>
        </Shell>
    );
}
  