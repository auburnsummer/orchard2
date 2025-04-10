import { Shell } from "@cafe/components/Shell"
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
        <PrefillLoading error={prefill.errors} />
    )
}