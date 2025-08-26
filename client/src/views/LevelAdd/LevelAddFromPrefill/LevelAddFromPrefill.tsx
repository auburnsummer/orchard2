import { RDLevelPrefill } from "@cafe/types/rdLevelPrefill"
import { PrefillLoading } from "./PrefillLoading/PrefillLoading"
import { PrefillReady } from "./PrefillReady/PrefillReady"

type LevelAddFromPrefillProps = {
    prefill: RDLevelPrefill
}

export function LevelAddFromPrefill({prefill}: LevelAddFromPrefillProps) {
    if (prefill.ready) {
        return (
            <PrefillReady prefill={prefill} />
        )
    }
    
    return (
        <PrefillLoading prefillType={prefill.prefill_type} error={prefill.errors} />
    )
}