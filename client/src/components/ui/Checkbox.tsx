import React, { useId, useRef } from "react";
import cc from "clsx";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { useTooltip } from "@cafe/hooks/useTooltip";

type CheckboxProps = Omit<React.ComponentPropsWithRef<'input'>, 'type'> & {
  label?: string | React.ReactNode;
  className?: string;
  labelClassName?: string;
  description?: string;
  showDescriptionAsTooltip?: boolean;
};

export function Checkbox({
  label,
  className,
  labelClassName,
  description,
  id,
  showDescriptionAsTooltip = false,
  ...props
}: CheckboxProps) {
  const generatedId = useId();
  const checkboxId = id ?? generatedId;
  const labelId = `${checkboxId}-label`;
  const descriptionId = description ? `${checkboxId}-description` : undefined;
  const wrapperRef = useRef<HTMLDivElement>(null);
  const tooltip = useTooltip();

  const handleMouseEnter = () => {
    if (showDescriptionAsTooltip && description && wrapperRef.current) {
      tooltip.show(description, wrapperRef.current);
    }
  };

  const handleMouseLeave = () => {
    if (showDescriptionAsTooltip && description) {
      tooltip.hide();
    }
  };

  return (
    <div 
      ref={wrapperRef}
      className={cc("flex items-start gap-3", className)}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="flex h-6 items-center">
        <div className="group relative">
          <input
            {...props}
            id={checkboxId}
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
            <label 
              id={labelId} 
              htmlFor={checkboxId} 
              className={cc("font-medium text-slate-900 dark:text-white cursor-pointer", labelClassName)}
            >
              {label}
            </label>
          )}
          {!showDescriptionAsTooltip && description && (
            <p id={descriptionId} className="mt-0.5 text-slate-500 dark:text-slate-400">
              {description}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
