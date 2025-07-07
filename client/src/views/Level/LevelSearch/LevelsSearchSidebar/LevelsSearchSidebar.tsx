import type { FacetDistribution } from '../LevelSearch';
import styles from './LevelsSearchSidebar.module.css';

import cc from "clsx";

import { Text } from '@mantine/core';
import { FacetSelect } from './FacetSelect/FacetSelect';

type LevelsSearchSidebarProps = React.HTMLAttributes<HTMLDivElement> & {
    facets: FacetDistribution;
}

export function LevelsSearchSidebar({className, facets, ...rest}: LevelsSearchSidebarProps) {
    return (
        <div className={cc(styles.container, className)} {...rest}>
            <FacetSelect facetName="Tags" facet={facets.tags} />
        </div>
    );
}