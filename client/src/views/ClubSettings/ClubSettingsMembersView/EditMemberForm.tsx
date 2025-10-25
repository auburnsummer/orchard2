import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";
import { ClubMembership } from "@cafe/types/clubMembership";
import Select from "@cafe/components/ui/Select";
import { Button } from "@cafe/components/ui/Button";
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
            <div className="flex flex-col items-start gap-4">
              <Select
                className="w-32"
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
              />
              <div className="flex gap-2 mt-4">
                <Button type="submit" disabled={!canEdit} variant="primary">
                  Submit
                </Button>
                {deleteWarningClicked ? (
                  <Button
                    variant="danger"
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
                    variant="default"
                    onClick={() => setDeleteWarningClicked(true)}
                  >
                    Remove member from group
                  </Button>
                )}
              </div>
            </div>
          </Form>
        </>
      )}
    </div>
  );
}
