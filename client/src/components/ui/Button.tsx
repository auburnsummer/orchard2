
type Variant = "default" | "primary" | "secondary" | "danger";

const commonStyles = `
    rounded-lg hover:cursor-pointer text-sm font-semibold px-3 py-2 shadow-xs
    disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150
`;

const variantStyles: Record<Variant, string> = {
    default: `${commonStyles} bg-slate-200 text-slate-900 hover:bg-slate-300 dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600`,
    primary: `${commonStyles} bg-violet-500 text-white hover:bg-violet-600 dark:bg-violet-600 dark:hover:bg-violet-700`,
    secondary: `${commonStyles} bg-slate-500 text-white hover:bg-slate-600`,
    danger: `${commonStyles} bg-red-500 text-white hover:bg-red-600`,

}

type ButtonBaseProps = {
    children: React.ReactNode;
    className?: string;
    variant?: Variant;
}

type ButtonProps<T extends React.ElementType = 'button'> = ButtonBaseProps & {
    as?: T;
} & Omit<React.ComponentPropsWithoutRef<T>, keyof ButtonBaseProps | 'as'>;

export function Button<T extends React.ElementType = 'button'>({
    as,
    children,
    className,
    variant = "default",
    ...props
}: ButtonProps<T>) {
    const Component = as || 'button';
    return (
        <Component className={`${className} ${variantStyles[variant]}`} {...props}>
            {children}
        </Component>
    );
}