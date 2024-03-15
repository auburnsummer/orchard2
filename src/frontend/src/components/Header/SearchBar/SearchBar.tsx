import cc from 'clsx';
import { object, string } from 'valibot';
import './SearchBar.css';
import { type WithClass } from '~/utils/withClass';
import { Button, Input, Icon } from '~/ui';
import { fetchResults$ } from '~/signals/searchResults';
import { rdSearchParams$, setSearchParams } from '~/signals/searchParams';
import { useForm } from '~/hooks/useForm';

type SearchBarProperties = WithClass;

const searchBarFormContentsSchema = object({
	search: string(),
});

export function SearchBar({ class: _class }: SearchBarProperties) {
	const formProps = useForm(searchBarFormContentsSchema, ({ search }) => {
		setSearchParams(d => {
			d.q = search;
		});
		void fetchResults$.value(true);
	});

	const rdSearchParams = rdSearchParams$.value;

	return (
		<div class={cc(_class, 'se')}>
			<form class='se_bar' {...formProps}>
				<Input
					name='search'
					class='se_input'
					placeholder='Search'
					// Note value is only one-way bounded here, so as soon as the user types something,
					// the value in the input is different from rdSearchParams.q. but then rdSearchParams
					// is re-rendered (e.g. by a popstate), this component rerenders and changes the visible
					// value back to sync.
					value={rdSearchParams.q ?? ''}
				/>
				<Button type='submit'>
					<Icon name='search' />
				</Button>
			</form>
		</div>
	);
}
