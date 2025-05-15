import { RDLevelPrefillReady } from "@cafe/types/rdLevelPrefill"
import { Alert, Text } from "@mantine/core";

import { RDLevel } from "@cafe/types/rdLevelBase";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { EditLevelForm } from "@cafe/components/EditLevelForm/EditLevelForm";

function buildInitialLevel(prefill: RDLevelPrefillReady): RDLevel {
    return {
        ...prefill.data,
        id: "",
        song_alt: "",
        submitter: prefill.user,
        club: prefill.club,
        approval: 0
    }
}

type PrefillReadyProps = {
    prefill: RDLevelPrefillReady
}

export function PrefillReady({ prefill }: PrefillReadyProps) {
    return (
        <EditLevelForm
            level={buildInitialLevel(prefill)}
            preamble={
                <Alert icon={<FontAwesomeIcon icon={faInfoCircle} />}>
                    <Text>We've filled out the fields below based on the rdzip file.</Text>
                    <Text>If it all looks OK, you can simply click "Add Level" now to add the level.</Text>
                    <Text>Otherwise, make changes, and then click "Add Level".</Text>
                    <Text>You will be able to come back and edit later.</Text>
                </Alert>
            }
            submitButtonText="Add Level"
        />
    );
}