import cc from 'clsx';
import { useCallback, useRef } from 'preact/hooks';
import type { SlCheckbox, SlDialog, SlInput } from '@shoelace-style/shoelace';
import { useComputed, useSignal } from '@preact/signals';
import { type Draft, produce } from 'immer';
import { LevelBox } from '../LevelBox';
import './EditLevel.css';
import { type WithClass } from '~/utils/withClass';
import { Input, Select, TagInput, Textarea, Option, Checkbox, Button, Divider, Dialog } from '~/ui';
import type { Publisher } from '~/api/publisher';
import { type AddRDLevelPayload, type RDLevel, type RDPrefillResult } from '~/api/levels/schemas';

type EditLevelProps = WithClass & {
	levelPrefill: RDPrefillResult;
	publisher: Publisher;
	onSubmit: (payload: AddRDLevelPayload) => void;
};

const initialAdditionalLevelState = {
	song_alt: '',
};

export function EditLevel({ class: _class, levelPrefill, publisher, onSubmit }: EditLevelProps) {
	const preview$ = useSignal({
		...levelPrefill,
		...initialAdditionalLevelState,
	});

	const resetPreview = useCallback(() => {
		preview$.value = {
			...levelPrefill,
			...initialAdditionalLevelState,
		};
	}, [levelPrefill]);

	const setPreview = useCallback((draftFunc: (draft: Draft<RDLevel>) => void) => {
		preview$.value = produce(preview$.value, draftFunc);
	}, []);

	const levelPreviewDialog = useRef<SlDialog>(null);

	const merged$ = useComputed(() => ({
		...levelPrefill,
		...preview$.value,
		id: 'rd_preview',
		uploader: {
			id: 'u_preview',
			name: 'Preview',
			avatar_url: null,
		},
		publisher,
		uploaded: new Date().toISOString(),
		approval: 0,
	}));

	return (
		<div class={cc(_class, 'el')}>
			<Dialog
				class='el_level-preview-smallscreens'
				ref={levelPreviewDialog}
			>
				<LevelBox level={merged$.value} />
			</Dialog>
			<div class='el_too-small'>
				<p class='el_too-small-message'>Please increase the size of the web browser</p>
			</div>
			<div class='el_wrapper'>
				{/*
                    nit: we should make this an actual form at some point. the current issue is that
                    TagInput does not behave like a form control
                */}
				<div class='el_form'>
					<div class='el_controls'>
						<Button
							class='el_reset-button'
							variant='text'
							size='small'
							onClick={resetPreview}
						>
                            Reset form
						</Button>
						<div class='el_controls-spacer' />
						<Button
							class='el_preview-button'
							onClick={() => {
								void levelPreviewDialog.current?.show();
							}}
						>
                            Show preview
						</Button>
						{/* not type submit, it's too easy for a stray enter to submit the form */}
						<Button
							class='el_submit-button'
							onClick={_ => onSubmit(preview$.value)}
						>
                            Submit
						</Button>
					</div>
					<Divider class='el_control-title-divider' />
					<div class='el_titles'>
						<Input
							class='el_title'
							label='Song'
							value={preview$.value.song}
							onSlInput={event => setPreview(d => {
								d.song = (event.target as SlInput).value;
							})}
						/>
						<Input
							class='el_title'
							label='Song alternate name (optional)'
							value={preview$.value.song_alt}
							onSlInput={event => setPreview(d => {
								d.song_alt = (event.target as SlInput).value;
							})}
						/>
					</div>
					<TagInput
						class='el_artists'
						items={preview$.value.artist_tokens}
						onItems={items => setPreview(d => {
							d.artist_tokens = items;
						})}
						commaSubmits={false}
						inputProps={{
							label: preview$.value.artist_tokens.length === 1 ? 'Artist' : 'Artists',
						}}
					/>
					<TagInput
						class='el_authors'
						items={preview$.value.authors}
						onItems={items => setPreview(d => {
							d.authors = items;
						})}
						commaSubmits={true}
						inputProps={{
							label: preview$.value.authors.length === 1 ? 'Author' : 'Authors',
						}}
					/>
					<Textarea
						class='el_description'
						value={preview$.value.description}
						label='Description'
						onSlInput={ev => setPreview(d => {
							d.description = (ev.target as SlInput).value;
						})}
					/>
					<div class='el_bpm-and-difficulty-section'>
						<Input
							class='el_bpm'
							step='any'
							value={`${preview$.value.min_bpm}`}
							type='number'
							label='Min BPM'
							onSlInput={ev => setPreview(d => {
								d.min_bpm = Number.parseFloat((ev.target as SlInput).value);
								if (d.max_bpm < d.min_bpm) {
									d.max_bpm = d.min_bpm;
								}
							})}
						/>
						<Input
							class='el_bpm'
							step='any'
							value={`${preview$.value.max_bpm}`}
							type='number'
							label='Max BPM'
							onSlInput={ev => setPreview(d => {
								d.max_bpm = Number.parseFloat((ev.target as SlInput).value);
								if (d.min_bpm > d.max_bpm) {
									d.min_bpm = d.max_bpm;
								}
							})}
						/>
						<Select
							label='Difficulty'
							value={`${preview$.value.difficulty}`}
							class='el_difficulty'
							onSlChange={ev => setPreview(d => {
								d.difficulty = Number.parseInt((ev.target as SlInput).value, 10);
							})}
						>
							<Option value='0'>Easy</Option>
							<Option value='1'>Medium</Option>
							<Option value='2'>Tough</Option>
							<Option value='3'>Very Tough</Option>
						</Select>
					</div>
					<TagInput
						class='el_tags'
						items={preview$.value.tags}
						onItems={items => setPreview(d => {
							d.tags = items;
						})}
						commaSubmits={true}
						inputProps={{
							label: 'Tags',
						}}
					/>
					<div class='el_checkboxes'>
						<Checkbox
							checked={preview$.value.seizure_warning}
							onSlInput={ev => setPreview(d => {
								d.seizure_warning = (ev.target as SlCheckbox).checked;
							})}
						>
                            Seizure warning
						</Checkbox>
						<Checkbox
							checked={preview$.value.single_player}
							onSlInput={ev => setPreview(d => {
								d.single_player = (ev.target as SlCheckbox).checked;
							})}
						>
                            Supports single player
						</Checkbox>
						<Checkbox
							checked={preview$.value.two_player}
							onSlInput={ev => setPreview(d => {
								d.two_player = (ev.target as SlCheckbox).checked;
							})}
						>
                            Supports two player
						</Checkbox>
						{
							([
								['classics', 'Contains classics'],
								['oneshots', 'Contains oneshots'],
								['squareshots', 'Contains squareshots'],
								['freezeshots', 'Contains freezeshots'],
								['freetimes', 'Contains freetimes'],
								['holds', 'Contains holds'],
								['skipshots', 'Contains skipshots'],
								['window_dance', 'Uses window dance'],
							] as const).map(([tag, s]) => (
								<Checkbox
									checked={preview$.value[`has_${tag}`]}
									onSlInput={ev => setPreview(d => {
										d[`has_${tag}`] = (ev.target as SlCheckbox).checked;
									})}
								>
									{s}
								</Checkbox>
							))
						}
					</div>
				</div>
				<div class='el_preview'>
					<LevelBox level={merged$.value} />
				</div>
			</div>
		</div>
	);
}
