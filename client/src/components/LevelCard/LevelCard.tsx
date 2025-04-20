import { RDLevel } from "@cafe/types/rdLevelBase"

import cc from "clsx";
import styles from "./LevelCard.module.css";

import { Text, UnstyledButton } from "@mantine/core";
import { useClipboard } from '@mantine/hooks';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDownload, faHeartPulse, faPaste, faPen, faPerson } from "@fortawesome/free-solid-svg-icons";
import { DifficultyDecorator } from "./DifficultyDecorator/DifficultyDecorator";
import { ConjunctionList } from "../ConjunctionList/ConjunctionList";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";

type LevelCardProps = {
    level: RDLevel;
}

export function LevelCard({level}: LevelCardProps) {
    const clipboard = useClipboard({ timeout: 500 });
    const bpmText = level.min_bpm === level.max_bpm
        ? `${level.min_bpm} BPM`
        : `${level.min_bpm}-${level.max_bpm} BPM`;

    return (
        <article className={styles.base}>
            <div className={styles.imageBox}>
                <img className={styles.image} src={level.thumb_url} />
                <div className={styles.overlay}>
                    <div className={styles.description}>
                        {
                            level.description.split('\n').map(p => <Text>{p}</Text>)
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
                    <h2 className={styles.song}>{level.song}</h2>
                    <h3 className={styles.artist}>{level.artist}</h3>
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
                        <Text className={cc(styles.metaitemText, styles.sourceText)}>Rhythm Doctor Lounge</Text>
                    </div>
                </div>
            </div>
        </article>
    )
}