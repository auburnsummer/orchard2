import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import styles from "./CreateClubForm.module.css";
import { Form } from "@cafe/minibridge/components/Form";
import { TextInput } from "../ui/TextInput";
import { Button } from "../ui/Button";

type CreateClubFormProps = {
  redirectTo?: string;
  onSubmit?: () => void;
};

export function CreateClubForm({
  redirectTo,
  onSubmit
}: CreateClubFormProps) {
  const csrfInput = useCSRFTokenInput();

  return (
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
      <div className="flex flex-col gap- items-start">
        <TextInput
          name="name"
          label="Group name"
          description="You can change this at any time."
        />
        <Button type="submit" variant="primary" className="mt-4">Create group</Button>
      </div>
    </Form>
  );
}
