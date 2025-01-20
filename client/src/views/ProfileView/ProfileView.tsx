import { Shell } from '@cafe/components/Shell';
import { Avatar, Group, NavLink, Stack, Text } from '@mantine/core';
import { useLoggedInUser } from '@cafe/hooks/useUser';

import styles from './ProfileView.module.css';
import { useNavigationContext } from '@cafe/hooks/useNavigationContext';
import { ProfileSubpage } from './ProfileSubpage/ProfileSubpage';
import { SettingsSubpage } from './SettingsSubpage/SettingsSubpage';
import { Spacer } from '@cafe/components/Spacer/Spacer';
import { GroupsSubpage, GroupsSubpageProps } from './GroupsSubpage/GroupsSubpage';
import { Link } from '@cafe/components/Link/Link';

function ProfileNavbar(){
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
        },
        {
            label: "Groups",
            href: "/accounts/profile/groups/"
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
            <Text c="dimmed" className={styles.navbarId}>Your ID: { user.id }</Text>
        </Stack>
    );
}

type ProfileSubpageProps = {
    subpage: 'profile'
};

type SettingSubpageProps = {
    subpage: 'settings'
}

type ProfileViewProps = ProfileSubpageProps | SettingSubpageProps | GroupsSubpageProps;

export function ProfileView(props: ProfileViewProps) {
    let content = <></>;

    if (props.subpage === 'profile') {
        content = <ProfileSubpage />;
    }
    if (props.subpage === 'settings') {
        content = <SettingsSubpage />;
    }

    if (props.subpage === 'groups') {
        content = <GroupsSubpage {...props} />;
    }

    return (
        <Shell
            navbar={<ProfileNavbar />}
        >
            <div className={styles.mainArea}>
                { content }
            </div>
        </Shell>
    );
}
  