import cc from 'clsx';
import './Loading.css';
import { type WithClass } from '~/utils/withClass';
import { Spinner } from '~/ui';

type LoadingProps = WithClass & {
	text: string;
};

export function Loading({ class: _class, text }: LoadingProps) {
	return (
		<div class={cc(_class, 'lo')}>
			<Spinner class='lo_spinner' />
			<span class='lo_text'>{text}</span>
		</div>
	);
}
