import cc from "clsx";

type SurfaceProps = {
    children: React.ReactNode;
    className?: string;
}

export function Surface({ children, className }: SurfaceProps) {
    return (
        <div className={cc("bg-slate-50 dark:bg-slate-800 shadow-sm rounded-lg", className)}>
            {children}
        </div>
    )
}