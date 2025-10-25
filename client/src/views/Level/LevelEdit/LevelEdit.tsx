import { EditLevelForm } from "@cafe/components/EditLevelForm";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Alert, Text } from "@mantine/core";

type LevelEditProps = {
  rdlevel: RDLevel;
};

export function LevelEdit({ rdlevel }: LevelEditProps) {
  return (
    <EditLevelForm
      level={rdlevel}
      preamble={
        <Alert icon={<FontAwesomeIcon icon={faInfoCircle} />}>
          <Text>
            This page is for changing the metadata of the level without changing
            the actual .rdzip file.
          </Text>
          <Text>
            If you want to upload a new .rdzip file, please upload it to Discord
            first, use the "Add to Rhythm Café" command, then select "Update to
            existing level."
          </Text>
        </Alert>
      }
      submitButtonText="Edit Level"
    />
  );
}
