import React from "react";
import cc from "clsx";

type TextInputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  className?: string;
  labelClassName?: string;
  inputClassName?: string;
  description?: string;
  rightSlot?: React.ReactNode;
};

export function TextInput({
  label,
  className,
  labelClassName,
  inputClassName,
  description,
  rightSlot,
  ...props
}: TextInputProps) {
  return (
    <div className={className}>
      <label
        htmlFor={props.id}
        className={cc(
          "block text-sm/6 font-medium text-slate-900 dark:text-white",
          labelClassName,
        )}
      >
        {label}
      </label>
      <div className="mt-2 grid grid-cols-1">
        <input
          {...props}
          className={cc(
            "col-start-1 row-start-1 block w-full rounded-md bg-white px-3 py-1.5 text-base text-slate-900 outline-1 -outline-offset-1 outline-slate-300 placeholder:text-slate-400 focus:outline-2 focus:-outline-offset-2 focus:outline-violet-500 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-slate-500 dark:focus:outline-violet-500 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500 disabled:outline-slate-200 dark:disabled:bg-white/10 dark:disabled:text-gray-500 dark:disabled:outline-white/5",
            inputClassName,
          )}
        />
        {rightSlot && <div className="col-start-1 row-start-1 justify-self-end self-center">{rightSlot}</div>}
      </div>
      {description && (
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400 font-light">
          {description}
        </p>
      )}
    </div>
  );
}
