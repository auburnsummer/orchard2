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
		// We should never render this state bc HomeContents won't render LevelList if it has an error.
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
			<div class={cc('le_content', { 'loading!le_content': searchResultsLoading })}>
				<div class='le_controls'>
					<button>Next page</button>
					<button>Previous page</button>
				</div>
				<ul class='le_levels'>
				{
					searchResultsCombined.data.levels.map(level => (
						<LevelBox level={level} key={level.id} class='le_level' />
					))
				}
			</ul>
			</div>

		</div>
	);
}
