import cc from 'clsx';
import './DifficultyDecorator.css';
import type { VitalsLevelExport } from '@orchard/api/levels';
import type { WithClass } from '@orchard/utils/withClass';

const DIFFICULTY_STRINGS = [
    "Easy",
    "Medium",
    "Tough",
    "Very Tough"
];

const DIFFICULTY_CLASSES = [
    'easy!dd',
    'medium!dd',
    'tough!dd',
    'ultima!dd'
];

type DifficultyDecoratorProps = Pick<VitalsLevelExport, 'difficulty'> & WithClass;

export function DifficultyDecorator({ difficulty, 'class': _class }: DifficultyDecoratorProps) {
    const difficultyString = DIFFICULTY_STRINGS[difficulty];
    const difficultyClass = DIFFICULTY_CLASSES[difficulty];

    return (
        <div class={cc(_class, 'dd', difficultyClass)}>
            <span role="presentation" class="dd_triangle"></span>
            <span class="dd_text">{difficultyString}</span>
        </div>
    );
}