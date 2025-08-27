import { Shell } from "@cafe/components/Shell";
import { RDLevelPrefillUpdateReady } from "@cafe/types/rdLevelPrefill";
import { faInfoCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Alert, List, ListItem, Text } from "@mantine/core";

type PrefillUpdateProps = {
    prefill: RDLevelPrefillUpdateReady
}

export function PrefillUpdate({ prefill }: PrefillUpdateProps) {
    // TODO: if we're going to just ask them to put the ID in sometimes we need to expose the ID better in level view
    return (
        <Shell>
            <Alert icon={<FontAwesomeIcon icon={faInfoCircle} />}>
                <Text>Select the level this rdzip is updating.</Text>
                <Text>There are two ways you can do this.</Text>
                <List>
                    <ListItem><Text>If you know the level ID, enter it into the "Level ID" input field and submit.</Text></ListItem>
                    <ListItem><Text>We have also identified potential matches for your rdzip in the "Potential Matches" section below. If your level is there, you can select it.</Text></ListItem>
                </List>
                <Text>If the level does not appear in Potential Matches, please search for the level to find the level ID to update.</Text>
            </Alert>
            <p>hello prefill update</p>
            <pre>
                {
                    JSON.stringify(prefill, null, 2)
                }
            </pre>
        </Shell>
    )
}