import cc from 'clsx';
import copy from 'clipboard-copy';
import { ConjunctionList } from './ConjunctionList';
import { DifficultyDecorator } from './DifficultyDecorator';

import "./LevelBox.css";

import type { WithClass } from '@orchard/utils/withClass';
import { useExcite } from '@orchard/hooks/useExcite';
import { LevelPreviewData } from '../EditLevel/EditLevel';
import { Icon, Animation } from '@orchard/ui';

type LevelBoxProps = {
    level: LevelPreviewData  // for now
} & WithClass;

export function LevelBox({ level, 'class': _class }: LevelBoxProps) {
    const approval = 10 as number;
    const { song, artist, authors, tags, thumb, min_bpm, max_bpm, seizure_warning } = level;

    const bpmText = min_bpm === max_bpm ? `${min_bpm} BPM` : `${min_bpm}-${max_bpm} BPM`;
    const sourceText = 'Rhythm Doctor Lounge';

    const usersIcon = authors.length > 1 ? "people-fill" : "person-fill";
    const canonicalUrl = level.url;

    const [copyEffect, exciteCopyEffect] = useExcite(1000);

    const onCopyClick = () => {
        void copy(canonicalUrl).then(exciteCopyEffect);
    };

    return (
        <article class={cc(_class, "lb")}>
            <div class="lb_imagebox">
                <img class="lb_image" src={thumb} />
                <div class="lb_overlay">
                    <div class="lb_description">
                        {
                            level.description.split('\n').map(p => <p>{p}</p>)
                        }
                    </div>
                    <div class="lb_buttons">
                        <button onClick={onCopyClick} class={cc('lb_button lb_copy', { 'clicked!lb_copy': copyEffect })}>
                            <Icon name="clipboard2-pulse-fill" class="lb_overlayicon" />
                        </button>
                        <a href={canonicalUrl} class="lb_button lb_download">
                            <Icon name="cloud-arrow-down-fill" class="lb_overlayicon" />
                        </a>
                    </div>
                </div>
            </div>

            <div class="lb_info">
                <DifficultyDecorator {...level} class="lb_decorator" />
                <div class="lb_cast">
                    <h1 class="lb_song">{song}</h1>
                    <h2 class="lb_artist">{artist}</h2>
                </div>
                <div class="lb_metadata">
                    <div class="lb_metaitem lb_authors">
                        <Icon name={usersIcon} class="lb_metaicon" />
                        <ConjunctionList
                            class="lb_author-list"
                            elementRender={(v) => (
                                    <button
                                        disabled
                                        onClick={() => {}}
                                        class="lb_metabutton"
                                    >
                                        {v}
                                    </button>
                            )}
                            literalRender={(v) => <span class="lb_metatext">{v}</span>}
                        >
                            {authors}
                        </ConjunctionList>
                    </div>
                    <div class="lb_metaitem lb_bpm">
                        <Icon name="heart-pulse-fill" class="lb_metaicon" />
                        <span class="lb_metatext lb_bpm-text">{bpmText}</span>
                    </div>
                    <div class="lb_metaitem lb_source">
                        <Icon library="fa" name="fab-discord" class="lb_metaicon" />
                        <button disabled class="lb_metabutton lb_source-button">{sourceText}</button>
                    </div>
                    <div
                        class={cc(
                            'lb_metaitem lb_approval',
                            { 'yay!lb_approval' : approval >= 10,
                                'nope!lb_approval' : approval < 0,
                                'umm!lb_approval' : approval === 0
                            }
                        )}
                    >
                        {
                            approval >= 10 ? (
                                <span title={'Peer-Reviewed: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability.'}>
                                    <Icon name="check" class="lb_metaicon" />
                                </span>
                            ) : approval < 0 ? (
                                <span title={'Non-Referred: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability, and has found that this level does not meet standards.'}>
                                    <Icon name="x" class="lb_metaicon" />
                                </span>
                            ) : null
                        }
                    </div>
                </div>
                <div class="lb_spacer">

                </div>
                <ul class="lb_tags">
                    {
                        seizure_warning && (
                            <li>
                                <button class="caution!lb_tag lb_tag" disabled>
                                    <Icon name="exclamation-triangle-fill" class="lb_metaicon" />
                                    <span title="ayaya seizure warning">Seizure warning</span>
                                </button>
                            </li>
                        )
                    }
                    {
                        tags.map(tag => (
                            <li>
                                <button
                                    disabled
                                    class="lb_tag">
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