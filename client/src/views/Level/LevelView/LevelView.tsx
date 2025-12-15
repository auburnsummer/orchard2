import { Shell } from "@cafe/components/Shell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import {
  faHeartPulse,
  faPen,
  faDownload,
  faLink,
  faTrash,
  faEdit,
  faTags,
  faUsers,
  faExclamationTriangle,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDiscord } from "@fortawesome/free-brands-svg-icons";
import { useClipboard, useDisclosure } from "@mantine/hooks";
import { Form } from "@cafe/minibridge/components/Form";
import { Link } from "@cafe/minibridge/components/Link";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { DIFFICULTY_STRINGS } from "@cafe/utils/constants";
import { CopyIconButton } from "@cafe/components/CopyIconButton";
import { ConjunctionList } from "@cafe/components/ConjunctionList";
import { Button } from "@cafe/components/ui/Button";
import { Dialog } from "@cafe/components/ui/Dialog";
import { Surface } from "@cafe/components/ui/Surface";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Words } from "@cafe/components/ui/Words";

import styles from "./LevelView.module.css";
import { useUser } from "@cafe/hooks/useUser";

type LevelViewProps = {
  rdlevel: RDLevel;
  can_edit: boolean;
  can_delete: boolean;
};

export function LevelView({ rdlevel, can_edit, can_delete }: LevelViewProps) {
  const clipboard = useClipboard({ timeout: 500 });
  const bpmText =
    rdlevel.min_bpm === rdlevel.max_bpm
      ? `${rdlevel.min_bpm} BPM`
      : `${rdlevel.min_bpm}-${rdlevel.max_bpm} BPM`;

  const [showDeleteForm, { open: openDeleteForm, close: closeDeleteForm }] =
    useDisclosure(false);

  const csrfInput = useCSRFTokenInput();

  // TODO: align with DifficultyDecorator.tsx
  const getDifficultyBadgeClass = (difficulty: number) => {
    if (difficulty === 0) return "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300"; // Easy
    if (difficulty === 1) return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300"; // Medium
    if (difficulty === 2) return "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300"; // Tough
    return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300"; // Very Tough
  };

  const getDifficultyString = (difficulty: number) => {
    return DIFFICULTY_STRINGS[difficulty] || "Unknown";
  };

  const user = useUser();

  const canPeerReview = user.authenticated && user.is_peer_reviewer;

  return (
    <Shell>
      <Dialog open={showDeleteForm} onClose={closeDeleteForm}>
        <Words as="h3" variant="subheader" className="mb-4">
          Delete {rdlevel.song}
        </Words>
        <Form method="POST" action={`/levels/${rdlevel.id}/delete/`}>
          {csrfInput}
          <div className="flex flex-col gap-4">
            <Words>Are you sure you want to delete this level?</Words>
            <Words variant="muted" className="text-sm">
              This action cannot be undone.
            </Words>
            <div className="flex justify-end gap-2">
              <Button type="button" onClick={closeDeleteForm}>
                Cancel
              </Button>
              <Button
                type="submit"
                variant="danger"
              >
                <FontAwesomeIcon icon={faTrash} className="mr-2" />
                Delete Level
              </Button>
            </div>
          </div>
        </Form>
      </Dialog>

      <div className="max-w-7xl mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          {/* Main Content */}
          <div className="md:col-span-8">
            <Surface className="p-6">
              <div className="flex flex-col md:flex-row gap-4 mb-6 items-start">
                <img
                  src={rdlevel.image_url}
                  alt={`${rdlevel.song} cover`}
                  className="rounded-md h-[200px] w-full md:w-[355px] object-cover"
                />

                <div className="flex-1 flex flex-col gap-2">
                  <div>
                    <ConjunctionList
                      className={styles.artistList}
                      items={rdlevel.artist_tokens}
                      elementRender={(v) => (
                        <Words variant="muted" className="text-sm">
                          {v}
                        </Words>
                      )}
                      literalRender={(v) => (
                        <Words variant="muted" className="text-sm">
                          {v}
                        </Words>
                      )}
                    />
                    <Words as="h1" className="text-2xl font-bold mb-2">
                      {rdlevel.song}
                      {rdlevel.song_alt && (
                        <Words as="span" variant="muted" className="ml-2">
                          ({rdlevel.song_alt})
                        </Words>
                      )}
                    </Words>
                  </div>

                  <div className="flex flex-wrap gap-4">
                    <div className="flex items-center gap-1">
                      <FontAwesomeIcon
                        icon={faPen}
                        className={styles.metaIcon}
                      />
                      <ConjunctionList
                        className={styles.metadataList}
                        elementRender={(v) =>
                          typeof v === "string" ? (
                            <button className={styles.authorButton}>
                              {v}
                            </button>
                          ) : (
                            <></>
                          )
                        }
                        literalRender={(v) => (
                          <Words className="text-sm">
                            {v}
                          </Words>
                        )}
                        items={rdlevel.authors}
                      />
                    </div>

                    <div className="flex items-center gap-1">
                      <FontAwesomeIcon
                        icon={faHeartPulse}
                        className={styles.metaIcon}
                      />
                      <Words className="text-sm">{bpmText}</Words>
                    </div>

                    <div className="flex items-center gap-1">
                      <FontAwesomeIcon
                        icon={faDiscord}
                        className={styles.metaIcon}
                      />
                      <Words className="text-sm">{rdlevel.club.name}</Words>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 mt-2">
                    <span className={`px-3 py-1 rounded-md text-sm font-medium ${getDifficultyBadgeClass(rdlevel.difficulty)}`}>
                      {getDifficultyString(rdlevel.difficulty)}
                    </span>

                    {rdlevel.seizure_warning && (
                      <span className="px-3 py-1 rounded-md text-sm font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300 flex items-center gap-1">
                        <FontAwesomeIcon icon={faExclamationTriangle} />
                        Seizure Warning
                      </span>
                    )}

                    {rdlevel.single_player && rdlevel.two_player ? (
                      <span className="px-3 py-1 rounded-md text-sm font-medium bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 flex items-center gap-1">
                        <FontAwesomeIcon icon={faUsers} />
                        1-2 Players
                      </span>
                    ) : rdlevel.two_player ? (
                      <span className="px-3 py-1 rounded-md text-sm font-medium bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 flex items-center gap-1">
                        <FontAwesomeIcon icon={faUsers} />
                        2 Players
                      </span>
                    ) : (
                      <span className="px-3 py-1 rounded-md text-sm font-medium bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 flex items-center gap-1">
                        <FontAwesomeIcon icon={faUsers} />
                        1 Player
                      </span>
                    )}
                  </div>
                </div>
              </div>

              <hr className="my-6 border-slate-200 dark:border-slate-700" />

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-2 mb-6">
                <Button
                  as="a"
                  href={rdlevel.rdzip_url}
                  variant="primary"
                >
                  <FontAwesomeIcon icon={faDownload} className="mr-2" />
                  Download
                </Button>
                <Button
                  onClick={() => clipboard.copy(rdlevel.rdzip_url)}
                >
                  <FontAwesomeIcon icon={faLink} className="mr-2" />
                  {clipboard.copied ? "Copied!" : "Copy Link"}
                </Button>
                {can_edit && (
                  <Button
                    as={Link}
                    href={`/levels/${rdlevel.id}/edit/`}
                  >
                    <FontAwesomeIcon icon={faEdit} className="mr-2" />
                    Edit
                  </Button>
                )}
                {can_delete && (
                  <Button
                    variant="danger"
                    onClick={openDeleteForm}
                  >
                    <FontAwesomeIcon icon={faTrash} className="mr-2" />
                    Delete
                  </Button>
                )}
              </div>

              {/* Description */}
              {rdlevel.description && (
                <div>
                  <Words className="font-medium mb-2">
                    Description
                  </Words>
                  <div className="p-4 bg-slate-100 dark:bg-slate-900 rounded-lg">
                    {rdlevel.description.split("\n").map((paragraph, index) => (
                      <Words key={index} className="mb-2">
                        {paragraph}
                      </Words>
                    ))}
                  </div>
                </div>
              )}
            </Surface>
          </div>

          {/* Sidebar */}
          <div className="md:col-span-4">
            <div className="flex flex-col gap-4">
              {/* Tags */}
              {rdlevel.tags.length > 0 && (
                <Surface className="p-4">
                  <div className="flex items-center gap-1 mb-2">
                    <FontAwesomeIcon
                      icon={faTags}
                      className={styles.sectionIcon}
                    />
                    <Words className="font-medium">Tags</Words>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {rdlevel.tags.map((tag) => (
                      <span key={tag} className="px-3 py-0.5 rounded-full text-xs bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-200">
                        {tag}
                      </span>
                    ))}
                  </div>
                </Surface>
              )}
              {/* PR status */}
              <Surface className="p-4">
                <div className="flex items-center gap-1 mb-2">
                  <FontAwesomeIcon
                    icon={faPen}
                    className={styles.sectionIcon}
                  />
                  <Words className="font-medium ml-1">Peer Review Status</Words>
                </div>
                {rdlevel.approval === 10 ? (
                  <Words variant="sm">
                    Peer Reviewed
                  </Words>
                ) : rdlevel.approval === -1 ? (
                  <Words variant="sm">
                    Non-Refeered
                  </Words>
                ) : (
                  <Words variant="sm">
                    Pending Peer Review
                  </Words>
                )}
                {
                  canPeerReview && (
                    <Words variant="link" as={Link} href={`/peer-review/${rdlevel.id}/`} className="mt-2 block text-sm">
                      Go to PR Page for this level
                    </Words>
                  )
                }
              </Surface>

              <TextInput
                label="Level ID"
                value={rdlevel.id}
                readOnly
                rightSlot={<CopyIconButton value={rdlevel.id} />}
              />

            </div>
          </div>
        </div>
      </div>
    </Shell>
  );
}
