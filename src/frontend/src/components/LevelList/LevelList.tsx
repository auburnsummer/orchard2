import cc from 'clsx';
import { LevelBox } from '../LevelBox';
import { Loading } from '../Loading';
import './LevelList.css';
import { LevelListSidebar } from './LevelListSidebar';
import { searchResultsCombined$, searchResultsLoading$ } from '~/signals/searchResults';
import { type WithClass } from '~/utils/withClass';

type LevelListProperties = WithClass;

export function LevelList({ class: _class }: LevelListProperties) {
	const searchResultsCombined = searchResultsCombined$.value;

	if (searchResultsCombined.state === 'has error') {
		// We should never render this state bc HomeContents guards.
		return <></>;
	}

	if (searchResultsCombined.state === 'loading') {
		return (
			<Loading text='loading' />
		);
	}

	const searchResultsLoading = searchResultsLoading$.value;

	return (
		<div class={cc(_class, 'le')}>
			<LevelListSidebar class='le_sidebar' />
			<ul class={cc('le_levels', { 'loading!le_levels': searchResultsLoading })}>
				{
					searchResultsCombined.data.levels.map(level => (
						<LevelBox level={level} key={level.id} class='le_level' />
					))
				}
			</ul>
		</div>
	);
}
