import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";
import { ClubMembership } from "@cafe/types/clubMembership";
import { Stack, Select, Group, Button } from "@mantine/core";
import { useRef, useState } from "react";

type EditMemberFormProps = {
  onSubmit?: () => void;
  membership: ClubMembership | null;
  canEdit: boolean;
  club: Club;
};

export function EditMemberForm({
  onSubmit,
  membership,
  canEdit,
  club,
}: EditMemberFormProps) {
  const deleteFormRef = useRef<HTMLFormElement>(null);
  const csrfInput = useCSRFTokenInput();
  const [deleteWarningClicked, setDeleteWarningClicked] = useState(false);

  return (
    <div>
      {membership && (
        <>
          <Form
            action={`/groups/${club.id}/settings/members/${membership.user.id}/delete/`}
            method="POST"
            ref={deleteFormRef}
            onSubmit={onSubmit}
          >
            {csrfInput}
          </Form>
          <Form
            action={`/groups/${club.id}/settings/members/${membership.user.id}/edit/`}
            method="POST"
            onSubmit={onSubmit}
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
                    label: "Owner",
                    value: "owner",
                  },
                  {
                    label: "Admin",
                    value: "admin",
                  },
                ]}
              ></Select>
              <Group>
                <Button type="submit" disabled={!canEdit}>
                  Submit
                </Button>
                {deleteWarningClicked ? (
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
                ) : (
                  <Button
                    type="button"
                    color="grey"
                    onClick={() => setDeleteWarningClicked(true)}
                  >
                    Delete user
                  </Button>
                )}
              </Group>
            </Stack>
          </Form>
        </>
      )}
    </div>
  );
}
