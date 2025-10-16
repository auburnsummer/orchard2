import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import styles from "./CreateClubForm.module.css";
import { Stack, TextInput, Button, Modal } from "@mantine/core";
import { Form } from "@cafe/minibridge/components/Form";

type CreateClubFormProps = {
  redirectTo?: string;
  opened: boolean;
  onClose: () => void;
  onSubmit?: () => void;
};

export function CreateClubForm({
  redirectTo,
  opened,
  onClose,
  onSubmit = onClose,
}: CreateClubFormProps) {
  const csrfInput = useCSRFTokenInput();

  return (
    <Modal opened={opened} onClose={onClose} centered title="Create group">
      <Form
        action="/groups/create/"
        method="POST"
        className={styles.base}
        onSubmit={onSubmit}
      >
        {csrfInput}
        {redirectTo && (
          <input type="hidden" name="redirect" value={redirectTo} />
        )}
        <Stack align="start">
          <TextInput
            name="name"
            label="Group name"
            description="You can change this at any time."
          />
          <Button type="submit">Create group</Button>
        </Stack>
      </Form>
    </Modal>
  );
}
