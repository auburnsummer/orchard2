import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";
import { Button, Modal, Select, Stack } from "@mantine/core";

type AddMemberFormProps = {
  opened: boolean;
  onClose: () => void;
  onSubmit?: () => void;
  club: Club;
};

export function AddMemberForm({
  opened,
  club,
  onClose,
  onSubmit = onClose,
}: AddMemberFormProps) {
  const csrfInput = useCSRFTokenInput();

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      centered
      title="Create invite to group"
    >
      <p>
        Clicking the button will generate an invite link. Send the invite link
        to the person you wish to invite.
      </p>
      <p>The link will expire in 24 hours.</p>
      <Form
        method="post"
        action={`/groups/${club.id}/settings/members/invite/`}
        onSubmit={onSubmit}
      >
        {csrfInput}
        <Stack align="start">
          <Select
            defaultValue="admin"
            allowDeselect={false}
            data={[
              {
                label: "Owner",
                value: "owner",
              },
              {
                label: "Admin",
                value: "admin",
              },
            ]}
            name="role"
          ></Select>
          <Button type="submit">Create link</Button>
        </Stack>
      </Form>
    </Modal>
  );
}
