import cc from 'clsx';
import { useCallback, useEffect, useMemo, useRef, useState } from 'preact/hooks';
import { type SlInput } from '@shoelace-style/shoelace';
import { IconButton, Input, Tag } from '../shoelace.js';
import './TagInput.css';
import { type WithClass } from '~/utils/withClass';

type TagInputProps = WithClass & {
	items: string[];
	onItems: (items: string[]) => void;
	commaSubmits: boolean;
	validationMessage?: string;
	inputProps?: Parameters<typeof Input>[0];
};

export function TagInput({
	class: _class,
	items, onItems,
	commaSubmits,
	validationMessage = '',
	inputProps = {},
}: TagInputProps) {
	const [value, setValue] = useState('');

	const prefix = useMemo(() => (
		<span slot='prefix' class='ti_tags'>
			{
				items.map((item, i) => (
					<Tag
						variant='primary'
						size={'medium'}
						removable
						class='ti_tag'
						onSlRemove={() => {
							const itemsCopy = items.slice();
							itemsCopy.splice(i, 1);
							onItems(itemsCopy);
						}}
					>
						{item}
					</Tag>
				))
			}
		</span>
	), [items]);

	const newTagCut = useCallback(() => {
		if (value !== '') {
			onItems([...items, value]);
			setValue('');
		}
	}, [items, onItems, value, setValue]);

	const onKeyDown = useCallback((ev: KeyboardEvent) => {
		if (ev.key === 'Enter' || (commaSubmits && ev.key === ',')) {
			newTagCut();
			ev.preventDefault();
		}

		if (ev.key === 'Backspace' && value === '') {
			onItems(items.slice(0, -1));
		}
	}, [items, onItems, value, newTagCut]);

	const inputRef = useRef<SlInput>(null);

	useEffect(() => {
		if (inputRef.current) {
			inputRef.current.setCustomValidity(validationMessage);
		}
	}, [validationMessage]);

	return (
		<Input
			{...inputProps}
			class={cc(_class, inputProps.class, inputProps.className, 'ti')}
			size={inputProps.size ?? 'medium'}
			value={value}
			onSlInput={ev => setValue((ev.target as SlInput).value)}
			onKeyDown={onKeyDown}
			ref={inputRef}
		>
			{prefix}
			<IconButton
				slot='suffix'
				name='plus-circle-dotted'
				label='add tag'
				onClick={newTagCut}
				class='ti_add-button'
			/>
		</Input>
	);
}
