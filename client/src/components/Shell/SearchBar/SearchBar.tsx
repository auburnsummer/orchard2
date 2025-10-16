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
        <form className={cc("flex my-1 rounded-tl-lg rounded-bl-lg", className)} onSubmit={onSubmit}>
            <input
                className="
                    bg-stone-50
                    rounded-tl-lg
                    rounded-bl-lg
                    px-3
                    active:bg-white
                    outline-none
                    focus:inset-ring-2
                    focus:inset-ring-violet-400
                "
                type="text"
                placeholder={placeholder}
                defaultValue={initialValue}
                onChange={(e) => setValue(e.target.value)}
            />
            <button type="submit" className="bg-violet-500 text-violet-50 w-10 rounded-tr-lg rounded-br-lg hover:bg-violet-600 hover:cursor-pointer">
                <FontAwesomeIcon icon={faMagnifyingGlass} />
            </button>
        </form>
    );
}