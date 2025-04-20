import cc from 'clsx';

import styles from "./ConjunctionList.module.css";
import { useMemo } from 'react';

const formatter = new Intl.ListFormat('en', { style: 'short', type: 'conjunction' });

type ConjunctionListProps = React.HTMLAttributes<HTMLUListElement> & {
    items: string[];
    elementRender: (v: string) => JSX.Element;
    literalRender: (v: string) => JSX.Element;
};

export function ConjunctionList({
    className,
    items,
    elementRender,
    literalRender,
    ...rest
}: ConjunctionListProps) {

    const fragments = useMemo(() => {
        const formatted = formatter.formatToParts(items);
        return formatted;
    }, [items]);

    return (
        <ul className={cc(className, styles.base)} {...rest}>
            {
                fragments.map(f => (
                    <li>
                        {
                            f.type === 'element'
                                ? elementRender(f.value)
                                : literalRender(f.value)
                        }
                    </li>
                ))
            }
        </ul>
    );
}