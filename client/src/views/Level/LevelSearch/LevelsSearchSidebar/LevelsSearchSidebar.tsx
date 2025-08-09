import type { FacetDistribution } from '../LevelSearch';
import styles from './LevelsSearchSidebar.module.css';

import cc from "clsx";

import { FacetSelect } from './FacetSelect/FacetSelect';
import { DifficultySelect } from './DifficultySelect/DifficultySelect';

type LevelsSearchSidebarProps = React.HTMLAttributes<HTMLDivElement> & {
    facets: FacetDistribution;
}

export function LevelsSearchSidebar({className, facets, ...rest}: LevelsSearchSidebarProps) {
    return (
        <div className={cc(styles.container, className)} {...rest}>
            <FacetSelect
                facetName="Tags"
                facets={facets.tags}
                searchParamKey='tags_all'
                facetQueryField='tags'
            />
            <FacetSelect
                facetName="Authors"
                facets={facets.authors}
                searchParamKey='authors_all'
                facetQueryField='authors'
            />
            <FacetSelect
                facetName="Artists"
                facets={facets.artist_tokens}
                searchParamKey='artists_all'
                facetQueryField='artist_tokens'
            />
            <DifficultySelect />
        </div>
    );
}