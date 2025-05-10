import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Container, BackgroundImage } from "@mantine/core";

type LevelViewProps = {
    rdlevel: RDLevel
}

export function LevelView({rdlevel}: LevelViewProps) {
    return (
        <Shell>
            <Container>
                <div>
                    <h1>hi</h1>
                    <pre>{JSON.stringify(rdlevel, null, 2)}</pre>
                </div>
            </Container>
        </Shell>
    );
}