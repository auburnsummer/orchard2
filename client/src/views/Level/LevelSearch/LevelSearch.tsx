import React from 'react';
import styles from './LevelSearch.module.css';

interface LevelSearchProps {
    results: any;
}

export const LevelSearch: React.FC<LevelSearchProps> = ({ results }) => {
    return (
        <pre>
            {
                JSON.stringify(results, null, 2)
            }
        </pre>
   );
}; 