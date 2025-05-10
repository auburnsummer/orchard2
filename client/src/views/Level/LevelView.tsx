import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Container, Group, Image, Stack } from "@mantine/core";

type LevelViewProps = {
    rdlevel: RDLevel
}

export function LevelView({rdlevel}: LevelViewProps) {
    return (
        <Shell>
            <Container pt="md">
                <Group>
                    <Image
                        h={240}
                        w="auto"
                        src={rdlevel.image_url}
                    >
                    </Image>
                    <Stack>
                        <h1>{rdlevel.song}</h1>
                        <h2>{rdlevel.song_alt}</h2>
                        <h2>{rdlevel.artist}</h2>
                    </Stack>
                    {/* <img
                        src={rdlevel.image_url}
                    >
                    </img>
                    <Stack>
                        <h1>{rdlevel.song}</h1>
                    </Stack> */}
                </Group>
            </Container>
        </Shell>
    );
}