import React from 'react';
import styles from './LevelSearch.module.css';

interface LevelSearchProps {
    message: string;
}

export const LevelSearch: React.FC<LevelSearchProps> = ({ message }) => {
    return (
        <div className={styles.container}>
            {message || "Search placeholder"}
        </div>
    );
}; 