import cc from 'clsx';
import copy from 'clipboard-copy';
import { ConjunctionList } from './ConjunctionList';
import { DifficultyDecorator } from './DifficultyDecorator';
import './LevelBox.css';
import type { WithClass } from '~/utils/withClass';
import { useExcite } from '~/hooks/useExcite';
import { Icon } from '~/ui';
import { type RDLevel } from '~/api/levels/schemas';
import { useState } from 'preact/hooks';

type LevelBoxProps = {
	level: RDLevel;
} & WithClass;

export function LevelBox({ level, class: _class }: LevelBoxProps) {
	const { approval, song, song_alt, artist_tokens, authors, tags, thumb, min_bpm, max_bpm, seizure_warning } = level;

	const bpmText = min_bpm === max_bpm ? `${min_bpm} BPM` : `${min_bpm}-${max_bpm} BPM`;
	const sourceText = level.publisher.name;

	const usersIcon = authors.length > 1 ? 'people-fill' : 'person-fill';
	const canonicalUrl = level.url;

	const [copyEffect, setCopyEffect] = useState(false);

	const onCopyClick = () => {
		void copy(canonicalUrl);
		setCopyEffect(false);
		setTimeout(() => setCopyEffect(true), 0);
	};

	return (
		<article class={cc(_class, 'lb')}>
			<div class='lb_imagebox'>
				<img class='lb_image' src={thumb} loading='lazy' />
				<div class='lb_overlay'>
					<div class='lb_description'>
						{
							level.description.split('\n').map(p => <p>{p}</p>)
						}
					</div>
					<div class='lb_buttons'>
						<button onClick={onCopyClick} class={cc('lb_button lb_copy', { 'clicked!lb_copy': copyEffect })}>
							<Icon name='clipboard2-pulse-fill' class='lb_overlayicon' />
						</button>
						<a href={canonicalUrl} class='lb_button lb_download'>
							<Icon name='cloud-arrow-down-fill' class='lb_overlayicon' />
						</a>
					</div>
				</div>
			</div>

			<div class='lb_info'>
				<DifficultyDecorator {...level} class='lb_decorator' />
				<div class='lb_cast'>
					<div class='lb_song-wrapper'>
						<h1 class='lb_song'>{song}</h1>
						{song_alt && <h2 class='lb_songalt'>({song_alt})</h2>}
					</div>
					<div class='lb_artist-wrapper'>
						<ConjunctionList
							class='lb_artist-list'
							elementRender={v => (
								<h2
									class='lb_artist'
								>
									{v}
								</h2>
							)}
							literalRender={v => <span class='lb_artist-literal'>{v}</span>}
						>
							{artist_tokens}
						</ConjunctionList>
					</div>
				</div>
				<div class='lb_metadata'>
					<div class='lb_metaitem lb_authors'>
						<Icon name={usersIcon} class='lb_metaicon' />
						<ConjunctionList
							class='lb_author-list'
							elementRender={v => (
								<button
									disabled
									onClick={() => {}}
									class='lb_metabutton'
								>
									{v}
								</button>
							)}
							literalRender={v => <span class='lb_metatext'>{v}</span>}
						>
							{authors}
						</ConjunctionList>
					</div>
					<div class='lb_metaitem lb_bpm'>
						<Icon name='heart-pulse-fill' class='lb_metaicon' />
						<span class='lb_metatext lb_bpm-text'>{bpmText}</span>
					</div>
					<div class='lb_metaitem lb_source'>
						<Icon library='fa' name='fab-discord' class='lb_metaicon' />
						<button disabled class='lb_metabutton lb_source-button'>{sourceText}</button>
					</div>
					<div
						class={cc(
							'lb_metaitem lb_approval',
							{ 'yay!lb_approval': approval >= 10,
								'nope!lb_approval': approval < 0,
								'umm!lb_approval': approval === 0,
							},
						)}
					>
						{
							approval >= 10 ? (
								<span title={'Peer-Reviewed: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability.'}>
									<Icon name='check' class='lb_metaicon' />
								</span>
							) : (approval < 0 ? (
								<span title={'Non-Referred: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability, and has found that this level does not meet standards.'}>
									<Icon name='x' class='lb_metaicon' />
								</span>
							) : null)
						}
					</div>
				</div>
				<div class='lb_spacer'>

				</div>
				<ul class='lb_tags'>
					{
						seizure_warning && (
							<li>
								<button class='caution!lb_tag lb_tag' disabled>
									<Icon name='exclamation-triangle-fill' class='lb_metaicon' />
									<span title='ayaya seizure warning'>Seizure warning</span>
								</button>
							</li>
						)
					}
					{
						tags.map(tag => (
							<li>
								<button
									disabled
									class='lb_tag'>
									{tag}
								</button>
							</li>
						))
					}
				</ul>
			</div>
		</article>
	);
}
