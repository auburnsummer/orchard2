import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "../ProfileNavbar/ProfileNavbar";

import styles from "./ProfileSettingsView.module.css";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useLoggedInUser } from "@cafe/hooks/useUser";
import { Form } from "@cafe/minibridge/components/Form";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { TextInput } from "@cafe/components/ui/TextInput";
import Select from "@cafe/components/ui/Select";
import { Button } from "@cafe/components/ui/Button";

export function ProfileSettingsView() {
  const user = useLoggedInUser();
  const input = useCSRFTokenInput();

  return (
    <Shell navbar={<ProfileNavbar />}>
      <Surface className="m-3 p-6 flex-grow">
        <Words as="h2" variant="header">Settings</Words>
        <Form className={styles.base} method="post">
          {input}
          <div className="flex flex-col gap-2">
            <TextInput
              name="display_name"
              label="Display name"
              maxLength={150}
              defaultValue={user.displayName}
              className="max-w-64"
            />

            <Select
              label="Theme"
              className="max-w-64"
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

            <Button type="submit" variant="primary" className="max-w-32 py-2 mt-4">Save</Button>
          </div>
        </Form>
      </Surface>
    </Shell>
  );
}
