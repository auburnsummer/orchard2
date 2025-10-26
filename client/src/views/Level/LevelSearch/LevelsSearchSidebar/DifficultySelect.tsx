import { useSearchParams } from "@cafe/minibridge/hooks";
import { Checkbox } from "@cafe/components/ui/Checkbox";
import { Words } from "@cafe/components/ui/Words";

const DIFFICULTY_NAMES = ["Easy", "Medium", "Tough", "Very Tough"];

export function DifficultySelect() {
  const [searchParams, navigateViaSearchParams] = useSearchParams();

  const selectedDifficulties = searchParams.getAll("difficulty").map(Number);

  return (
    <div>
      <Words variant="label" className="mb-2 block">
        Difficulty
      </Words>
      <div className="flex flex-col gap-0.5">
        {[0, 1, 2, 3].map((level) => (
          <Checkbox
            key={level}
            defaultChecked={selectedDifficulties.includes(level)}
            label={`${DIFFICULTY_NAMES[level]}`}
            onChange={(event) => {
              const checked = event.currentTarget.checked;
              navigateViaSearchParams((params) => {
                if (checked) {
                  params.append("difficulty", level.toString());
                } else {
                  params.delete("difficulty", level.toString());
                }
              });
            }}
          />
        ))}
      </div>
    </div>
  );
}
