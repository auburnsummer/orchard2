import styles from "./FacetSelect.module.css";

import cc from "clsx";

import { Checkbox, Group, Stack, Text, TextInput } from "@mantine/core";
import { Facet } from "../../LevelSearch";

import { useEffect, useState } from "react";
import { djangoGet } from "@cafe/minibridge/fetch";
import { notifications } from "@mantine/notifications";
import { useSearchParams } from "@cafe/minibridge/hooks";

type FacetSelectProps = React.HTMLAttributes<HTMLDivElement> & {
    facetName: string;
    facets: Facet[];
}

const searchFacets = async (facetName: string, filter: string) => {
    const newUrl = new URL(window.location.href);
    newUrl.searchParams.set("facet_query_field", facetName);
    newUrl.searchParams.set("facet_query", filter);
    const result = await djangoGet(newUrl.toString());
    if (result.action === "render") {
        console.log("Search facets result:", result.props);
        return result.props.facets as Facet[];
    }  else {
        notifications.show({
            title: "Unknown error",
            message: `Failed to fetch facets for ${facetName}}`,
            color: "red",
        })
    }
}

export function FacetSelect({ facetName, className, facets, ...rest }: FacetSelectProps) {
    const [filter, setFilter] = useState("");

    const [searchParams, navigateViaSearchParams] = useSearchParams();

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
                        <Checkbox
                            key={value}
                            defaultChecked={searchParams.getAll("tags_all").includes(value)}
                            label={
                                <Group gap="0.25rem" align="baseline">
                                    <Text>{value}</Text>
                                    <Text size="xs" c="dimmed">({count})</Text>
                                </Group>
                            }
                            onChange={(event) => {
                                const checked = event.currentTarget.checked;
                                navigateViaSearchParams(params => {
                                    if (checked) {
                                        params.append("tags_all", value)
                                    } else {
                                        params.delete("tags_all", value);
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