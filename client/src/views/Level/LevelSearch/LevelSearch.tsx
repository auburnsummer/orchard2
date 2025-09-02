import React, { useMemo } from 'react';
import styles from './LevelSearch.module.css';
import { RDLevel } from '@cafe/types/rdLevelBase';
import { Shell } from '@cafe/components/Shell';
import { LevelCard } from '@cafe/components/LevelCard/LevelCard';
import { Button, Title, Text } from '@mantine/core';
import { useSearchParams } from '@cafe/minibridge/hooks';
import { LevelsSearchSidebar } from './LevelsSearchSidebar/LevelsSearchSidebar';

// nb: there are 21 levels per page in the API, but we only show 20 here
// the last one is used to determine if there are more pages
const LEVELS_PER_PAGE = 20;

export type Facet = {
    count: number;
    value: string;
}

export type FacetDistribution = {
    artist_tokens: Facet[];
    authors: Facet[];
    "club.id": Facet[];
    difficulty: Facet[];
    has_classics: Facet[];
    has_freetimes: Facet[];
    has_freezeshots: Facet[];
    has_holds: Facet[];
    has_oneshots: Facet[];
    has_squareshots: Facet[];
    has_window_dance: Facet[];
    single_player: Facet[];
    "submitter.id": Facet[];
    tags: Facet[];
    two_player: Facet[];
}

interface LevelSearchProps {
    results: {
        estimatedTotalHits: number;
        processingTimeMs: number;
        limit: number;
        offset: number;
        query: string;
        hits: RDLevel[];
        facetDistribution: FacetDistribution;
    }
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
        navigateViaSearchParams(params => {
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
            return <span className={styles.noResults}>No results found for "<span className={styles.query}>{query}</span>"</span>;
        } else if (results.estimatedTotalHits === 1000) {
            return <span className={styles.moreResults}>Results for "<span className={styles.query}>{query}</span>"</span>;
        } else {
            return `${results.estimatedTotalHits} results for "${query}"`;
        }
    }, [query, results]);

    const showPrevious = page > 1;
    const showNext = results.hits.length > LEVELS_PER_PAGE;

    const nextPrevButtons = (
        <div className={styles.nextPrevButtons}>
            <Button onClick={onPrev} disabled={!showPrevious} variant='outline' size="compact-sm">Previous</Button>
            <Button onClick={onNext} disabled={!showNext} variant='outline' size="compact-sm">Next</Button>
        </div>
    )

    return (
        <Shell
            navbar={
                <LevelsSearchSidebar className={styles.sidebar} facets={results.facetDistribution} />
            }
        >
            <div className={styles.levelsContainer}>
                <div className={styles.levelsHeader}>
                    <Title order={4} className={styles.levelsTitle}>
                        {levelTitleText}
                    </Title>
                    {nextPrevButtons}
                </div>
                <ul className={styles.gridContainer}> 
                    {
                        results.hits.slice(0, LEVELS_PER_PAGE).map((level) => (
                            <li key={level.id}>
                                <LevelCard
                                    level={level}
                                    className={styles.levelCard}
                                    href={`/levels/${level.id}/`}
                                />
                            </li>
                        ))
                    }
                </ul>
                <div className={styles.levelsFooter}>
                    <Text size="xs" c="dimmed" className={styles.processingTime}>Δ{results.processingTimeMs}ms</Text>
                    {nextPrevButtons}
                </div>
            </div>
        </Shell>
   );
}; 