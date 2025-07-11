import styles from "./FacetSelect.module.css";

import cc from "clsx";

import { Checkbox, Group, Stack, Text, TextInput } from "@mantine/core";
import { Facet } from "../../LevelSearch";

type FacetSelectProps = React.HTMLAttributes<HTMLDivElement> & {
    facetName: string;
    facets: Facet[];
}

export function FacetSelect({ facetName, className, facets, ...rest }: FacetSelectProps) {
    return (
        <div className={cc(styles.container, className)} {...rest}>
            <Text fw={700} className={styles.label}>
                {facetName}
            </Text>
            <TextInput placeholder="Filter..." size="xs" className={styles.input} radius="xs" />
            <Stack gap="0.125rem">
                {
                    facets.map(({ value, count }) => (
                        <Checkbox key={value} label={
                                <Group gap="0.25rem" align="baseline">
                                    <Text>{value}</Text>
                                    <Text size="xs" c="dimmed">({count})</Text>
                                </Group>
                            }
                        />
                    ))
                }
            </Stack>
        </div>
    );

}