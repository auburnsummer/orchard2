import styles from "./FacetSelect.module.css";

import cc from "clsx";

import { Checkbox, Group, Loader, Stack, Text, TextInput } from "@mantine/core";
import { Facet } from "../../LevelSearch";

import { useEffect, useMemo, useState } from "react";
import { djangoGet } from "@cafe/minibridge/fetch";
import { notifications } from "@mantine/notifications";
import { useSearchParams } from "@cafe/minibridge/hooks";
import { removeDuplicates } from "@cafe/utils/list";

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
    const [searchResults, setSearchResults] = useState<Facet[]>(facets);
    const [isSearching, setIsSearching] = useState(false);

    const [searchParams, navigateViaSearchParams] = useSearchParams();

    const selectedFacets = facets.filter(f => searchParams.getAll("tags_all").includes(f.value));

    useEffect(() => {
        setFilter("");
    }, [facets]);

    useEffect(() => {
        console.log(`Filter changed: ${filter}`);
        if (filter === "") {
            setSearchResults([]);
            return;
        }
        const newUrl = new URL(window.location.href);
        newUrl.searchParams.set("facet_query_field", `tags`);
        newUrl.searchParams.set("facet_query", filter);
        setIsSearching(true);
        (async () => {
            const resp = await djangoGet(newUrl.toString());
            if (resp.action === "render") {
                setIsSearching(false);
                setSearchResults(resp.props.facets as Facet[]);
            } else {
                notifications.show({
                    title: "Unknown error",
                    message: `Failed to fetch facets for ${facetName}}`,
                    color: "red",
                });
            }
        })();
    }, [filter]);

    const displayFacets = useMemo(() => {
        if (searchResults.length > 0) {
            const toDisplay = [...selectedFacets, ...searchResults];
            return removeDuplicates(toDisplay);
        }
        return facets;
    }, [searchResults, facets]);

    return (
        <div className={cc(styles.container, className)} {...rest}>
            <Group gap="xs">
                <Text fw={700} className={styles.label}>
                    {facetName}
                </Text>
                {
                    isSearching && <Loader size="xs" type="dots"/>
                }
            </Group>
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
                    displayFacets.map(({ value, count }) => (
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
                                        params.append("tags_all", value);
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