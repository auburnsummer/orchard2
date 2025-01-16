import { Button, Group, Stack, TextInput } from "@mantine/core"

import styles from './SettingsSubpage.module.css';
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useLoggedInUser } from "@cafe/hooks/useUser";

export function SettingsSubpage() {
    const input = useCSRFTokenInput();
    const user = useLoggedInUser();

    return (
        <>
            <h2>Settings</h2>
            <form className={styles.base} method="post">
                { input }
                <Stack align="flex-start" gap="1rem">
                    <TextInput
                        name="display_name"
                        label="Display name"
                        defaultValue={user.displayName}
                    />
                    <Button type="submit">Save</Button>
                </Stack>
            </form>
        </>
    )
}