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
        <p>facets</p>
    );
}