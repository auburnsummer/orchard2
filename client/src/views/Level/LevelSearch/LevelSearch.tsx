import React, { useMemo } from 'react';
import styles from './LevelSearch.module.css';
import { RDLevel } from '@cafe/types/rdLevelBase';
import { Shell } from '@cafe/components/Shell';
import { LevelCard } from '@cafe/components/LevelCard/LevelCard';
import { Button, Title } from '@mantine/core';
import { useSearchParams } from '@cafe/minibridge/hooks';

// nb: there are 21 levels per page in the API, but we only show 20 here
// the last one is used to determine if there are more pages
const LEVELS_PER_PAGE = 20;

type BooleanFacet<T> = {
    true: T;
    false: T;
}

interface LevelSearchProps {
    results: {
        estimatedTotalHits: number;
        limit: number;
        offset: number;
        query: string;
        hits: RDLevel[];
        facetDistribution: {
            artist_tokens: Record<string, number>;
            authors: Record<string, number>;
            "club.id": Record<string, number>;
            difficulty: Record<number, number>;
            has_classics: BooleanFacet<number>;
            has_freetimes: BooleanFacet<number>;
            has_freezeshots: BooleanFacet<number>;
            has_holds: BooleanFacet<number>;
            has_oneshots: BooleanFacet<number>;
            has_squareshots: BooleanFacet<number>;
            has_window_dance: BooleanFacet<number>;
            single_player: BooleanFacet<number>;
            "submitter.id": Record<string, number>;
            tags: Record<string, number>;
            two_player: BooleanFacet<number>;
        }
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

    return (
        <Shell
            navbar={
                <p>facets will go here</p>
            }
        >
            <div className={styles.levelsContainer}>
                <div className={styles.levelsHeader}>
                    <Title order={4} className={styles.levelsTitle}>
                        {levelTitleText}
                    </Title>
                    <div className={styles.nextPrevButtons}>
                        <Button onClick={onPrev} disabled={!showPrevious} variant='outline'>Previous</Button>
                        <Button onClick={onNext} disabled={!showNext} variant='outline'>Next</Button>
                    </div>
                </div>
                <ul className={styles.gridContainer}> 
                    {
                        results.hits.slice(0, LEVELS_PER_PAGE).map((level) => (
                            <li key={level.id}>
                                <LevelCard level={level} className={styles.levelCard} />
                            </li>
                        ))
                    }
                </ul>
            </div>
        </Shell>
   );
}; 