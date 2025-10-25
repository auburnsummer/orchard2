import type { FacetDistribution } from "../LevelSearch";

import { FacetSelect } from "./FacetSelect/FacetSelect";
import { DifficultySelect } from "./DifficultySelect/DifficultySelect";
import { BPMSelect } from "./BPMSelect/BPMSelect";
import { PeerReviewStatusSelect } from "./PeerReviewStatusSelect/PeerReviewStatusSelect";
import { Surface } from "@cafe/components/ui/Surface";

import cc from "clsx";

type LevelsSearchSidebarProps = React.HTMLAttributes<HTMLDivElement> & {
  facets: FacetDistribution;
};

export function LevelsSearchSidebar({
  className,
  facets,
  ...rest
}: LevelsSearchSidebarProps) {
  return (
    <Surface className={cc("mx-2 flex flex-col overflow-hidden", className)} {...rest}>
      <div className="overflow-y-auto flex flex-col gap-6 p-2">
        <FacetSelect
          facetName="Tags"
          facets={facets.tags}
          searchParamKey="tags_all"
          facetQueryField="tags"
        />
        <FacetSelect
          facetName="Authors"
          facets={facets.authors}
          searchParamKey="authors_all"
          facetQueryField="authors"
        />
        <FacetSelect
          facetName="Artists"
          facets={facets.artist_tokens}
          searchParamKey="artists_all"
          facetQueryField="artist_tokens"
        />
        <DifficultySelect />
        <BPMSelect />
        <PeerReviewStatusSelect />
      </div>
    </Surface>
  );
}
