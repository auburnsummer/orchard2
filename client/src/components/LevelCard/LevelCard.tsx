import { RDLevel } from "@cafe/types/rdLevelBase"

import cc from "clsx";
import styles from "./LevelCard.module.css";

import { Group, Text, UnstyledButton } from "@mantine/core";
import { useClipboard } from '@mantine/hooks';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faDownload, faExclamationTriangle, faHeartPulse, faPaste, faPen, faPerson, faX, faXmark } from "@fortawesome/free-solid-svg-icons";
import { DifficultyDecorator } from "./DifficultyDecorator/DifficultyDecorator";
import { ConjunctionList } from "../ConjunctionList/ConjunctionList";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";

type LevelCardProps = React.HTMLAttributes<HTMLDivElement> & {
    level: RDLevel;
}

export function LevelCard({level, className, ...rest}: LevelCardProps) {
    const clipboard = useClipboard({ timeout: 500 });
    const bpmText = level.min_bpm === level.max_bpm
        ? `${level.min_bpm} BPM`
        : `${level.min_bpm}-${level.max_bpm} BPM`;

    return (
        <article className={cc(styles.base, className)} {...rest}>
            <div className={styles.imageBox}>
                <img className={styles.image} src={level.thumb_url} />
                <div className={styles.overlay}>
                    <div className={styles.description}>
                        {
                            level.description.split('\n').map((p) => <Text>{p}</Text>)
                        }
                    </div>
                    <div className={styles.overlayButtons}>
                        <button
                            onClick={() => {
                                clipboard.copy(level.rdzip_url);
                            }}
                            className={cc(styles.button, styles.copy, clipboard.copied && styles.copyIsClicked)}
                        >
                            <FontAwesomeIcon icon={faPaste} className={styles.overlayIcon} />
                        </button>
                        <a href={level.rdzip_url} className={cc(styles.button, styles.download)}>
                            <FontAwesomeIcon icon={faDownload} className={styles.overlayIcon} />
                        </a>
                    </div>
                </div>
            </div>
            <div className={styles.info}>
                <DifficultyDecorator difficulty={level.difficulty} className={styles.decorator} />
                <div className={styles.cast}>
                    <div className={styles.songBox}>
                        <h2 className={styles.song}>{level.song}</h2>
                        {
                            level.song_alt && (
                                <p className={styles.songAlt}>({level.song_alt})</p>
                            )
                        }
                    </div>
                    <ConjunctionList
                        className={styles.artists}
                        items={level.artist_tokens}
                        elementRender={v => <p className={styles.artist}>{v}</p>}
                        literalRender={v => <p className={styles.artist}>{v}</p>}
                    />
                </div>
                <div className={styles.metadata}>
                    <div className={cc(styles.metaitem, styles.authors)}>
                        <FontAwesomeIcon icon={faPen} />
                        <ConjunctionList
                            className={styles.authorList}
                            elementRender={(v) => 
                                typeof v === 'string' 
                                    ? <UnstyledButton
                                        className={styles.metaitemButton}
                                    >
                                        {v}
                                    </UnstyledButton> : <></>
                            }
                            literalRender={(v) => <span className={styles.metaitemText}>{v}</span>}
                            items={level.authors}
                        />
                    </div>
                    <div className={cc(styles.metaitem, styles.bpm)}>
                        <FontAwesomeIcon icon={faHeartPulse} />
                        <Text className={cc(styles.metaitemText, styles.bpmText)}>{bpmText}</Text>
                    </div>
                    <div className={cc(styles.metaitem, styles.source)}>
                        <FontAwesomeIcon icon={faDiscord} />
                        <Text className={cc(styles.metaitemText, styles.sourceText)}>{level.club.name}</Text>
                    </div>
                    <div className={
                        cc(
                            styles.metaitem,
                            styles.approval,
                            level.approval >= 10 && styles.approvalYay,
                            level.approval < 0 && styles.approvalNope
                        )
                    }>
                        {
                            level.approval >= 10 ? (
                                <span title={'Peer-Reviewed: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability.'}>
                                    <FontAwesomeIcon icon={faCheck} className={styles.metaicon} />
                                </span>
                            ) : level.approval < 0 ? (
                                <span title={'Non-Referred: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability, and has found that this level does not meet standards.'}>
                                    <FontAwesomeIcon icon={faXmark} className={styles.metaicon} />
                                </span>
                            ) : null
                        }
                    </div>
                </div>
                <div className={styles.spacer} />
                <ul className={styles.tags}>
                    {
                        level.seizure_warning && (
                            <li>
                                <span className={cc(styles.tagCaution, styles.tag)}>
                                    <FontAwesomeIcon icon={faExclamationTriangle} className={styles.metaicon} />
                                    <span title="This level contains visuals and sustained flashing lighting that may affect those who are susceptible to photosensitive epilepsy or have other photosensitivities.">Seizure warning</span>
                                </span>
                            </li>
                        )
                    }
                    {
                        level.tags.map((tag) => (
                            <li>
                                <span
                                    className={styles.tag}
                                >
                                    {tag}
                                </span>
                            </li>
                        ))
                    }
                </ul>
            </div>
        </article>
    )
}