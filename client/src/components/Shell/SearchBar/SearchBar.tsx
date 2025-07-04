import { Button, TextInput } from '@mantine/core';
import styles from './SearchBar.module.css';
import React from 'react';

import cc from "clsx";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';

type SearchBarProps = React.HTMLAttributes<HTMLDivElement> & {
    placeholder?: string;
    initialValue?: string;
    onSearch?: (query: string) => void;
}

export function SearchBar({ placeholder, className, onSearch, initialValue }: SearchBarProps) {
    const [value, setValue] = React.useState(initialValue || "");

    const handleSearch = () => {
        if (onSearch) {
            onSearch(value);
        }
    };

    const onSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        handleSearch();
    };

    return (
        <form className={cc(styles.container, className)} onSubmit={onSubmit}>
            <TextInput
                type="text"
                placeholder={placeholder}
                className={styles.searchInput}
                defaultValue={initialValue}
                onChange={(e) => setValue(e.target.value)}
            />
            <Button className={styles.searchButton} type="submit" variant="default">
                <FontAwesomeIcon icon={faMagnifyingGlass} />
            </Button>
        </form>
    );
}