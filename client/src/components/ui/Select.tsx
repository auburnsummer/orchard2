import {
  faCheckCircle,
  faChevronDown,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  Label,
  Listbox,
  ListboxButton,
  ListboxOption,
  ListboxOptions,
  ListboxProps,
} from "@headlessui/react";

type SelectProps = ListboxProps & {
  data: { value: string; label: string }[];
  allowDeselect?: boolean;
  label?: string;
  className?: string;
};

export default function Select({
  data,
  label,
  allowDeselect,
  ...props
}: SelectProps) {
  return (
    <Listbox as="div" {...props}>
      {label && (
        <Label className="block text-sm/6 font-medium text-slate-900 dark:text-white">
          {label}
        </Label>
      )}
      <div className="relative mt-2">
        <ListboxButton className="grid w-full cursor-default grid-cols-1 rounded-md bg-white py-1.5 pr-2 pl-3 text-left text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus-visible:outline-2 focus-visible:-outline-offset-2 focus-visible:outline-violet-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:focus-visible:outline-violet-500">
          {({ value }) => (
            <div className="flex flex-row">
              <span>
                {data.find((item) => item.value === value)?.label ||
                  "Select..."}
              </span>
              <FontAwesomeIcon
                icon={faChevronDown}
                className="ml-auto self-center text-slate-400"
              />
            </div>
          )}
        </ListboxButton>
        <ListboxOptions
          transition
          className="absolute z-30 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg outline-1 outline-black/5 data-leave:transition data-leave:duration-100 data-leave:ease-in data-closed:data-leave:opacity-0 sm:text-sm dark:bg-gray-800 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10"
        >
          {data.map((item) => (
            <ListboxOption
              key={item.value}
              value={item.value}
              className="group relative cursor-default py-2 pr-4 pl-8 text-gray-900 select-none data-focus:bg-violet-100 data-focus:text-violet-950 data-focus:outline-hidden dark:text-white dark:data-focus:bg-violet-500"
            >
              <span className="block truncate font-normal group-data-selected:font-semibold">
                {item.label}
              </span>

              <span className="absolute inset-y-0 left-1 flex items-center pl-1.5 text-violet-600 group-not-data-selected:hidden group-data-focus:text-violet-900 dark:text-violet-400">
                <FontAwesomeIcon icon={faCheckCircle} />
              </span>
            </ListboxOption>
          ))}
        </ListboxOptions>
      </div>
    </Listbox>
  );
}
