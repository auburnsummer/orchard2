import { Link } from "@cafe/minibridge/components/Link";
import { Shell } from "../components/Shell";

import { List, ListItem, Text } from "@mantine/core";

export function HomeView() {
  return (
    <Shell>
      <Text>
        Rhythm Café is an unofficial site for Rhythm Doctor custom levels.
      </Text>
      <Text>This site is not associated with 7th Beat Games or Indienova.</Text>
      <List>
        <ListItem>
          <Link href="/levels">See all the levels</Link>
        </ListItem>
        <ListItem>
          <Link href="https://docs.google.com/spreadsheets/d/1Uz26L34OZIgaK6hMfLBysgtEW4TYDj7iZZ5KqOMbNKY">
            Level setlists (for beginners)
          </Link>
        </ListItem>
        <ListItem>
          <Link href="https://example.com">How to add a level</Link>
        </ListItem>
        <ListItem>
          <Link href="https://rd-editor-docs.github.io/intro/">
            Editor tutorial
          </Link>
        </ListItem>
      </List>
    </Shell>
  );
}
