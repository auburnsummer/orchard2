import { LevelCard } from "@cafe/components/LevelCard/LevelCard"
import { RDLevel } from "@cafe/types/rdLevelBase"


type LevelAlreadyExistsProps = {
    existingLevel: RDLevel
}

export function LevelAlreadyExists({ existingLevel }: LevelAlreadyExistsProps) {
    return (
        <div>
            <h2>Level Already Exists</h2>
            <p>This rdzip has already been uploaded:</p>
            <LevelCard level={existingLevel} />
        </div>
    )
}
