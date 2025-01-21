import { Club } from "@cafe/types/club"
import { Anchor, Button, List, Modal, Overlay, Stack, Title } from "@mantine/core";

import styles from "./GroupsSubpage.module.css";
import { useNavigationContext } from "@cafe/hooks/useNavigationContext";
import { Link } from "@cafe/components/Link/Link";

export type GroupsSubpageProps = {
    subpage: 'groups',
    clubs: {
        club: Club,
        role: 'owner' | 'admin'
    }[];
}

function LinkToClub({ club }: { club: Club }) {
    return <Anchor component={Link} href={`/groups/${club.id}/settings/`}>{club.name}</Anchor>
}

export function GroupsSubpage({ clubs }: GroupsSubpageProps) {
    const navigation = useNavigationContext();

    const ownerClubs = clubs.filter(c => c.role === 'owner');
    const adminClubs = clubs.filter(c => c.role === 'admin');

    return (
        <Stack className={styles.base} align="start">
            <Title order={2}>Groups</Title>
            {
                ownerClubs.length > 0 && (
                    <>
                        <Title order={3}>Owner</Title>
                        <List>
                            {
                                ownerClubs.map(c => (
                                    <List.Item key={c.club.id}>
                                        <LinkToClub club={c.club} />
                                    </List.Item>
                                ))
                            }
                        </List>
                    </>
                )
            }
            {
                adminClubs.length > 0 && (
                    <>
                        <Title order={3}>Admin</Title>
                        <List>
                            {
                                adminClubs.map(c => (
                                    <List.Item>
                                        <LinkToClub club={c.club} />
                                    </List.Item>
                                ))
                            }
                        </List>
                    </>
                )
            }
            <Button
                onClick={() => navigation.openOverlay("/groups/create/", (content) => {
                    return (
                        <div
                        >
                            { content }
                        </div>
                    )
                })}
            >
                Create group
            </Button>
        </Stack>
    )
}