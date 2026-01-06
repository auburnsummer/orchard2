import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter";
import { Button } from "@cafe/components/ui/Button";
import { Checkbox } from "@cafe/components/ui/Checkbox";
import Select from "@cafe/components/ui/Select";
import { Words } from "@cafe/components/ui/Words";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { useState } from "react";

type LevelAddTypeSelectProps = {
  code: string;
  code_valid: boolean;
};

export function LevelAddTypeSelect({
  code: _code,
  code_valid,
}: LevelAddTypeSelectProps) {
  const [addType, setAddType] = useState<string | undefined>(undefined);
  const csrfInput = useCSRFTokenInput();

  const selectData = [
    { value: "new", label: "New Level" },
    { value: "update", label: "Update Existing Level" },
  ];

  const content = code_valid ? (
    <Form method="POST">
      {csrfInput}
      <div className="flex flex-col gap-4">
        <Select
          value={addType}
          label="Is this a new level or an update to an existing level?"
          data={selectData}
          onChange={setAddType}
          name="prefill_type"
        ></Select>
        {
          addType === "new" && (
            <Checkbox
              name="go_to_prepost"
              label="Edit level metadata before posting"
            />
          )
        }
        <Button type="submit" variant="primary" disabled={addType == undefined} className="mt-4">
          Continue
        </Button>
      </div>
    </Form>
  ) : (
    <>
      <Words as="p">This link to add a level is invalid or has expired.</Words>
      <Words as="p">Please run the command again to get a fresh link.</Words>
    </>
  );

  return (
    <ShellDramaticCenter>
      {content}
    </ShellDramaticCenter>
  );
}
