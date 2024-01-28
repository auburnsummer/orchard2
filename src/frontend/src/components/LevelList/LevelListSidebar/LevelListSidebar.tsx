import cc from 'clsx';
import './LevelListSidebar.css';
import { type WithClass } from '~/utils/withClass';

type LevelListSidebarProperties = WithClass;

export function LevelListSidebar({ class: _class }: LevelListSidebarProperties) {
	return (
		<div class={cc(_class, 'ls')}>
            Level list sidebar
		</div>
	);
}
