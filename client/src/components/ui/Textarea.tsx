import { TextareaHTMLAttributes } from "react";

type TextareaProps = TextareaHTMLAttributes<HTMLTextAreaElement> & {
  className?: string;
  label?: string;
  description?: string;
};

export default function Textarea({
  label,
  className,
  description,
  ...props
}: TextareaProps) {
  return (
    <div className={className}>
      {label && (
        <label
          htmlFor={props.id}
          className="block text-sm/6 font-medium text-slate-900 dark:text-white"
        >
          {label}
        </label>
      )}
      <div className="mt-2">
        <textarea
          id={props.id}
          name={props.name}
          rows={4}
          className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-slate-900 outline-1 -outline-offset-1 outline-slate-300 placeholder:text-slate-400 focus:outline-2 focus:-outline-offset-2 focus:outline-violet-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-slate-500 dark:focus:outline-violet-500"
          {...props}
        />
      </div>
      {description && (
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400 font-light">
          {description}
        </p>
      )}
    </div>
  );
}
