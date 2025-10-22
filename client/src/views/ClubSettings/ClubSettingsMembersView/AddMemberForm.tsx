import { Button } from "@cafe/components/ui/Button";
import Select from "@cafe/components/ui/Select";
import { Words } from "@cafe/components/ui/Words";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";

type AddMemberFormProps = {
  onSubmit?: () => void;
  club: Club;
};

export function AddMemberForm({
  club,
  onSubmit,
}: AddMemberFormProps) {
  const csrfInput = useCSRFTokenInput();

  return (
    <div className="flex flex-col gap-1">
      <Words as="p">
        Clicking the button will generate an invite link. Send the invite link
        to the person you wish to invite.
      </Words>
      <Words as="p" className="font-semibold">The link will expire in 24 hours.</Words>
      <Form
        method="post"
        action={`/groups/${club.id}/settings/members/invite/`}
        onSubmit={onSubmit}
      >
        {csrfInput}
        <div className="lex flex-col gap-1">
          <Select
            className="mt-4"
            defaultValue="admin"
            allowDeselect={false}
            label="Role for invited member"
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
          <Button type="submit" variant="primary" className="mt-8 w-32">Create link</Button>
        </div>
      </Form>
    </div>
  );
}
