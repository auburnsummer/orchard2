import cc from 'clsx';
import type { TargetedEvent } from 'preact/compat';
import { useComputed } from '@preact/signals';
import { type SlButton } from '@shoelace-style/shoelace';
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

	return (
		<div class={cc(_class, 'se')}>
			<form class='se_bar' {...formProps}>
				<Input
					name='search'
					class='se_input'
					placeholder='Search'
				/>
				<Button type='submit'>
					<Icon name='search' />
				</Button>
			</form>
		</div>
	);
}
