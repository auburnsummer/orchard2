import styles from "./FacetSelect.module.css";

import cc from "clsx";

import { Checkbox, Group, Stack, Text, TextInput } from "@mantine/core";
import { Facet } from "../../LevelSearch";

import { useEffect, useState } from "react";
import { djangoGet } from "@cafe/minibridge/fetch";

type FacetSelectProps = React.HTMLAttributes<HTMLDivElement> & {
    facetName: string;
    facets: Facet[];
}

export function FacetSelect({ facetName, className, facets, ...rest }: FacetSelectProps) {
    const [filter, setFilter] = useState("");

    useEffect(() => {
        console.log(`Filter changed: ${filter}`);
        const newUrl = new URL(window.location.href);
        newUrl.searchParams.set("facet_query_field", `tags`);
        newUrl.searchParams.set("facet_query", filter);
        djangoGet(newUrl.toString()).then(console.log)
    }, [filter]);

    return (
        <div className={cc(styles.container, className)} {...rest}>
            <Text fw={700} className={styles.label}>
                {facetName}
            </Text>
            <TextInput
                placeholder="Filter..."
                size="xs"
                className={styles.input}
                radius="xs"
                value={filter}
                onChange={(e) => setFilter(e.currentTarget.value)}
            />
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