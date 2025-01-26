import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "../ClubSettingsNavbar/ClubSettingsNavbar";
import { ClubMembership, ClubMembershipRole } from "@cafe/types/clubMembership";
import { Button, Group, Modal, Select, Stack, Table } from "@mantine/core";

import styles from "./ClubSettingsMembersView.module.css";
import { useRef, useState } from "react";
import { AuthenticatedUser } from "@cafe/hooks/useUser";
import { Form } from "@django-bridge/react";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

type ClubSettingsMembersViewProps = {
    club: Club,
    memberships: ClubMembership[];
    user_role: ClubMembershipRole;
};

export function ClubSettingsMembersView({ club, memberships, user_role }: ClubSettingsMembersViewProps) {

    const [editMemberFormOpen, setEditMemberFormOpen] = useState(false);
    const [membershipBeingEdited, setMembershipBeingEdited] = useState<ClubMembership | null>(null);
    const [deleteWarningClicked, setDeleteWarningClicked] = useState(false);
    const deleteFormRef = useRef<HTMLFormElement>(null);
    const csrfInput = useCSRFTokenInput();

    const rows = memberships.map(membership => (
        <Table.Tr key={membership.user.id}>
            <Table.Td>{membership.user.displayName}</Table.Td>
            <Table.Td>{membership.user.id}</Table.Td>
            <Table.Td className={styles.tableRole}>{membership.role}</Table.Td>
            <Table.Td>
                <Button
                    variant="light"
                    onClick={() => {
                        setDeleteWarningClicked(false);
                        setMembershipBeingEdited(membership);
                        setEditMemberFormOpen(true);
                    }}
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
            <Modal
                opened={editMemberFormOpen}
                onClose={() => setEditMemberFormOpen(false)}
                centered
                title={`Editing user ${membershipBeingEdited && membershipBeingEdited.user.displayName}`}
            >
                {
                    membershipBeingEdited && (
                        <>
                            <Form
                                action={`/groups/${club.id}/settings/members/${membershipBeingEdited.user.id}/delete/`}
                                method="POST"
                                ref={deleteFormRef}
                            >
                                {csrfInput}
                            </Form>
                            <Form
                                action={`/groups/${club.id}/settings/members/${membershipBeingEdited.user.id}/edit/`}
                                method="POST"
                            >
                                {csrfInput}
                                <Stack align="start">
                                    <Select
                                        label="User role"
                                        allowDeselect={false}
                                        defaultValue={membershipBeingEdited.role}
                                        name="role"
                                        data={[
                                            {
                                                label: 'Owner',
                                                value: 'owner'
                                            },
                                            {
                                                label: 'Admin',
                                                value: 'admin'
                                            }
                                        ]}
                                    >
                                    </Select>
                                    <Group>
                                        <Button type="submit">Submit</Button>
                                        {
                                            deleteWarningClicked
                                                ? (
                                                    <Button
                                                        color="red"
                                                        type="button"
                                                        onClick={() => {
                                                            console.log(deleteFormRef.current);
                                                            if (deleteFormRef.current) {
                                                                deleteFormRef.current.submit();
                                                            }
                                                        }}
                                                    >
                                                        Click again to confirm
                                                    
                                                    </Button>
                                                )
                                                : <Button
                                                    type="button"
                                                    color="grey"
                                                    onClick={() => setDeleteWarningClicked(true)}
                                                >
                                                    Delete user
                                                </Button>
                                        }
                                    </Group>
                                </Stack>
                            </Form>
                        </>
                    )
                }
            </Modal>
            <Stack align="start">
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
                <Button>
                    Add member
                </Button>
            </Stack>
        </Shell>
    )
}