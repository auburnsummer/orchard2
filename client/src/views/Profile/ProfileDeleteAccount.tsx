import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "./ProfileNavbar";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { Form } from "@cafe/minibridge/components/Form";
import { Radio } from "@cafe/components/ui/Radio";
import { Button } from "@cafe/components/ui/Button";
import { Alert } from "@cafe/components/ui/Alert";
import React from "react";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

type ProfileDeleteAccountProps = {
    number_of_levels: number;
    number_of_clubs: number;
};

export function ProfileDeleteAccount(props: ProfileDeleteAccountProps) {
  const csrfInput = useCSRFTokenInput();
  let content: React.ReactNode;
  if (props.number_of_clubs > 0) {
    content = (
      <Alert variant="error" className="mt-4">
        You are currently the owner of {props.number_of_clubs} group(s).
        You cannot delete your account while you own groups. Please transfer ownership or delete your groups before proceeding.
      </Alert>
    );
  }
  else if (props.number_of_levels > 0) {
    content = (
      <div>
        <Words as="p">
          You have {props.number_of_levels} level(s) associated with your account.
        </Words>
        <Words className="mt-4">
          What would you like to do with them?
        </Words>
        <Form className="pt-4" method="post">
          {csrfInput}
          <div className="flex flex-col gap-2">
            <Radio
              name="level_handling"
              label="Delete all my levels"
              value="delete"
            />
            <Radio
              name="level_handling"
              label="Keep the levels (ownership will be transferred to 'Deleted User')"
              value="transfer"
              defaultChecked
            />
            <Button type="submit" variant="danger" className="max-w-32 py-2 mt-4">Delete Account</Button>
          </div>
        </Form>
      </div>
    );
  }

  // No levels
  else if (!content) {
    content = (
      <div>
        <Words as="p">
          Are you sure you want to delete your account? This action cannot be undone.
        </Words>
        <Form className="pt-4" method="post">
          {csrfInput}
          {/* which doesn't matter since there are no levels to handle */}
          <input type="hidden" name="level_handling" value="transfer" />
          <Button type="submit" variant="danger" className="max-w-32 py-2 mt-4">Delete Account</Button>
        </Form>
      </div>
    );
  }

  return (
    <Shell navbar={<ProfileNavbar />}>
      <Surface className="m-3 p-6 flex-grow">
        <Words as="h2" variant="header">Delete Account</Words>
        {content}
      </Surface>
    </Shell>
  );
}
