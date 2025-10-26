import { EditLevelForm } from "@cafe/components/EditLevelForm";
import { Alert } from "@cafe/components/ui/Alert";
import { Words } from "@cafe/components/ui/Words";
import { RDLevel } from "@cafe/types/rdLevelBase";

type LevelEditProps = {
  rdlevel: RDLevel;
};

export function LevelEdit({ rdlevel }: LevelEditProps) {
  return (
    <EditLevelForm
      level={rdlevel}
      preamble={
        <Alert>
          <Words>
            This page is for changing the metadata of the level without changing
            the actual .rdzip file.
          </Words>
          <Words>
            If you want to upload a new .rdzip file, please upload it to Discord
            first, use the "Add to Rhythm Café" command, then select "Update to
            existing level."
          </Words>
        </Alert>
      }
      submitButtonText="Edit Level"
    />
  );
}
