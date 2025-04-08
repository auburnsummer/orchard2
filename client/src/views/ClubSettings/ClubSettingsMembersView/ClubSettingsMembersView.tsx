import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "../ClubSettingsNavbar/ClubSettingsNavbar";
import { ClubMembership } from "@cafe/types/clubMembership";
import { ActionIcon, Alert, Button, CopyButton, Group, Stack, Table, Text, TextInput, Tooltip } from "@mantine/core";

import styles from "./ClubSettingsMembersView.module.css";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faCopy } from "@fortawesome/free-solid-svg-icons";
import { AddMemberForm } from "./AddMemberForm/AddMemberForm";
import { EditMemberForm } from "./EditMemberForm/EditMemberForm";
import { useAtomValue } from "jotai";
import { locationAtom } from "@cafe/minibridge/atoms";

type MembershipPermission = {
    can_change: boolean;
    can_delete: boolean;
}

type ClubSettingsMembersViewProps = {
    club: Club,
    memberships: {
        membership: ClubMembership,
        permissions: MembershipPermission
    }[];
    can_add: boolean;
};

export function ClubSettingsMembersView({ club, memberships, can_add }: ClubSettingsMembersViewProps) {
    const [editMemberFormOpen, setEditMemberFormOpen] = useState(false);
    const [membershipBeingEdited, setMembershipBeingEdited] = useState<ClubMembership | null>(null);
    const [addMemberFormOpen, setAddMemberFormOpen] = useState(false);
    const { searchParams } = useAtomValue(locationAtom);

    const inviteCode = searchParams && searchParams.get("invite_code")
    const inviteUrl = new URL(`/groups/redeem_invite/${inviteCode}/`, window.location.origin).toString();

    const rows = memberships.map(({membership, permissions}) => (
        <Table.Tr key={membership.user.id}>
            <Table.Td>{membership.user.displayName}</Table.Td>
            <Table.Td className={styles.tableId}>{membership.user.id}</Table.Td>
            <Table.Td className={styles.tableRole}>{membership.role}</Table.Td>
            <Table.Td>
                <Button
                    variant="light"
                    onClick={() => {
                        setMembershipBeingEdited(membership);
                        setEditMemberFormOpen(true);
                    }}
                    disabled={!permissions.can_change && !permissions.can_delete}
                >
                    Edit
                </Button>
            </Table.Td>
        </Table.Tr>
    ))

    return (
        <Shell
            navbar={<ClubSettingsNavbar club={club} />}
        >
            <EditMemberForm
                opened={editMemberFormOpen}
                onClose={() => setEditMemberFormOpen(false)}
                membership={membershipBeingEdited}
                canEdit={memberships.find(m => m.membership.user === membershipBeingEdited?.user)?.permissions.can_change || false}
                club={club}
            />
            <AddMemberForm
                club={club}
                opened={addMemberFormOpen}
                onClose={() => setAddMemberFormOpen(false)}
            />
            <Stack align="start">
                {
                    inviteCode && (
                        <Alert className={styles.inviteBox} variant="light" color="blue" title="Here is the invite link">
                            <Stack>
                                <Text size="sm">Send this link to the person you want to invite.</Text>
                                <Group>
                                    <TextInput
                                        onFocus={e => e.target.select()}
                                        disabled={false}
                                        value={inviteUrl}
                                        readOnly
                                    >

                                    </TextInput>
                                    <CopyButton value={inviteUrl}>
                                        {({ copied, copy }) => (
                                            <Tooltip label={copied ? 'Copied' : 'Copy'} withArrow position="right">
                                                <ActionIcon color={copied ? 'teal' : 'gray'} variant="subtle" onClick={copy}>
                                                    {copied ?  <FontAwesomeIcon icon={faCheck} /> : <FontAwesomeIcon icon={faCopy} />}
                                                </ActionIcon>
                                            </Tooltip>
                                        )}
                                    </CopyButton>
                                </Group>
                            </Stack>
                        </Alert>
                    )
                }
                <h2>Members of {club.name}</h2>
                <Table>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>User</Table.Th>
                            <Table.Th>ID</Table.Th>
                            <Table.Th>Role</Table.Th>
                            <Table.Th>Edit</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>{rows}</Table.Tbody>
                </Table>
                <Button
                    onClick={() => setAddMemberFormOpen(true)}
                    disabled={!can_add}
                >
                    Add member
                </Button>
            </Stack>
        </Shell>
    )
}