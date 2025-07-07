import styles from "./FacetSelect.module.css";

import cc from "clsx";

import { Checkbox, Group, Stack, Text, TextInput } from "@mantine/core";

type FacetSelectProps = React.HTMLAttributes<HTMLDivElement> & {
    facetName: string;
    facet: Record<string, number>;
}

export function FacetSelect({ facetName, className, facet, ...rest }: FacetSelectProps) {
    return (
        <div className={cc(styles.container, className)} {...rest}>
            <Text fw={700} className={styles.label}>
                {facetName}
            </Text>
            <TextInput placeholder="Filter..." size="xs" className={styles.input} radius="xs" />
            <Stack gap="0.125rem">
                {
                    Object.entries(facet).map(([key, value]) => (
                        <Checkbox key={key} label={
                                <Group gap="0.25rem" align="baseline">
                                    <Text>{key}</Text>
                                    <Text size="xs" c="dimmed">({value})</Text>
                                </Group>
                            }
                        />
                    ))
                }
            </Stack>
        </div>
    );

}