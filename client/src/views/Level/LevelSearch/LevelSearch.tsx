import React from 'react';
import styles from './LevelSearch.module.css';
import { RDLevel } from '@cafe/types/rdLevelBase';
import { Shell } from '@cafe/components/Shell';
import { LevelCard } from '@cafe/components/LevelCard/LevelCard';

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

export const LevelSearch: React.FC<LevelSearchProps> = ({ results }) => {
    return (
        <Shell
            navbar={
                <p>facets will go here</p>
            }
        >
            <ul className={styles.levels}>
                {
                    results.hits.map((level) => (
                        <li key={level.id}>
                            <LevelCard level={level} />
                        </li>
                    ))
                }
            </ul>
        </Shell>
   );
}; 