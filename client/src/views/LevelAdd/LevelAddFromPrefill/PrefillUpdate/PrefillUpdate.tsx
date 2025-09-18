import { LevelCard } from "@cafe/components/LevelCard/LevelCard";
import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { RDLevelPrefillUpdateReady } from "@cafe/types/rdLevelPrefill";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Alert, Box, Button, Group, List, ListItem, Text, TextInput, Title } from "@mantine/core";

type PrefillUpdateProps = {
    prefill: RDLevelPrefillUpdateReady
    potentialMatches: RDLevel[]
}

export function PrefillUpdate({ potentialMatches }: PrefillUpdateProps) {
    return (
        <Shell>
            <Box p="md">
                <Alert icon={<FontAwesomeIcon icon={faInfoCircle} />}>
                    <Text>Select the level this rdzip is updating.</Text>
                    <Text>There are two ways you can do this.</Text>
                    <List>
                        <ListItem><Text>If you know the level ID of the old level, enter it into the "Level ID" input field and Submit.</Text></ListItem>
                        <ListItem><Text>We have also guessed potential levels for your rdzip in the "Potential Matches" section below. If your level is there, you can select it, then click Submit.</Text></ListItem>
                    </List>
                    <Text>If the level does not appear in Potential Matches, please search for the level to find the level ID to update.</Text>
                </Alert>
                <Group align="end">
                    <TextInput label="Level ID" placeholder="Enter level ID" />
                    <Button>Submit</Button>
                </Group>
                <Title order={3} mt="md" mb="sm">Potential Matches</Title>
                {potentialMatches.length === 0 && <Text>No potential matches found.</Text>}
                {potentialMatches.length > 0 && (
                    <List>
                        {potentialMatches.map((match) => (
                            <LevelCard key={match.id} level={match} showId={true} className="fejiwaf" />
                        ))}
                    </List>
                )}
            </Box>
        </Shell>
    )
}