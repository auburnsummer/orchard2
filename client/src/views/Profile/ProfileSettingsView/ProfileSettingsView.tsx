import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "../ProfileNavbar/ProfileNavbar";

import styles from "./ProfileSettingsView.module.css";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Stack, Select, Button } from "@mantine/core";
import { useLoggedInUser } from "@cafe/hooks/useUser";
import { Form } from "@cafe/minibridge/components/Form";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { TextInput } from "@cafe/components/ui/TextInput";

export function ProfileSettingsView() {
  const user = useLoggedInUser();
  const input = useCSRFTokenInput();

  return (
    <Shell navbar={<ProfileNavbar />}>
      <Surface className="m-3 p-6 flex-grow">
        <Words as="h2" variant="header">Settings</Words>
        <Form className={styles.base} method="post">
          {input}
          <div className="flex flex-col gap-4">
            <TextInput
              name="display_name"
              label="Display name"
              maxLength={150}
              defaultValue={user.displayName}
              className="max-w-48"
            />

            <Select
              label="Theme"
              allowDeselect={false}
              defaultValue={user.theme_preference}
              name="theme_preference"
              data={[
                {
                  label: "Light",
                  value: "light",
                },
                {
                  label: "Dark",
                  value: "dark",
                },
              ]}
            />

            <Button type="submit">Save</Button>
          </div>
        </Form>
      </Surface>
    </Shell>
  );
}
