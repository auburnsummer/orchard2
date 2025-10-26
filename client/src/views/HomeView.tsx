import { Link } from "@cafe/minibridge/components/Link";
import { Shell } from "../components/Shell";
import { Words } from "@cafe/components/ui/Words";


export function HomeView() {
  return (
    <Shell>
      <Words>
        Rhythm Café is an unofficial site for Rhythm Doctor custom levels.
      </Words>
      <Words>This site is not associated with 7th Beat Games or Indienova.</Words>
      <ul>
        <li>
          <Words as={Link} href="/levels">See all the levels</Words>
        </li>
        <li>
          <Words as={Link} href="https://docs.google.com/spreadsheets/d/1Uz26L34OZIgaK6hMfLBysgtEW4TYDj7iZZ5KqOMbNKY">
            Level setlists (for beginners)
          </Words>
        </li>
        <li>
          <Words as={Link} href="https://example.com">How to add a level</Words>
        </li>
        <li>
          <Words as={Link} href="https://rd-editor-docs.github.io/intro/">
            Editor tutorial
          </Words>
        </li>
      </ul>
    </Shell>
  );
}
