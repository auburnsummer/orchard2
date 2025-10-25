import React from "react";
import cc from "clsx";

type RadioProps = Omit<React.ComponentPropsWithRef<'input'>, 'type'> & {
  label?: React.ReactNode;
  className?: string;
  labelClassName?: string;
  description?: string;
};

export function Radio({
  label,
  className,
  labelClassName,
  description,
  id,
  ...props
}: RadioProps) {
  const labelId = id ? `${id}-label` : undefined;
  const descriptionId = id && description ? `${id}-description` : undefined;

  return (
    <div className={cc("flex items-start gap-3", className)}>
      <div className="flex h-6 items-center">
        <div className="group relative">
          <input
            {...props}
            id={id}
            type="radio"
            aria-labelledby={labelId}
            aria-describedby={descriptionId}
            className="relative size-4 appearance-none rounded-full border border-slate-300 bg-white transition-all duration-150 before:absolute before:inset-1 before:rounded-full before:bg-white not-checked:before:hidden checked:border-violet-600 checked:bg-violet-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-600 disabled:border-slate-300 disabled:bg-slate-100 disabled:before:bg-slate-400 dark:border-white/10 dark:bg-white/5 dark:checked:border-violet-500 dark:checked:bg-violet-500 dark:focus-visible:outline-violet-500 dark:disabled:border-white/5 dark:disabled:bg-white/10 dark:disabled:before:bg-white/20 forced-colors:appearance-auto forced-colors:before:hidden"
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
