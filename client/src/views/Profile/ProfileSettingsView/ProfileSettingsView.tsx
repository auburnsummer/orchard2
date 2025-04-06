import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "../ProfileNavbar/ProfileNavbar";

import styles from "./ProfileSettingsView.module.css";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Stack, TextInput, Select, Button } from "@mantine/core";
import { useLoggedInUser } from "@cafe/hooks/useUser";

export function ProfileSettingsView() {
    const user = useLoggedInUser();
    const input = useCSRFTokenInput();

    return (
        <Shell
            navbar={<ProfileNavbar />}
        >
            <h2>Settings</h2>
            <form className={styles.base} method="post">
                { input }
                <Stack align="flex-start" gap="1rem">
                    <TextInput
                        name="display_name"
                        label="Display name"
                        defaultValue={user.displayName}
                    />

                <Select
                    label="Theme"
                    allowDeselect={false}
                    defaultValue={user.theme_preference}
                    name="theme_preference"
                    data={[
                        {
                            'label': 'Light',
                            'value': 'light'
                        },
                        {
                            'label': 'Dark',
                            'value': 'dark'
                        }
                    ]}
                />

                    <Button type="submit">Save</Button>
                </Stack>
            </form>
        </Shell>
    );
}