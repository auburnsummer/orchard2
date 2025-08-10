import { Group, Text, Stack, Checkbox, RangeSlider } from '@mantine/core';
import styles from './BPMSelect.module.css';

import { useState } from 'react';
import { useSearchParams } from '@cafe/minibridge/hooks';

export function BPMSelect() {

    const [searchParams, navigateViaSearchParams] = useSearchParams();

    const minBpmS = searchParams.get("min_bpm");
    const maxBpmS = searchParams.get("max_bpm");
    const minBpm = minBpmS ? parseInt(minBpmS, 10) : null;
    const maxBpm = maxBpmS ? parseInt(maxBpmS, 10) : null;

    const [isEnabled, setIsEnabled] = useState(minBpm !== null || maxBpm !== null);

    return (
        <div className={styles.container}>
            <Group>
                <Text fw={700} className={styles.label}>
                    BPM
                </Text>
                <Checkbox
                    onChange={(event) => {
                        const checked = event.currentTarget.checked;
                        setIsEnabled(checked);
                        if (!checked) {
                            navigateViaSearchParams(params => {
                                params.delete("min_bpm");
                                params.delete("max_bpm");
                            });
                        }
                    }}
                    checked={isEnabled}
                    size="xs"
                    label="Enable filter"
                    defaultChecked={false}
                />
            </Group>

            <RangeSlider
                min={20}
                max={400}
                defaultValue={[minBpm ?? 20, maxBpm ?? 400]}
                step={1}
                disabled={!isEnabled}
                className={styles.slider}
                onChangeEnd={(value) => {
                    const [min, max] = value;
                    navigateViaSearchParams(params => {
                        params.set("min_bpm", min.toString());
                        params.set("max_bpm", max.toString());
                    });
                }}
            ></RangeSlider>
        </div>
    )
}