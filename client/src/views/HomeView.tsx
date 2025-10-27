import { Link } from "@cafe/minibridge/components/Link";
import { Shell } from "../components/Shell";
import { Words } from "@cafe/components/ui/Words";


export function HomeView() {
  return (
    <Shell>
      <div className="flex flex-col lg:flex-row gap-8 p-8 max-w-7xl mx-auto">
        {/* Left side - Content */}
        <div className="flex-1 flex flex-col gap-6">
          <div>
            <Words as="p" className="text-lg mb-2">
              Rhythm Café is an unofficial site for Rhythm Doctor custom levels.
            </Words>
            <Words as="p" variant="muted" className="text-sm">
              This site is not associated with 7th Beat Games or Indienova.
            </Words>
          </div>

          <div className="bg-white dark:bg-slate-700 rounded-lg p-6 shadow-sm">
            <Words as="h2" variant="subheader" className="mb-4">
              Quick Links
            </Words>
            <ul className="space-y-3">
              <li className="flex items-center gap-2">
                <span className="text-violet-600 dark:text-violet-400 mt-0.5">→</span>
                <Words as={Link} variant="link" href="/levels">
                  Browse all custom levels
                </Words>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-violet-600 dark:text-violet-400 mt-0.5">→</span>
                <Words as={Link} variant="link" href="https://docs.google.com/spreadsheets/d/1Uz26L34OZIgaK6hMfLBysgtEW4TYDj7iZZ5KqOMbNKY">
                  Level setlists (for beginners)
                </Words>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-violet-600 dark:text-violet-400 mt-0.5">→</span>
                <Words as={Link} variant="link" href="https://example.com">
                  How to add a level
                </Words>
              </li>
              <li className="flex items-center gap-2">
                <span className="text-violet-600 dark:text-violet-400 mt-0.5">→</span>
                <Words as={Link} variant="link" href="https://rd-editor-docs.github.io/intro/">
                  Editor tutorial
                </Words>
              </li>
            </ul>
          </div>
        </div>

        {/* Right side - Illustration Placeholder */}
        <div className="flex-1 flex items-center justify-center">
          <div className="w-full max-w-md aspect-square rounded-lg shadow-lg flex items-center justify-center bg-purple-200 dark:bg-purple-600">
            <div className="flex flex-col gap-4">
              <Words className="text-center px-8">
                The daily blend goes here probably
              </Words>
            </div>
          </div>
        </div>
      </div>
    </Shell>
  );
}
