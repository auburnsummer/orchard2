import { Checkbox } from "@cafe/components/ui/Checkbox";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Words } from "@cafe/components/ui/Words";
import { Facet } from "../LevelSearch";

import { useEffect, useMemo, useState } from "react";
import { djangoGet } from "@cafe/minibridge/fetch";
import { notifications } from "@mantine/notifications";
import { useSearchParams } from "@cafe/minibridge/hooks";
import { removeDuplicates } from "@cafe/utils/list";
import { useDebouncedValue } from "@mantine/hooks";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleNotch } from "@fortawesome/free-solid-svg-icons";

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
    <div className={className} {...rest}>
      <div className="flex items-center gap-2 mb-2">
        <Words variant="label">
          {facetName}
        </Words>
        {isSearching && (
          <FontAwesomeIcon 
            icon={faCircleNotch} 
            className="animate-spin text-violet-600 dark:text-violet-400" 
            size="xs" 
          />
        )}
      </div>
      <TextInput
        placeholder="Filter..."
        className="pr-1 mb-1.5"
        value={filter}
        onChange={(e) => setFilter(e.currentTarget.value)}
      />
      <div className="flex flex-col gap-0.5">
        {displayFacets.map(({ value, count }) => (
          <Checkbox
            key={value}
            defaultChecked={selectedFacets.some((f) => f.value === value)}
            label={
              <span className="flex items-baseline gap-1">
                <Words variant="sm">{value}</Words>
                <Words variant="xs">
                  ({count})
                </Words>
              </span>
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
      </div>
    </div>
  );
}
