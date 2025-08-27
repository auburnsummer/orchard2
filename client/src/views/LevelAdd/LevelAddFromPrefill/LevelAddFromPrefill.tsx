import { RDLevelPrefill } from "@cafe/types/rdLevelPrefill"
import { PrefillLoading } from "./PrefillLoading/PrefillLoading"
import { PrefillReady } from "./PrefillReady/PrefillReady"
import { PrefillUpdate } from "./PrefillUpdate/PrefillUpdate"

type LevelAddFromPrefillProps = {
    prefill: RDLevelPrefill
}

export function LevelAddFromPrefill({prefill}: LevelAddFromPrefillProps) {
    if (prefill.ready) {
        if (prefill.prefill_type === 'new') {
            return <PrefillReady prefill={prefill} />
        }
        else {
            return <PrefillUpdate prefill={prefill} />
        }
    }
    
    return (
        <PrefillLoading prefillType={prefill.prefill_type} error={prefill.errors} />
    )
}