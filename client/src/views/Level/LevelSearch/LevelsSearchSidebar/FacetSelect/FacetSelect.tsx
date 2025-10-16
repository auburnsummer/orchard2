import styles from "./FacetSelect.module.css";

import cc from "clsx";

import { Checkbox, Group, Loader, Stack, Text, TextInput } from "@mantine/core";
import { Facet } from "../../LevelSearch";

import { useEffect, useMemo, useState } from "react";
import { djangoGet } from "@cafe/minibridge/fetch";
import { notifications } from "@mantine/notifications";
import { useSearchParams } from "@cafe/minibridge/hooks";
import { removeDuplicates } from "@cafe/utils/list";
import { useDebouncedValue } from "@mantine/hooks";

type FacetSelectProps = React.HTMLAttributes<HTMLDivElement> & {
  facetName: string;
  facets: Facet[];
  searchParamKey: string;
  facetQueryField: string;
};

export function FacetSelect({
  facetName,
  className,
  facets,
  searchParamKey,
  facetQueryField,
  ...rest
}: FacetSelectProps) {
  const [filter, setFilter] = useState("");
  const [filterDebounced] = useDebouncedValue(filter, 150);
  const [searchResults, setSearchResults] = useState<Facet[]>(facets);
  const [isSearching, setIsSearching] = useState(false);

  const [searchParams, navigateViaSearchParams] = useSearchParams();

  const selectedFacets = facets.filter((f) =>
    searchParams.getAll(searchParamKey).includes(f.value),
  );

  // we should reset the filter when facets change
  useEffect(() => {
    setFilter("");
  }, [facets]);

  useEffect(() => {
    if (filterDebounced === "") {
      setSearchResults([]);
      return;
    }
    const facetQueryUrl = new URL(window.location.href);
    facetQueryUrl.searchParams.set("facet_query_field", facetQueryField);
    facetQueryUrl.searchParams.set("facet_query", filterDebounced);
    setIsSearching(true);
    let isCancelled = false;
    (async () => {
      const resp = await djangoGet(facetQueryUrl.toString());
      if (resp.action === "render") {
        if (isCancelled) return;
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
    return () => {
      isCancelled = true;
    };
  }, [filterDebounced]);

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
        {isSearching && <Loader size="xs" type="dots" />}
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
        {displayFacets.map(({ value, count }) => (
          <Checkbox
            key={value}
            defaultChecked={selectedFacets.some((f) => f.value === value)}
            label={
              <Group gap="0.25rem" align="baseline">
                <Text size="sm">{value}</Text>
                <Text size="xs" c="dimmed">
                  ({count})
                </Text>
              </Group>
            }
            onChange={(event) => {
              const checked = event.currentTarget.checked;
              navigateViaSearchParams((params) => {
                if (checked) {
                  params.append(searchParamKey, value);
                } else {
                  params.delete(searchParamKey, value);
                }
              });
            }}
          />
        ))}
      </Stack>
    </div>
  );
}
