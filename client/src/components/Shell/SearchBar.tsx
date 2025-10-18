import React from "react";

import cc from "clsx";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";

type SearchBarProps = React.HTMLAttributes<HTMLDivElement> & {
  placeholder?: string;
  initialValue?: string;
  onSearch?: (query: string) => void;
};

export function SearchBar({
  placeholder,
  className,
  onSearch,
  initialValue,
}: SearchBarProps) {
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
    <form
      className={cc("my-1 flex rounded-tl-lg rounded-bl-lg", className)}
      onSubmit={onSubmit}
    >
      <input
        className="rounded-tl-lg rounded-bl-lg bg-violet-50 dark:bg-slate-800 px-3 outline-none focus:inset-ring-2 focus:inset-ring-violet-200 active:bg-white focus:bg-white placeholder:text-violet-400 text-sm dark:placeholder:text-slate-400 dark:active:bg-slate-700 dark:focus:bg-slate-700 dark:text-white"
        type="text"
        placeholder={placeholder}
        defaultValue={initialValue}
        onChange={(e) => setValue(e.target.value)}
      />
      <button
        type="submit"
        className="w-10 rounded-tr-lg rounded-br-lg bg-violet-500 text-violet-50 hover:cursor-pointer hover:bg-violet-600"
      >
        <FontAwesomeIcon icon={faMagnifyingGlass} />
      </button>
    </form>
  );
}
