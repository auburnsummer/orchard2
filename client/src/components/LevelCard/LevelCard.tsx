import { RDLevel } from "@cafe/types/rdLevelBase";

import cc from "clsx";

import { useClipboard } from "@mantine/hooks";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCheck,
  faDownload,
  faExclamationTriangle,
  faHeartPulse,
  faPaste,
  faPen,
  faXmark,
} from "@fortawesome/free-solid-svg-icons";
import { DifficultyDecorator } from "./DifficultyDecorator/DifficultyDecorator";
import { ConjunctionList } from "../ConjunctionList";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { Link } from "@cafe/minibridge/components/Link";
import { Words } from "../ui/Words";

type LevelCardProps = React.HTMLAttributes<HTMLDivElement> & {
  level: RDLevel;
  showId?: boolean;
  href?: string;
  onClick?: () => void;
};

export function LevelCard({
  level,
  className,
  showId = false,
  href,
  onClick,
  ...rest
}: LevelCardProps) {
  const clipboard = useClipboard({ timeout: 500 });
  const bpmText =
    level.min_bpm === level.max_bpm
      ? `${level.min_bpm} BPM`
      : `${level.min_bpm}-${level.max_bpm} BPM`;

  return (
    <article 
      className={cc(
        "w-[26rem] max-w-screen rounded-lg flex flex-col bg-slate-100 dark:bg-slate-700",
        "group",
        onClick !== undefined && "hover:bg-slate-200 hover:shadow-md dark:hover:bg-slate-800",
        className
      )} 
      {...rest}
    >
      <div className="aspect-video grid grid-cols-1 grid-rows-1 rounded-t-lg overflow-hidden">
        <img 
          className={cc(
            "col-start-1 row-start-1 w-full h-full bg-blueGray-600 object-cover",
            "transition-all duration-250",
            "group-hover:bg-gray-200 group-hover:brightness-[45%] group-hover:saturate-[35%] group-hover:blur-[3px]",
            "dark:group-hover:bg-gray-800"
          )}
          src={level.thumb_url} 
        />
        <div className={cc(
          "col-start-1 row-start-1 z-10 p-5 opacity-0 text-white",
          "transition-opacity duration-250 shadow-[inset_0_3px_5px_0_rgba(0,0,0,0.1)]",
          "flex flex-row group-hover:opacity-100"
        )}>
          <div className="text-sm leading-4 flex-grow overflow-y-auto">
            {level.description.split("\n").map((p, i) => (
              <Words variant="alwaysLight" key={i}>{p}</Words>
            ))}
          </div>
          <div className="w-8 ml-2 flex flex-col items-center gap-4">
            <button
              onClick={() => {
                clipboard.copy(level.rdzip_url);
              }}
              className={cc(
                "w-8 border border-white p-2 rounded flex items-center justify-center",
                "bg-transparent text-white hover:bg-[--mantine-color-primary-4] hover:cursor-pointer",
                "relative",
                "after:content-['copied!'] after:absolute after:flex after:invisible",
                "after:inset-0 after:items-center after:justify-center after:text-base",
                "after:text-green-500 after:font-semibold after:z-10",
                "after:translate-y-[-0.5rem] after:opacity-100",
                "after:transition-all after:duration-1000 after:ease-out",
                clipboard.copied && "after:visible after:opacity-0 after:translate-y-[-2.5rem]"
              )}
            >
              <FontAwesomeIcon icon={faPaste} className="w-4 h-4" />
            </button>
            <a
              href={level.rdzip_url}
              className="w-8 border border-white p-2 rounded flex items-center justify-center bg-transparent text-white hover:bg-[--mantine-color-primary-4] hover:cursor-pointer"
            >
              <FontAwesomeIcon icon={faDownload} className="w-4 h-4" />
            </a>
          </div>
        </div>
      </div>
      <div
        className={cc(
          "p-4 relative flex flex-col flex-grow",
          onClick !== undefined && "hover:cursor-pointer"
        )}
        onClick={onClick}
      >
        <DifficultyDecorator
          difficulty={level.difficulty}
          className="absolute top-0 right-0"
        />
        <div className="flex flex-col-reverse gap-[0.075rem]">
          <div className="flex items-baseline gap-1 text-slate-800 dark:text-slate-200">
            {href ? (
              <Link href={href} className="text-[--mantine-color-text] no-underline hover:underline">
                <h2 className="font-semibold text-lg leading-5 break-words m-0">{level.song}</h2>
              </Link>
            ) : (
              <h2 className="font-semibold text-lg leading-5 break-words m-0">{level.song}</h2>
            )}
            {level.song_alt && (
              <p className="text-sm text-slate-500 dark:text-slate-400">({level.song_alt})</p>
            )}
          </div>
          <ConjunctionList
            className="list-none pl-0 flex"
            items={level.artist_tokens}
            elementRender={(v) => (
              <p className="whitespace-pre text-xs leading-4 text-slate-500 dark:text-slate-400 font-light m-0">
                {v}
              </p>
            )}
            literalRender={(v) => (
              <p className="whitespace-pre text-xs leading-4 text-slate-500 dark:text-slate-400 font-light m-0">
                {v}
              </p>
            )}
          />
        </div>
        <div className="mt-1 flex flex-wrap gap-x-5 gap-y-0">
          <div className="flex items-center text-xs leading-[1.125rem] text-slate-500 dark:text-slate-400">
            <FontAwesomeIcon icon={faPen} className="w-4 h-4" />
            <ConjunctionList
              className="ml-1 p-0 list-none"
              elementRender={(v) =>
                typeof v === "string" ? (
                  <Words as="span" className="whitespace-pre text-slate-500 dark:text-slate-400 text-xs">
                    {v}
                  </Words>
                ) : (
                  <></>
                )
              }
              literalRender={(v) => (
                <span className="whitespace-pre text-slate-500 dark:text-slate-400 text-xs">{v}</span>
              )}
              items={level.authors}
            />
          </div>
          <div className="flex items-center text-xs leading-[1.125rem] text-slate-500 dark:text-slate-400">
            <FontAwesomeIcon icon={faHeartPulse} className="w-4 h-4" />
            <Words className="ml-1 whitespace-pre text-slate-500 dark:text-slate-400 text-xs">
              {bpmText}
            </Words>
          </div>
          <div className="flex items-center text-xs leading-[1.125rem] text-slate-500 dark:text-slate-400">
            <FontAwesomeIcon icon={faDiscord} className="w-4 h-4" />
            <Words className="ml-1 whitespace-pre text-slate-500 dark:text-slate-400 text-xs">
              {level.club.name}
            </Words>
          </div>
          <div
            className={cc(
              "flex",
              level.approval >= 10 && "text-green-400",
              level.approval < 0 && "text-rose-600"
            )}
          >
            {level.approval >= 10 ? (
              <span
                className="flex items-center"
                title={
                  "Peer-Reviewed: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability."
                }
              >
                <FontAwesomeIcon icon={faCheck} className="w-4 h-4" />
              </span>
            ) : level.approval < 0 ? (
              <span
                className="flex items-center"
                title={
                  "Non-Referred: a trusted member of the community has checked for correct BPM/offset, metadata, and cues to ensure playability, and has found that this level does not meet standards."
                }
              >
                <FontAwesomeIcon icon={faXmark} className="w-4 h-4" />
              </span>
            ) : null}
          </div>
        </div>
        <div className="flex-grow" />
        <ul className="flex flex-row flex-wrap gap-1 pt-3 list-none pl-0">
          {level.seizure_warning && (
            <li>
              <span className="text-xs leading-4 bg-amber-200 dark:bg-amber-800 text-amber-600 dark:text-amber-200 px-3 py-0.5 rounded-full flex items-center">
                <FontAwesomeIcon
                  icon={faExclamationTriangle}
                  className="w-4 h-4 text-amber-600 dark:text-amber-200"
                />
                <span 
                  className="ml-1"
                  title="This level contains visuals and sustained flashing lighting that may affect those who are susceptible to photosensitive epilepsy or have other photosensitivities."
                >
                  Seizure warning
                </span>
              </span>
            </li>
          )}
          {level.tags.map((tag, i) => (
            <li key={i}>
              <span className="text-xs leading-4 bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-200 px-3 py-0.5 rounded-full flex items-center">
                {tag}
              </span>
            </li>
          ))}
        </ul>
        {showId && <Words className="absolute bottom-0 right-1 text-[0.65rem] text-slate-400">{level.id}</Words>}
      </div>
    </article>
  );
}
