import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";
import { ClubMembership } from "@cafe/types/clubMembership";
import { Modal, Stack, Select, Group, Button } from "@mantine/core";
import { useEffect, useRef, useState } from "react";

type EditMemberFormProps = {
    opened: boolean;
    onClose: () => void;
    membership: ClubMembership | null;
    canEdit: boolean;
    club: Club;
};

export function EditMemberForm({
    opened,
    onClose,
    membership,
    canEdit,
    club
}: EditMemberFormProps) {
    const deleteFormRef = useRef<HTMLFormElement>(null);
    const csrfInput = useCSRFTokenInput();
    const [deleteWarningClicked, setDeleteWarningClicked] = useState(false);

    useEffect(() => {
        if (opened) {
            setDeleteWarningClicked(false);
        }
    }, [opened]);

    return (
        <Modal
            opened={opened}
            onClose={onClose}
            centered
            title={`Editing user ${membership && membership.user.displayName}`}
        >
            {
                membership && (
                    <>
                        <Form
                            action={`/groups/${club.id}/settings/members/${membership.user.id}/delete/`}
                            method="POST"
                            ref={deleteFormRef}
                        >
                            {csrfInput}
                        </Form>
                        <Form
                            action={`/groups/${club.id}/settings/members/${membership.user.id}/edit/`}
                            method="POST"
                        >
                            {csrfInput}
                            <Stack align="start">
                                <Select
                                    label="User role"
                                    disabled={!canEdit}
                                    allowDeselect={false}
                                    defaultValue={membership.role}
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
                                    <Button type="submit" disabled={!canEdit}>Submit</Button>
                                    {
                                        deleteWarningClicked
                                            ? (
                                                <Button
                                                    color="red"
                                                    type="button"
                                                    onClick={() => {
                                                        if (deleteFormRef.current) {
                                                            deleteFormRef.current.requestSubmit();
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
    )
}