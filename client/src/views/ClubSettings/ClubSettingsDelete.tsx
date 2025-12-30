import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "./ClubSettingsNavbar";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { Form } from "@cafe/minibridge/components/Form";
import { Button } from "@cafe/components/ui/Button";
import { Radio } from "@cafe/components/ui/Radio";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

type ClubSettingsInfoViewProps = {
  club: Club;
  club_level_count: number;
};

export function ClubSettingsDeleteView({
  club,
  club_level_count,
}: ClubSettingsInfoViewProps) {
  const csrfInput = useCSRFTokenInput();

  return (
    <Shell navbar={<ClubSettingsNavbar club={club} />}>
      <Surface className="m-3 flex-grow p-6">
        <Words as="h2" variant="header">
          Delete Group {club.name}
        </Words>
        {club_level_count > 0 ? (
          <div>
            <Words className="pt-4" as="p">
              There are {club_level_count} levels associated with this group.
            </Words>
            <Words as="p">What would you like to do with these levels?</Words>
            <Form method="post" className="flex flex-col gap-4 pt-4">
              {csrfInput}
              <Radio
                name="level_action"
                value="delete"
                defaultChecked
                description="Delete all levels in the group."
              >
              </Radio>
              <Radio
                name="level_action"
                value="disassociate"
                description="Disassociate all levels from this group (they will go to the Anonymous group)."
              >

              </Radio>
              <Button type="submit" variant="danger">
                Delete Group
              </Button>
            </Form>
          </div>
        ) : (
          <Words className="pt-4" variant="muted">
            Are you sure you want to delete this group? This action cannot be
            undone.
            <Form method="post" className="pt-4">
              {csrfInput}
              <input type="hidden" name="level_action" value="delete" />
              <Button type="submit" variant="danger">
                Delete Group
              </Button>
            </Form>
          </Words>
        )}
      </Surface>
    </Shell>
  );
}
