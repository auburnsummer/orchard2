
import { useSearchParams } from '@cafe/minibridge/hooks';
import styles from './DifficultySelect.module.css';
import { Checkbox, Stack, Text } from '@mantine/core';

const DIFFICULTY_NAMES = [
    "Easy",
    "Medium",
    "Tough",
    "Very Tough"
]

export function DifficultySelect() {
    const [searchParams, navigateViaSearchParams] = useSearchParams();

    const selectedDifficulties = searchParams.getAll("difficulty").map(Number);

    return (
        <div className={styles.container}>
            <Text fw={700} className={styles.label}>
                Difficulty
            </Text>
            <Stack gap="0.125rem">
                {
                    [0, 1, 2, 3].map(level => (
                        <Checkbox
                            key={level}
                            defaultChecked={selectedDifficulties.includes(level)}
                            label={`${DIFFICULTY_NAMES[level]}`}
                            onChange={(event) => {
                                const checked = event.currentTarget.checked;
                                navigateViaSearchParams(params => {
                                    if (checked) {
                                        params.append("difficulty", level.toString());
                                    } else {
                                        params.delete("difficulty", level.toString());
                                    }
                                })
                            }}
                        />
                    ))
                }
            </Stack>
            
        </div>
    );
}