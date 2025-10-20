import cc from "clsx";
import React from "react";

type Variant = "default" | "muted" | "header";

const variantStyles: Record<Variant, string> = {
    default: "text-slate-900 dark:text-slate-100",
    muted: "text-slate-600 dark:text-slate-400",
    header: "text-lg font-semibold text-slate-900 dark:text-slate-100",
}

type WordsBaseProps = {
    children: React.ReactNode;
    className?: string;
    variant?: Variant;
}

type WordsProps<T extends React.ElementType = "span"> = WordsBaseProps & {
    as?: T;
} & Omit<React.ComponentPropsWithoutRef<T>, keyof WordsBaseProps | 'as'>;

export function Words<T extends React.ElementType = "span">({ children, className, as, variant = "default" }: WordsProps<T>) {
    const Component = as || "span";
    return (
        <Component className={cc(variantStyles[variant], className)}>
            {children}
        </Component>
    )
}
