import { DIFFICULTY_STRINGS } from "@cafe/utils/constants";

import cc from "clsx";

type DifficultyDecoratorProps = React.HTMLAttributes<HTMLDivElement> & {
  difficulty: number;
};

const DIFFICULTY_CLASSES = [
  // Easy
  "bg-teal-100 text-teal-600 dark:bg-teal-900 dark:text-teal-200",
  // Medium
  "bg-amber-100 text-amber-600 dark:bg-amber-900 dark:text-amber-200",
  // Tough
  "bg-pink-100 text-pink-600 dark:bg-pink-900 dark:text-pink-200",
  // Very Tough
  "bg-violet-100 text-violet-600 dark:bg-violet-900 dark:text-violet-200",
];

export function DifficultyDecorator({
  difficulty,
  className,
  ...rest
}: DifficultyDecoratorProps) {
  const difficultyString = DIFFICULTY_STRINGS[difficulty];
  const difficultyClass = DIFFICULTY_CLASSES[difficulty];

  return (
    <div className={cc("flex", className)} {...rest}>
      <span 
        role="presentation" 
        className={cc(
          "w-6 [clip-path:polygon(0%_-4%,104%_-4%,104%_100%,100%_100%)]",
          difficultyClass
        )}
      />
      <span 
        className={cc(
          "text-xs leading-4 py-0.5 px-1 lowercase font-light rounded-[inherit]",
          difficultyClass
        )}
      >
        {difficultyString}
      </span>
    </div>
  );
}
