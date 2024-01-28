import cc from 'clsx';
import type { TargetedEvent } from 'preact/compat';
import { useComputed } from '@preact/signals';
import { type SlButton } from '@shoelace-style/shoelace';
import './SearchBar.css';
import { type WithClass } from '~/utils/withClass';
import { Button, Input, Icon } from '~/ui';
import { fetchResults$ } from '~/signals/searchResults';
import { rdSearchParams$, setSearchParams } from '~/signals/searchParams';

type SearchBarProperties = WithClass;

export function SearchBar({ class: _class }: SearchBarProperties) {
	const onSubmit = (e: TargetedEvent<SlButton>) => {
		e.preventDefault();
		void fetchResults$.value(true);
	};

	const q$ = useComputed(() => rdSearchParams$.value.q);

	return (
		<div class={cc(_class, 'se')}>
			<div class='se_bar'>
				<Input
					value={q$.value ?? ''}
					onInput={event => setSearchParams(d => {
						d.q = event.currentTarget.value;
					})}
					class='se_input'
					placeholder='Search'
				/>
				<Button onClick={onSubmit}>
					<Icon name='search' />
				</Button>
			</div>
		</div>
	);
}
