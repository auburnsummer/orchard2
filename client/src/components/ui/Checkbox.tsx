import React from "react";
import cc from "clsx";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck } from "@fortawesome/free-solid-svg-icons";

type CheckboxProps = Omit<React.ComponentPropsWithRef<'input'>, 'type'> & {
  label?: string;
  className?: string;
  labelClassName?: string;
  description?: string;
};

export function Checkbox({
  label,
  className,
  labelClassName,
  description,
  id,
  ...props
}: CheckboxProps) {
  const labelId = id ? `${id}-label` : undefined;
  const descriptionId = id && description ? `${id}-description` : undefined;

  return (
    <div className={cc("flex items-start gap-3", className)}>
      <div className="flex h-6 items-center">
        <div className="group relative">
          <input
            {...props}
            id={id}
            type="checkbox"
            aria-labelledby={labelId}
            aria-describedby={descriptionId}
            className="peer size-4 appearance-none rounded border border-slate-300 bg-white transition-colors duration-150 checked:border-violet-500 checked:bg-violet-500 hover:border-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-600 dark:bg-slate-800 dark:checked:border-violet-600 dark:checked:bg-violet-600 dark:hover:border-slate-500 dark:focus:ring-violet-600 dark:focus:ring-offset-slate-900"
          />
          <FontAwesomeIcon
            icon={faCheck}
            className="pointer-events-none absolute left-0.5 top-0.5 size-3 text-white scale-0 transition-transform duration-150 peer-checked:scale-100"
          />
        </div>
      </div>

      {(label || description) && (
        <div className="text-sm">
          {label && (
            <label id={labelId} htmlFor={id} className={cc("font-medium text-slate-900 dark:text-white cursor-pointer", labelClassName)}>
              {label}
            </label>
          )}
          {description && (
            <p id={descriptionId} className="mt-0.5 text-slate-500 dark:text-slate-400">
              {description}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
