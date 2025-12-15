import React from 'react';
import cc from 'clsx';

// Base props that are always available on NavEntry
type NavEntryBaseProps = {
  children: React.ReactNode;
  className?: string;
  active?: boolean;
};

// Polymorphic component props that merge base props with the props of the element type
type NavEntryProps<T extends React.ElementType = 'button'> = NavEntryBaseProps & {
  as?: T;
} & Omit<React.ComponentPropsWithoutRef<T>, keyof NavEntryBaseProps | 'as'>;

// The component implementation
export function NavEntry<T extends React.ElementType = 'button'>({
  as,
  active,
  children,
  className,
  ...props
}: NavEntryProps<T>) {
  const Component = as || 'button';
  
  return (
    <Component
      className={cc("block w-full px-4 py-2 text-left text-sm text-slate-700 data-focus:cursor-pointer hover:cursor-pointer data-focus:bg-violet-50 hover:bg-violet-50 data-focus:text-violet-900 hover:text-violet-900 data-focus:outline-hidden hover:outline-hidden dark:text-slate-300 dark:data-focus:bg-white/5 dark:hover:bg-white/5 dark:data-focus:text-white dark:hover:text-white", className, { "bg-violet-100 dark:bg-white/10": active })}
      {...props}
    >
      {children}
    </Component>
  );
}