import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Button, Stack, TextInput } from "@mantine/core";

import styles from "./CreateClub.module.css";

export function CreateClubView() {
    const csrfInput = useCSRFTokenInput();

    return (
        <form action="/groups/create/" method="POST" className={styles.base}>
            {csrfInput}
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
        </form>
    )
}