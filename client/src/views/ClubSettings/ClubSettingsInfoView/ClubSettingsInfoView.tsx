import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "../ClubSettingsNavbar";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Button } from "@cafe/components/ui/Button";

type ClubSettingsInfoViewProps = {
  club: Club;
  can_edit: boolean;
};

export function ClubSettingsInfoView({
  club,
  can_edit: canEdit,
}: ClubSettingsInfoViewProps) {
  const input = useCSRFTokenInput();

  return (
    <Shell navbar={<ClubSettingsNavbar club={club} />}>
      <Surface className="m-3 p-6 flex-grow">
        <Words as="h2" variant="header">Group {club.name} settings</Words>
        <Form className="pt-2" method="post">
          {input}
          <div className="flex flex-col gap-2">
            <TextInput
              name="name"
              label="Group name"
              defaultValue={club.name}
              disabled={!canEdit}
              className="max-w-64"
            />

            <Button 
              type="submit" 
              variant="primary" 
              disabled={!canEdit}
              title={!canEdit ? "You have to be an owner of the group to edit." : undefined}
              className="max-w-32 py-2 mt-4"
            >
              Save
            </Button>
          </div>
        </Form>
      </Surface>
    </Shell>
  );
}
