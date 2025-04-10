import { LevelCard } from "@cafe/components/LevelCard/LevelCard"
import { Shell } from "@cafe/components/Shell"
import { RDLevelPrefillReady } from "@cafe/types/rdLevelPrefill"
import commonStyles from '@cafe/theme/commonPatterns.module.css';
import styles from "./PrefillReady.module.css";
import { Box, Center } from "@mantine/core";

import cc from "clsx";

type PrefillReadyProps = {
    prefill: RDLevelPrefillReady
}

function PrefillPreview(props: RDLevelPrefillReady) {
    return (
        <Center className={cc(styles.aside, commonStyles.paperBg)}>
            <LevelCard level={props.data} />
        </Center>
    )
}

export function PrefillReady({prefill}: PrefillReadyProps) {
    return (
        <Shell
            aside={<PrefillPreview {...prefill} />}
        >
            <p>hello!</p>
        </Shell>
    )
}