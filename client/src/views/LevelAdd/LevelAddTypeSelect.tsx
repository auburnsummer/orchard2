import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter";
import { Button } from "@cafe/components/ui/Button";
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
      <div className="flex flex-col">
        <Select
          value={addType}
          label="Is this a new level or an update to an existing level?"
          data={selectData}
          onChange={setAddType}
          name="prefill_type"
        ></Select>
        <Button type="submit" variant="primary" disabled={addType == undefined} className="mt-8">
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
