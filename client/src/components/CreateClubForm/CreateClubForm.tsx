import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import styles from "./CreateClubForm.module.css";
import { Form } from "@django-bridge/react";
import { Stack, TextInput, Button } from "@mantine/core";

type CreateClubFormProps = {
    redirectTo?: string;
}

export function CreateClubForm({redirectTo}: CreateClubFormProps) {
    const csrfInput = useCSRFTokenInput();

    return (
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
    )
    
}