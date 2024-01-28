import cc from 'clsx';
import type { JSX } from 'preact';
import { useMemo } from 'preact/hooks';
import './ConjunctionList.css';
import type { WithClass } from '~/utils/withClass';

const formatter = new Intl.ListFormat('en', { style: 'short', type: 'conjunction' });

type ElementPart = {
	type: 'element';
	value: string;
};

type LiteralPart = {
	type: 'literal';
	value: string;
};

type ConjunctionListProps = {
	children: string[];
	elementRender: (v: ElementPart['value']) => JSX.Element;
	literalRender: (v: LiteralPart['value']) => JSX.Element;
} & WithClass;

export function ConjunctionList({
	class: _class,
	children,
	elementRender,
	literalRender,
}: ConjunctionListProps) {
	const fragments = useMemo(() => {
		const formatted = formatter.formatToParts(children);
		return formatted;
	}, [children]);

	return (
		<ul class={cc(_class, 'cl')}>
			{
				fragments.map(f => (
					<li class='cl_item'>
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
