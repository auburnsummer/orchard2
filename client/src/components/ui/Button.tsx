
type Variant = "default" | "primary" | "secondary" | "danger";

const variantStyles: Record<Variant, string> = {
    default: "p-1 bg-slate-200 text-slate-900 hover:bg-slate-300 dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600 rounded-lg hover:cursor-pointer",
    primary: "p-1 bg-violet-500 text-white hover:bg-violet-600 rounded-lg hover:cursor-pointer",
    secondary: "p-1 bg-slate-500 text-white hover:bg-slate-600 rounded-lg hover:cursor-pointer",
    danger: "p-1 bg-red-500 text-white hover:bg-red-600 rounded-lg hover:cursor-pointer",
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