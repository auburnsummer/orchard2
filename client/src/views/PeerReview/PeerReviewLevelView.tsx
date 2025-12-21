import { RDLevel } from "@cafe/types/rdLevelBase";
import { PeerReviewShell } from "./PeerReviewShell";
import { Surface } from "@cafe/components/ui/Surface";
import { PixelButton } from "./PixelButton";
import { useMemo, useRef, useState } from "react";
import {
  BAD_THING_CATS,
  BAD_THINGS,
  BadThingNames,
  BLOCKED_ARTISTS,
  JAM_TAGS,
} from "./constants";
import Fieldset from "@cafe/components/ui/Fieldset";
import { Checkbox } from "@cafe/components/ui/Checkbox";
import { TextInput } from "@cafe/components/ui/TextInput";
import { useAtom, useAtomValue } from "jotai";
import {
  doIPCAtom,
  doPrivatePostAtom,
  doPublicPostAtom,
  forcePrivatePostAtom,
  prAvatarAtom,
  nrAvatarAtom,
  pdAvatarAtom,
  prFlairTextAtom,
  nrFlairTextAtom,
  pdFlairTextAtom,
  dcNickAtom,
  dcIDAtom,
  pathlabWebhookUrlAtom,
  publicWebhookUrlAtom,
} from "./PeerReviewConfiguration";
import { Button } from "@cafe/components/ui/Button";
import { Form } from "@cafe/minibridge/components/Form";
import { Alert } from "@cafe/components/ui/Alert";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Dialog } from "@cafe/components/ui/Dialog";
import { Words } from "@cafe/components/ui/Words";
import { useClipboard, useDisclosure } from "@mantine/hooks";

type PeerReviewMainViewProps = {
  levels: RDLevel[];
  rdlevel: RDLevel;
  is_first_level: boolean;
  discord_id: string | null;
  prev_notes: string;
};

const PROPERTIES_TO_SHOW_IN_PREVIEW = [
  "artist",
  "difficulty",
  "tags",
  "description",
  "single_player",
  "min_bpm",
  "id",
  "icon_url",
] as const;

// The avatar used for public posts
const GENERIC_AVATAR =
  "https://cdn.discordapp.com/attachments/362784581344034816/851257060565188618/wow.png?v=1";

// The avatars used for private posts if you don't pick your own
const DEFAULT_PR_AVATAR =
  "https://cdn.discordapp.com/emojis/468288736090783744.png?v=1";
const DEFAULT_NR_AVATAR =
  "https://cdn.discordapp.com/emojis/585876613128781838.png?v=1";
const DEFAULT_PD_AVATAR =
  "https://cdn.discordapp.com/emojis/468288736090783744.png?v=1";

function formatPropertyKey(key: string): string {
  return key.replaceAll("_", " ").toUpperCase();
}

function getPreviewText(
  level: RDLevel,
  key: (typeof PROPERTIES_TO_SHOW_IN_PREVIEW)[number],
): string {
  const value = level[key];

  switch (key) {
    case "artist":
      return level.artist;
    case "tags":
      return level.tags.length > 0 ? level.tags.join(", ") : "-";
    case "description":
      return level.description || "-";
    case "difficulty": {
      const difficulties = [
        "🟩 Easy",
        "🟧 Medium",
        "🟥 Tough",
        "🟪 Very Tough",
      ];
      return difficulties[level.difficulty] || "-";
    }
    case "single_player": {
      return `${level.single_player ? "👤✅" : "👤❌"} ${level.two_player ? "👥✅" : "👥❌"}`;
    }
    case "min_bpm":
      if (level.max_bpm === level.min_bpm) return String(level.max_bpm);
      return `${level.min_bpm} - ${level.max_bpm}`;
    case "id":
      return level.id;
    case "icon_url":
      return level.icon_url || "-";
    default:
      return String(value) || "-";
  }
}

function getApprovalStatus(approval: number): {
  text: string;
  variant: "pr" | "nr" | "pd";
} {
  if (approval >= 10) return { text: "Peer-Reviewed", variant: "pr" };
  if (approval < 0) return { text: "Non-Refereed", variant: "nr" };
  return { text: "Pending", variant: "pd" };
}

async function webhookPost(url: string, payload: any) {
  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function PeerReviewLevelView({
  levels,
  rdlevel,
  is_first_level,
  discord_id,
  prev_notes,
}: PeerReviewMainViewProps) {
  const clipboard = useClipboard({ timeout: 500 });

  const [approvalIntent, setApprovalIntent] = useState<number>(
    rdlevel.approval,
  );

  const currentApprovalStatus = getApprovalStatus(rdlevel.approval);

  const [reasons, setReasons] = useState<Record<BadThingNames, boolean>>(() => {
    const initialReasons: Record<string, boolean> = {};
    BAD_THINGS.forEach((bt) => {
      initialReasons[bt.name] = false;
    });
    return initialReasons as Record<BadThingNames, boolean>;
  });

  const [privateComments, setPrivateComments] = useState<string>("");
  const [publicComments, setPublicComments] = useState<string>("");

  const [isFirstLevel, setIsFirstLevel] = useState<boolean>(is_first_level);
  const [firstLevelDiscordID, setFirstLevelDiscordID] = useState<string>(
    discord_id || "",
  );

  const [doIPC, setDoIPC] = useAtom(doIPCAtom);

  const forcePrivatePost = useAtomValue(forcePrivatePostAtom);
  const [doPublicPost, setDoPublicPost] = useAtom(doPublicPostAtom);
  const [doPrivatePost, setDoPrivatePost] = useAtom(doPrivatePostAtom);

  const pathlabWebhookUrl = useAtomValue(pathlabWebhookUrlAtom);
  const publicWebhookUrl = useAtomValue(publicWebhookUrlAtom);

  const prAvatar = useAtomValue(prAvatarAtom);
  const nrAvatar = useAtomValue(nrAvatarAtom);
  const pdAvatar = useAtomValue(pdAvatarAtom);
  const prFlairText = useAtomValue(prFlairTextAtom);
  const nrFlairText = useAtomValue(nrFlairTextAtom);
  const pdFlairText = useAtomValue(pdFlairTextAtom);
  const dcNick = useAtomValue(dcNickAtom);
  const dcID = useAtomValue(dcIDAtom);

  const jamTagsIfAny = JAM_TAGS.filter((jamTag) =>
    rdlevel.tags.some((tag) => tag.toLowerCase() === jamTag.toLowerCase()),
  );

  const blockedArtistsIfAny = BLOCKED_ARTISTS.filter((artist) =>
    rdlevel.artist_tokens.some(
      (token) => token.toLowerCase() === artist.toLowerCase(),
    ),
  );

  const publicReasons = useMemo(() => {
    const checkedBadThings = BAD_THINGS.filter((bt) => reasons[bt.name]).map(
      (bt) => bt.name,
    );
    return [...checkedBadThings, publicComments]
      .filter((s) => s !== "")
      .join(", ");
  }, [reasons, publicComments]);

  const privateReasons = useMemo(() => {
    const checkedBadThings = BAD_THINGS.filter((bt) => reasons[bt.name]).map(
      (bt) => bt.name,
    );
    const comments = doIPC ? publicComments + privateComments : privateComments;
    return [...checkedBadThings, comments].filter((s) => s !== "").join(", ");
  }, [reasons, publicComments, privateComments, doIPC]);

  const webhookPayloads = useMemo(() => {
    // Just goes through the logic of each part of the embed; what to show, what the user wants in it, etc.
    const avatarToUse =
      approvalIntent === 10
        ? prAvatar || DEFAULT_PR_AVATAR
        : approvalIntent === -1
          ? nrAvatar || DEFAULT_NR_AVATAR
          : pdAvatar || DEFAULT_PD_AVATAR;

    const word =
      approvalIntent === 10
        ? "Peer-Reviewed"
        : approvalIntent === -1
          ? "Non-Refereed"
          : "Pending Review";
    const flair =
      approvalIntent === 10
        ? prFlairText
        : approvalIntent === -1
          ? nrFlairText
          : pdFlairText;
    const nick = dcNick
      ? dcID
        ? `${dcNick} [<@${dcID}>]`
        : dcNick
      : dcID
        ? `<@${dcID}>`
        : "";
    const words = word + (flair ? ` (${flair})` : "");

    const url = rdlevel.rdzip_url;
    const color =
      approvalIntent === 10
        ? "3066993"
        : approvalIntent === -1
          ? "15158332"
          : "16776960";

    const problems = Object.keys(reasons)
      .filter((k) => reasons[k as BadThingNames])
      .join(", ");

    const problemsSpaceArray: string[] = [];
    const publicProblemsArray: string[] = [];

    // Very roundabout yet fool-proof way of ensuring commas are in the right place
    if (problems) {
      problemsSpaceArray.push(problems);
      publicProblemsArray.push(problems);
    }

    if (doIPC && publicComments) problemsSpaceArray.push(publicComments);
    if (privateComments) problemsSpaceArray.push(privateComments);

    if (publicComments) publicProblemsArray.push(publicComments);

    let problemsSpace = problemsSpaceArray.join(", ");
    let publicProblems = publicProblemsArray.join(", ");

    let title = `${rdlevel.artist} - ${rdlevel.song}`;
    let description = `by ${rdlevel.authors.join(", ")}`;
    let wordsForEmbed = words;

    // Checks if Discord will complain that some text is too long
    if (title.length > 252) title = `${title.slice(0, 252)}...`; // 256 - Brought to you by KirbyCreep
    if (description.length + nick.length > 4092)
      description = `${description.slice(0, 4072 - nick.length)}...`; // 4096
    if (wordsForEmbed.length > 252)
      wordsForEmbed = `${wordsForEmbed.slice(0, 252)}...`; // 256
    if (problemsSpace.length > 2044)
      problemsSpace = `${problemsSpace.slice(0, 2044)}...`; // 2048
    if (publicProblems.length > 2044)
      publicProblems = `${publicProblems.slice(0, 2044)}...`; // 2048

    const firstLevelText =
      `Hello <@${firstLevelDiscordID}>, ` +
      (approvalIntent === 10
        ? "your first level got peer reviewed! This means it is now visible by default on <https://rhythm.cafe>. To learn more, ask in <#808382639748022332>!"
        : approvalIntent === -1
          ? "unfortunately, your first level was non-refereed for the reasons above. This means it is hidden by default on <https://rhythm.cafe>. If you have questions about what this means or how to fix it, feel free to read the [peer-review definitions](<https://docs.google.com/spreadsheets/d/1RKRov9kkbHKV-NJMCLWHFRL_AiKkB0I1_mg7WMG4iJA/edit>) or ask in <#808382639748022332>!"
          : "your first level is pending. This means it is in the process of getting peer reviewed and is hidden by default on <https://rhythm.cafe>. To learn more, ask in <#808382639748022332>!");

    const privatePayload = {
      avatar_url: avatarToUse,
      embeds: [
        {
          author: {
            name: wordsForEmbed,
            icon_url: avatarToUse,
          },
          title,
          description: `${description}${nick ? `\n-# Reviewed by ${nick}` : ""}`,
          footer: { text: problemsSpace },
          thumbnail: { url: rdlevel.image_url },
          color,
          url,
        },
      ],
    };

    const publicPayload = {
      avatar_url: GENERIC_AVATAR,
      embeds: [
        {
          author: {
            name: word,
          },
          title,
          description,
          footer: { text: publicProblems },
          thumbnail: { url: rdlevel.image_url },
          color,
          url,
        },
      ],
    };

    const firstLevelMessage = {
      avatar_url: GENERIC_AVATAR,
      content: firstLevelText,
      allowed_mentions: { users: [firstLevelDiscordID] },
    };

    return {
      public: publicPayload,
      private: privatePayload,
      firstLevelMessage,
    };
  }, [
    approvalIntent,
    reasons,
    publicComments,
    privateComments,
    doIPC,
    prAvatar,
    nrAvatar,
    pdAvatar,
    prFlairText,
    nrFlairText,
    pdFlairText,
    dcNick,
    dcID,
    firstLevelDiscordID,
    rdlevel,
  ]);

  const formRef = useRef<HTMLFormElement>(null);

  const toggleReason = (name: BadThingNames) => {
    setReasons((prev) => ({
      ...prev,
      [name]: !prev[name],
    }));
  };

  const csrfInput = useCSRFTokenInput();

  const warningsBeforeSubmit = useMemo(() => {
    const warnings: string[] = [];

    if (approvalIntent === 0 && doPublicPost) {
      warnings.push(
        "Are you sure you want to peer-review this publicly with the Pending status?",
      );
    }
    if (!doPublicPost && !doPrivatePost) {
      warnings.push(
        "Submitting this peer-review will not inform anyone. Are you sure?",
      );
    } else if (doPublicPost && !doPrivatePost) {
      warnings.push("This is not sent privately, only publicly. Are you sure?");
    } else if (!doPublicPost) {
      warnings.push(
        "You're changing the status on a level but not posting publicly. The public will not be informed of this change. Are you sure?",
      );
    }
    if (approvalIntent === rdlevel.approval) {
      warnings.push(
        "This level already has that approval status. Are you sure?",
      );
    }
    if (rdlevel.is_private && doPublicPost) {
      warnings.push(
        "This level is marked as private. Are you sure you want to post about it publicly?",
      );
    }
    if (rdlevel.approval !== 0) {
      warnings.push(
        "This level has already been peer-reviewed. Are you sure you want to change it?",
      );
    }
    if (blockedArtistsIfAny.length > 0) {
      warnings.push(
        `Level artist contains blocked artists: ${blockedArtistsIfAny.join(
          ", ",
        )}. Are you sure you want to proceed?`,
      );
    }

    return warnings;
  }, [
    approvalIntent,
    doPublicPost,
    doPrivatePost,
    forcePrivatePost,
    rdlevel.approval,
  ]);

  const [showWarningDialog, setShowWarningDialog] = useState<boolean>(false);

  const onSubmit = () => {
    if (warningsBeforeSubmit.length > 0) {
      setShowWarningDialog(true);
      return;
    } else {
      submitPR();
    }
  };

  const submitPR = async () => {
    const promises: Promise<void>[] = [];
    if (doPublicPost && publicWebhookUrl) {
      promises.push(webhookPost(publicWebhookUrl, webhookPayloads.public));
    }
    if (doPrivatePost && pathlabWebhookUrl) {
      promises.push(webhookPost(pathlabWebhookUrl, webhookPayloads.private));
    }
    if (isFirstLevel && firstLevelDiscordID && publicWebhookUrl) {
      promises.push(
        webhookPost(publicWebhookUrl, webhookPayloads.firstLevelMessage),
      );
    }
    await Promise.all(promises);
    formRef.current?.submit();
  };

  return (
    <PeerReviewShell pendingLevels={levels}>
      {/* invisible form containing the actual data to be submitted */}
      <Dialog
        open={showWarningDialog}
        onClose={() => setShowWarningDialog(false)}
      >
        <Words>Please review the following warnings before submitting:</Words>
        <ul>
          {warningsBeforeSubmit.map((warning, index) => (
            <li key={index} className="ml-6 list-disc">
              <Words variant="sm">{warning}</Words>
            </li>
          ))}
        </ul>
        <Button
          variant="primary"
          className="mt-4"
          onClick={() => {
            setShowWarningDialog(false);
            submitPR();
          }}
        >
          Submit Review
        </Button>
      </Dialog>
      <Form method="post" className="hidden" ref={formRef}>
        {csrfInput}
        <input type="hidden" name="approval_intent" value={approvalIntent} />
        <input type="hidden" name="public_comment" value={publicReasons} />
        <input type="hidden" name="private_comment" value={privateReasons} />
      </Form>
      <Surface className="relative m-4 overflow-hidden border border-gray-300 bg-white/70 p-6 shadow-xl backdrop-blur-lg dark:border-gray-700 dark:bg-slate-800/70">
        {/* Background Blur Image */}
        <div
          className="pointer-events-none absolute inset-0 opacity-5 blur-xl"
          style={{
            backgroundImage: `url('${rdlevel.image_url}')`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            zIndex: 0,
          }}
        />

        {/* Foreground Content */}
        <div className="relative z-10 flex flex-col items-start gap-6 md:flex-row">
          {/* Side Image */}
          <div className="w-full flex-shrink-0 md:w-1/3">
            <img
              src={rdlevel.image_url}
              alt={`${rdlevel.song} level preview`}
              className="aspect-video w-full border border-gray-200 object-cover shadow-lg dark:border-gray-700"
            />
            <br />

            {/* Title + Author */}
            <div className="w-full text-left">
              <a
                href={`/levels/${rdlevel.id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-3xl font-extrabold text-blue-600 hover:underline dark:text-blue-400"
              >
                {rdlevel.song}
              </a>
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                by {rdlevel.authors.join(", ")}
              </p>
            </div>

            {/* Buttons */}
            <div className="mt-4 flex flex-wrap gap-2">
              <Button
                as="a"
                href={rdlevel.rdzip_url}
                target="_blank"
                rel="noopener noreferrer"
                variant="primary"
              >
                Download
              </Button>
              <Button
                variant="secondary"
                onClick={() => {
                  clipboard.copy(rdlevel.rdzip_url);
                }}
              >
                {clipboard.copied ? "Copied!" : "Copy Link"}
              </Button>
            </div>
          </div>

          {/* Info & Metadata */}
          <div className="flex flex-1 flex-col gap-4">
            {/* Level Properties Grid */}
            <div className="mt-2 grid grid-cols-1 gap-x-6 gap-y-4 text-sm text-gray-800 sm:grid-cols-2 dark:text-gray-200">
              {PROPERTIES_TO_SHOW_IN_PREVIEW.map((key) => (
                <div key={key}>
                  <div className="text-xs font-bold tracking-wider text-gray-500 uppercase dark:text-gray-400">
                    {formatPropertyKey(key)}
                  </div>
                  <div className="text-md font-medium">
                    {getPreviewText(rdlevel, key)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Warnings */}
        <div className="mt-6">
          {rdlevel.seizure_warning && (
            <Alert variant="warning" className="mt-6">
              Level is marked with a seizure warning.
            </Alert>
          )}
          {jamTagsIfAny.length > 0 && (
            <Alert variant="info" className="mt-6">
              Level is tagged with Jam tag(s): {jamTagsIfAny.join(", ")}.
            </Alert>
          )}
          {blockedArtistsIfAny.length > 0 && (
            <Alert variant="error" className="mt-6">
              Level artist contains blocked artists:{" "}
              {blockedArtistsIfAny.join(", ")}.
            </Alert>
          )}
          {prev_notes.length > 0 && (
            <Alert variant="info" className="mt-6">
              Previous reviewer notes: {prev_notes}
            </Alert>
          )}
          {rdlevel.is_private && (
            <Alert variant="info" className="mt-6">
              Private level
            </Alert>
          )}
        </div>

        {/* Approval Badge */}
        <br />
        <PixelButton
          variant={currentApprovalStatus.variant}
          onClick={() => setApprovalIntent(rdlevel.approval)}
          inactive={approvalIntent !== rdlevel.approval}
        >
          {currentApprovalStatus.text}
        </PixelButton>

        {/* Timestamp */}
        <div className="absolute top-2 right-4 z-10 flex flex-col items-end space-y-1">
          <div className="text-xs font-medium text-gray-700 dark:text-gray-300">
            {new Date(rdlevel.last_updated).toLocaleString()}
          </div>
        </div>

        {/* form display */}
        <div className="mt-4">
          {BAD_THING_CATS.map((cat) => (
            <Fieldset legend={cat} key={cat} className="capitalize">
              <div className="grid normal-case md:grid-cols-2 lg:grid-cols-3">
                {BAD_THINGS.filter((bt) => bt.category === cat).map((bt) => (
                  <Checkbox
                    key={bt.name}
                    label={bt.name}
                    description={bt.description}
                    showDescriptionAsTooltip
                    checked={reasons[bt.name]}
                    onChange={() => toggleReason(bt.name)}
                  />
                ))}
              </div>
            </Fieldset>
          ))}
        </div>

        <div className="flex flex-row">
          <PixelButton
            variant="nr"
            className="mr-4"
            onClick={() => setApprovalIntent(-1)}
            inactive={approvalIntent !== -1}
          >
            Non-Refereed
          </PixelButton>
          <PixelButton
            variant="pd"
            className="mr-4"
            onClick={() => setApprovalIntent(0)}
            inactive={approvalIntent !== 0}
          >
            Pending
          </PixelButton>
          <PixelButton
            variant="pr"
            onClick={() => setApprovalIntent(10)}
            inactive={approvalIntent !== 10}
          >
            Peer-Reviewed
          </PixelButton>
        </div>
        {/* Comments and First Level */}
        <Fieldset legend="Comments" className="mt-4">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <TextInput
              label="Private Comments"
              description="Only shown in #pathology-lab."
              value={privateComments}
              onChange={(e) => setPrivateComments(e.target.value)}
            />
            <TextInput
              label="Public Comments"
              description="Shown publicly."
              value={publicComments}
              onChange={(e) => setPublicComments(e.target.value)}
            />
            {/* First Level Checkbox and User ID */}
            <div className="flex flex-col">
              <div className="mb-2 flex items-center">
                <Checkbox
                  id="firstLevel"
                  label="First level"
                  showDescriptionAsTooltip
                  className="mr-2"
                  description="If this is the creator's first time uploading a level."
                  checked={isFirstLevel}
                  onChange={() => setIsFirstLevel(!isFirstLevel)}
                />
              </div>
              {isFirstLevel && (
                <div>
                  <TextInput
                    label="Discord ID"
                    description="For pinging the user in #pathology-reports. Autofills when a Discord ID is found on a level."
                    value={firstLevelDiscordID}
                    onChange={(e) => setFirstLevelDiscordID(e.target.value)}
                  />
                </div>
              )}
            </div>
            {/* Include Public Comments in Private (this can also be changed in config) */}
            <Checkbox
              label="Include Public Comments in Private"
              description="Prepend message in 'Public Comments' into Private Comments"
              checked={doIPC}
              onChange={() => setDoIPC(!doIPC)}
            />
          </div>
        </Fieldset>
        {/* submit and toggles */}
        <div className="mt-4 flex flex-row items-center gap-4">
          <Button variant="primary" className="w-32" onClick={onSubmit}>
            Submit Review
          </Button>
          <Checkbox
            label="Public"
            description="Posts to #pathology-reports"
            showDescriptionAsTooltip
            checked={doPublicPost}
            onChange={() => setDoPublicPost(!doPublicPost)}
          />
          <Checkbox
            label="Private"
            disabled={forcePrivatePost}
            title={
              forcePrivatePost
                ? "Private posting is forced in configuration"
                : undefined
            }
            description="Posts to #pathology-lab"
            showDescriptionAsTooltip
            checked={doPrivatePost || forcePrivatePost}
            onChange={() => setDoPrivatePost(!doPrivatePost)}
          />
        </div>
      </Surface>
    </PeerReviewShell>
  );
}
