import React from "react";
import cc from "clsx";

type TextInputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  className?: string;
  labelClassName?: string;
  inputClassName?: string;
};

export function TextInput({
  label,
  className,
  labelClassName,
  inputClassName,
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
      <div className="mt-2">
        <input
          {...props}
          className={cc(
            "block w-full rounded-md bg-white px-3 py-1.5 text-base text-slate-900 outline-1 -outline-offset-1 outline-slate-300 placeholder:text-slate-400 focus:outline-2 focus:-outline-offset-2 focus:outline-violet-500 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-slate-500 dark:focus:outline-violet-500",
            inputClassName,
          )}
        />
      </div>
    </div>
  );
}
