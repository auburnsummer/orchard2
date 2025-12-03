import React, { useMemo } from "react";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Shell } from "@cafe/components/Shell";
import { LevelCard } from "@cafe/components/LevelCard/LevelCard";
import { Button } from "@cafe/components/ui/Button";
import { Words } from "@cafe/components/ui/Words";
import { useSearchParams } from "@cafe/minibridge/hooks";
import { LevelsSearchSidebar } from "./LevelsSearchSidebar/LevelsSearchSidebar";

// nb: there are 21 levels per page in the API, but we only show 20 here
// the last one is used to determine if there are more pages
const LEVELS_PER_PAGE = 20;

export type Facet = {
  count: number;
  value: string;
};

export type FacetDistribution = {
  artist_tokens: Facet[];
  authors: Facet[];
  "club.id": Facet[];
  difficulty: Facet[];
  single_player: Facet[];
  "submitter.id": Facet[];
  tags: Facet[];
  two_player: Facet[];
};

interface LevelSearchProps {
  results: {
    estimatedTotalHits: number;
    processingTimeMs: number;
    limit: number;
    offset: number;
    query: string;
    hits: RDLevel[];
    facetDistribution: FacetDistribution;
  };
}

function getPageFromSearchParams(searchParams: URLSearchParams): number {
  const page = parseInt(searchParams.get("page") || "1");
  return Number.isNaN(page) ? 1 : page;
}

export const LevelSearch: React.FC<LevelSearchProps> = ({ results }) => {
  const [searchParams, navigateViaSearchParams] = useSearchParams();

  const query = searchParams.get("q") || "";
  const page = getPageFromSearchParams(searchParams);

  const movePage = (n: number) => {
    navigateViaSearchParams((params) => {
      let next = page + n;
      params.set("page", `${next}`);
    });
  };

  const onNext = () => movePage(1);
  const onPrev = () => movePage(-1);

  const levelTitleText = useMemo(() => {
    if (query === "") {
      return "All levels";
    } else if (results.hits.length === 0) {
      return (
        <span>
          No results found for "<span className="text-violet-600 dark:text-violet-400">{query}</span>"
        </span>
      );
    } else if (results.estimatedTotalHits === 1000) {
      return (
        <span>
          Results for "<span className="text-violet-600 dark:text-violet-400">{query}</span>"
        </span>
      );
    } else {
      return `${results.estimatedTotalHits} results for "${query}"`;
    }
  }, [query, results]);

  const showPrevious = page > 1;
  const showNext = results.hits.length > LEVELS_PER_PAGE;

  const nextPrevButtons = (
    <div className="flex gap-2">
      <Button
        onClick={onPrev}
        disabled={!showPrevious}
      >
        Previous
      </Button>
      <Button
        onClick={onNext}
        disabled={!showNext}
      >
        Next
      </Button>
    </div>
  );

  return (
    <Shell
      navbar={
        <LevelsSearchSidebar
          className="pl-2 mt-4 mb-3"
          facets={results.facetDistribution}
        />
      }
    >
      <div className="p-4">
        <div className="flex justify-between items-center mb-4">
          <Words as="h2" variant="header">
            {levelTitleText}
          </Words>
          {nextPrevButtons}
        </div>
        <ul className="list-none grid gap-4 [--grid-column-count:3] [--grid-item--min-width:18rem] [--gap-count:calc(var(--grid-column-count)-1)] [--total-gap-width:calc(var(--gap-count)*1rem)] [--grid-item--max-width:calc((100%-var(--total-gap-width))/var(--grid-column-count))] grid-cols-[repeat(auto-fill,minmax(max(var(--grid-item--min-width),var(--grid-item--max-width)),1fr))]">
          {results.hits.slice(0, LEVELS_PER_PAGE).map((level) => (
            <li key={level.id}>
              <LevelCard
                level={level}
                className="w-full h-full"
                href={`/levels/${level.id}/`}
              />
            </li>
          ))}
        </ul>
        <div className="flex justify-between items-center mt-8">
          <Words variant="xs">
            Δ{results.processingTimeMs}ms
          </Words>
          {
            /* only show bottom buttons if there are enough results to need them */
            results.hits.length > (LEVELS_PER_PAGE / 2) && nextPrevButtons
          }
        </div>
      </div>
    </Shell>
  );
};
