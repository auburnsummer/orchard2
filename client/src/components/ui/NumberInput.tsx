import React from "react";
import cc from "clsx";

type NumberInputProps = {
    label?: string;
    value: number;
    min?: number;
    max?: number;
    step?: number;
    onChange: (value: number | undefined) => void;
    className?: string;
    labelClassName?: string;
    inputClassName?: string;
    description?: string;
    id?: string;
    placeholder?: string;
    disabled?: boolean;
}

export function NumberInput({
    label,
    className,
    labelClassName,
    inputClassName,
    description,
    value,
    min,
    max,
    step = 1,
    onChange,
    id,
    placeholder,
    disabled,
}: NumberInputProps) {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const val = e.target.value;
        if (val === '') {
            onChange(undefined);
        } else {
            const numVal = parseFloat(val);
            if (!isNaN(numVal)) {
                onChange(numVal);
            }
        }
    };

    return (
        <div className={className}>
            {label && (
                <label
                    htmlFor={id}
                    className={cc(
                        "block text-sm/6 font-medium text-slate-900 dark:text-white",
                        labelClassName,
                    )}
                >
                    {label}
                </label>
            )}

            <div className="mt-2">
                <input
                    type="number"
                    id={id}
                    value={value}
                    min={min}
                    max={max}
                    step={step}
                    onChange={handleChange}
                    placeholder={placeholder}
                    disabled={disabled}
                    className={cc(
                        "block w-full rounded-md bg-white px-3 py-1.5 text-base text-slate-900 outline-1 -outline-offset-1 outline-slate-300 placeholder:text-slate-400 focus:outline-2 focus:-outline-offset-2 focus:outline-violet-500 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-slate-500 dark:focus:outline-violet-500 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-500 disabled:outline-slate-200 dark:disabled:bg-white/10 dark:disabled:text-gray-500 dark:disabled:outline-white/5",
                        inputClassName,
                    )}
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
