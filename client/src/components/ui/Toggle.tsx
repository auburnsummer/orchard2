import React from "react";
import cc from "clsx";

type ToggleProps = Omit<React.ComponentPropsWithRef<'input'>, 'type'> & {
  label?: string;
  className?: string;
  labelClassName?: string;
  description?: string;
};

export function Toggle({
  label,
  className,
  labelClassName,
  description,
  id,
  ...props
}: ToggleProps) {
  const labelId = id ? `${id}-label` : undefined;
  const descriptionId = id && description ? `${id}-description` : undefined;

  return (
    <div className={cc("flex items-center justify-between gap-3", className)}>
      <div className="group relative inline-flex w-11 shrink-0 rounded-full bg-slate-200 p-0.5 inset-ring inset-ring-slate-900/5 outline-offset-2 outline-violet-600 transition-colors duration-200 ease-in-out has-checked:bg-violet-600 has-focus-visible:outline-2 dark:bg-white/5 dark:inset-ring-white/10 dark:outline-violet-500 dark:has-checked:bg-violet-500 cursor-pointer">
        <span className="size-5 rounded-full bg-white shadow-xs ring-1 ring-slate-900/5 transition-transform duration-200 ease-in-out group-has-checked:translate-x-5" />
        <input
          {...props}
          id={id}
          type="checkbox"
          aria-labelledby={labelId}
          aria-describedby={descriptionId}
          className="absolute inset-0 appearance-none focus:outline-hidden cursor-pointer"
        />
      </div>

      {(label || description) && (
        <div className="text-sm">
          {label && (
            <label id={labelId} htmlFor={id} className={cc("font-medium text-slate-900 dark:text-white cursor-pointer", labelClassName)}>
              {label}
            </label>
          )}
          {label && description && ' '}
          {description && (
            <span id={descriptionId} className="text-slate-500 dark:text-slate-400">
              {description}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

