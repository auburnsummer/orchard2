import { DIFFICULTY_STRINGS } from "@cafe/utils/constants";
import styles from "./DifficultyDecorator.module.css";

import cc from "clsx";

type DifficultyDecoratorProps = React.HTMLAttributes<HTMLDivElement> & {
    difficulty: number;
}

const DIFFICULTY_CLASSES = [
    styles.easyDiff,
    styles.mediumDiff,
    styles.toughDiff,
    styles.vtoughDiff
];

export function DifficultyDecorator({difficulty, className, ...rest}: DifficultyDecoratorProps) {
    const difficultyString = DIFFICULTY_STRINGS[difficulty];
    const difficultyClass = DIFFICULTY_CLASSES[difficulty];

    return (
        <div className={cc(className, styles.base, difficultyClass)} {...rest}>
            <span role="presentation" className={styles.triangle}></span>
            <span className={styles.text}>{difficultyString}</span>
        </div>
    )
}