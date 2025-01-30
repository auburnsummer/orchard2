import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import styles from "./CreateClubForm.module.css";
import { Form } from "@django-bridge/react";
import { Stack, TextInput, Button, Modal } from "@mantine/core";

type CreateClubFormProps = {
    redirectTo?: string;
    opened: boolean;
    onClose: () => void;
}

export function CreateClubForm({redirectTo, opened, onClose}: CreateClubFormProps) {
    const csrfInput = useCSRFTokenInput();

    return (
        <Modal
            opened={opened}
            onClose={onClose}
            centered
            title="Create group"
        >
            <Form action="/groups/create/" method="POST" className={styles.base}>
                {csrfInput}
                {
                    redirectTo && (
                        <input type="hidden" name="redirect" value={redirectTo} />
                    )
                }
                <Stack
                    align="start"
                >
                    <TextInput
                        name="name"
                        label="Group name"
                        description="You can change this at any time."
                    />
                    <Button type="submit">Create group</Button>
                </Stack>
            </Form>
        </Modal>
    )
    
}