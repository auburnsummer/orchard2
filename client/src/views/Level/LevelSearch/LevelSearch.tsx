import React from 'react';
import styles from './LevelSearch.module.css';
import { JsonEditor } from 'json-edit-react'

interface LevelSearchProps {
    results: any;
}

export const LevelSearch: React.FC<LevelSearchProps> = ({ results }) => {
    return (
        <>
            {/* temporary so we can see the API response */}
            <JsonEditor data={results} />
        </>
   );
}; 