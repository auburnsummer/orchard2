import { RDLevelPrefill } from "@cafe/types/rdLevelPrefill"
import { PrefillLoading } from "./PrefillLoading/PrefillLoading"
import { PrefillReady } from "./PrefillReady/PrefillReady"
import { PrefillUpdate } from "./PrefillUpdate/PrefillUpdate"
import { RDLevel } from "@cafe/types/rdLevelBase"

type LevelAddFromPrefillProps = {
    prefill: RDLevelPrefill
    potential_matches: RDLevel[]
}

export function LevelAddFromPrefill({prefill, potential_matches}: LevelAddFromPrefillProps) {
    if (prefill.ready) {
        if (prefill.prefill_type === 'new') {
            return <PrefillReady prefill={prefill} />
        }
        else {
            return <PrefillUpdate prefill={prefill} potentialMatches={potential_matches}/>
        }
    }
    
    return (
        <PrefillLoading prefillType={prefill.prefill_type} error={prefill.errors} />
    )
}