import { RDLevelPrefillReady } from "@cafe/types/rdLevelPrefill";

import { RDLevel } from "@cafe/types/rdLevelBase";

import { EditLevelForm } from "@cafe/components/EditLevelForm";
import { Alert } from "@cafe/components/ui/Alert";
import { Words } from "@cafe/components/ui/Words";

function buildInitialLevel(prefill: RDLevelPrefillReady): RDLevel {
  return {
    ...prefill.data,
    id: "",
    song_alt: "",
    submitter: prefill.user,
    club: prefill.club,
    approval: 0,
    is_private: false
  };
}

type PrefillReadyProps = {
  prefill: RDLevelPrefillReady;
};

export function PrefillReady({ prefill }: PrefillReadyProps) {
  return (
    <EditLevelForm
      level={buildInitialLevel(prefill)}
      preamble={
        <Alert variant="info" className="m-4">
          <Words as="p">
            We've filled out the fields below based on the rdzip file.
          </Words>
          <Words as="p">
            If it all looks OK, you can simply click "Add Level" now to add the
            level.
          </Words>
          <Words as="p">
            Otherwise, make changes, and then click "Add Level".
          </Words>
          <Words as="p">
            You will be able to come back and edit later.
          </Words>
        </Alert>
      }
      submitButtonText="Add Level"
    />
  );
}
