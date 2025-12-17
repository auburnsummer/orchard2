import { RDLevel } from "@cafe/types/rdLevelBase";
import { PeerReviewShell } from "./PeerReviewShell";
import { Surface } from "@cafe/components/ui/Surface";
import { PixelButton } from "./PixelButton";
import { useMemo, useRef, useState } from "react";
import { BAD_THING_CATS, BAD_THINGS, BadThingNames, BLOCKED_ARTISTS, JAM_TAGS } from "./constants";
import Fieldset from "@cafe/components/ui/Fieldset";
import { Checkbox } from "@cafe/components/ui/Checkbox";
import { TextInput } from "@cafe/components/ui/TextInput";
import { useAtom, useAtomValue } from "jotai";
import { doIPCAtom, doPrivatePostAtom, doPublicPostAtom, forcePrivatePostAtom } from "./PeerReviewConfiguration";
import { Button } from "@cafe/components/ui/Button";
import { Form } from "@cafe/minibridge/components/Form";
import { Alert } from "@cafe/components/ui/Alert";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

type PeerReviewMainViewProps = {
    levels: RDLevel[];
    rdlevel: RDLevel;
    is_first_level: boolean;
    discord_id: string | null;
};

const PROPERTIES_TO_SHOW_IN_PREVIEW = [
    "artist", "difficulty", "tags", "description",
    "single_player", "min_bpm",
    "id", "icon_url"
] as const;

function formatPropertyKey(key: string): string {
    return key.replaceAll('_', ' ').toUpperCase();
}

function getPreviewText(level: RDLevel, key: typeof PROPERTIES_TO_SHOW_IN_PREVIEW[number]): string {
    const value = level[key];
    
    switch (key) {
        case 'artist':
            return level.artist;
        case 'tags':
            return level.tags.length > 0 ? level.tags.join(', ') : '-';
        case 'description':
            return level.description || '-';
        case 'difficulty': {
            const difficulties = ['🟩 Easy', '🟧 Medium', '🟥 Tough', '🟪 Very Tough'];
            return difficulties[level.difficulty] || '-';
        }
        case 'single_player': {
            return `${level.single_player ? '👤✅' : '👤❌'} ${level.two_player ? '👥✅' : '👥❌'}`;
        }
        case 'min_bpm':
            if (level.max_bpm === level.min_bpm) return String(level.max_bpm);
            return `${level.min_bpm} - ${level.max_bpm}`;
        case 'id':
            return level.id;
        case 'icon_url':
            return level.icon_url || '-';
        default:
            return String(value) || '-';
    }
}

function getApprovalStatus(approval: number): { text: string; variant: 'pr' | 'nr' | 'pd' } {
    if (approval >= 10) return { text: 'Peer-Reviewed', variant: 'pr' };
    if (approval < 0) return { text: 'Non-Refereed', variant: 'nr' };
    return { text: 'Pending', variant: 'pd' };
}

export function PeerReviewLevelView({ levels, rdlevel, is_first_level, discord_id }: PeerReviewMainViewProps) {
    const [approvalIntent, setApprovalIntent] = useState<number>(rdlevel.approval);

    const currentApprovalStatus = getApprovalStatus(rdlevel.approval);

    const [reasons, setReasons] = useState<Record<BadThingNames, boolean>>(() => {
        const initialReasons: Record<string, boolean> = {};
        BAD_THINGS.forEach(bt => {
            initialReasons[bt.name] = false;
        });
        return initialReasons as Record<BadThingNames, boolean>;
    });

    const [privateComments, setPrivateComments] = useState<string>('');
    const [publicComments, setPublicComments] = useState<string>('');

    const [isFirstLevel, setIsFirstLevel] = useState<boolean>(is_first_level);
    const [firstLevelDiscordID, setFirstLevelDiscordID] = useState<string>(discord_id || '');

    const [doIPC, setDoIPC] = useAtom(doIPCAtom);

    const forcePrivatePost = useAtomValue(forcePrivatePostAtom);
    const [doPublicPost, setDoPublicPost] = useAtom(doPublicPostAtom);
    const [doPrivatePost, setDoPrivatePost] = useAtom(doPrivatePostAtom);

    const jamTagsIfAny = JAM_TAGS.filter(jamTag => 
        rdlevel.tags.some(tag => tag.toLowerCase() === jamTag.toLowerCase())
    );

    const blockedArtistsIfAny = BLOCKED_ARTISTS.filter(artist => 
        rdlevel.artist_tokens.some(token => token.toLowerCase() === artist.toLowerCase())
    );

    const publicReasons = useMemo(() => {
        const checkedBadThings = BAD_THINGS.filter(bt => reasons[bt.name]).map(bt => bt.name);
        return [...checkedBadThings, publicComments].filter(s => s !== '').join(', ');
    }, [reasons, publicComments]);

    const privateReasons = useMemo(() => {
        const checkedBadThings = BAD_THINGS.filter(bt => reasons[bt.name]).map(bt => bt.name);
        const comments = doIPC ? publicComments + privateComments : privateComments;
        return [...checkedBadThings, comments].filter(s => s !== '').join(', ');
    }, [reasons, publicComments, privateComments, doIPC]);

    const formRef = useRef<HTMLFormElement>(null);

    const toggleReason = (name: BadThingNames) => {
        setReasons(prev => ({
            ...prev,
            [name]: !prev[name]
        }));
    };

    const csrfInput = useCSRFTokenInput();

    return (
        <PeerReviewShell pendingLevels={levels}>
            {/* invisible form containing the actual data to be submitted */}
            <Form method="post" className="hidden" ref={formRef}>
                {csrfInput}
                <input type="hidden" name="approval_intent" value={approvalIntent} />
                <input type="hidden" name="public_comment" value={publicReasons} />
                <input type="hidden" name="private_comment" value={privateReasons} />
            </Form>
            <Surface className="m-4 relative p-6 shadow-xl border border-gray-300 dark:border-gray-700 bg-white/70 dark:bg-slate-800/70 backdrop-blur-lg overflow-hidden">
                {/* Background Blur Image */}
                <div 
                    className="absolute inset-0 opacity-5 blur-xl pointer-events-none"
                    style={{
                        backgroundImage: `url('${rdlevel.image_url}')`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                        zIndex: 0
                    }}
                />

                {/* Foreground Content */}
                <div className="relative z-10 flex flex-col md:flex-row gap-6 items-start">
                    {/* Side Image */}
                    <div className="flex-shrink-0 w-full md:w-1/3">
                        <img 
                            src={rdlevel.image_url} 
                            alt={`${rdlevel.song} level preview`}
                            className="w-full aspect-video object-cover border border-gray-200 dark:border-gray-700 shadow-lg"
                        />
                        <br />
                        
                        {/* Title + Author */}
                        <div className="text-left w-full">
                            <a 
                                href={`/levels/${rdlevel.id}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-3xl font-extrabold text-blue-600 dark:text-blue-400 hover:underline"
                                
                            >
                                {rdlevel.song}
                            </a>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                                by {rdlevel.authors.join(', ')}
                            </p>

                            {/* Warnings */}
                            <div className="mt-2 flex flex-wrap gap-2 text-xl justify-start">
                                {rdlevel.seizure_warning && (
                                    <span title="👁 Seizure Warning">👁</span>
                                )}
                                {rdlevel.club?.id === 'prescriptions' && (
                                    <span title="🔒 Uploaded Privately to #prescriptions">🔒</span>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Info & Metadata */}
                    <div className="flex-1 flex flex-col gap-4">
                        {/* Level Properties Grid */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4 text-gray-800 dark:text-gray-200 text-sm mt-2">
                            {PROPERTIES_TO_SHOW_IN_PREVIEW.map((key) => (
                                <div key={key}>
                                    <div className="font-bold uppercase text-xs text-gray-500 dark:text-gray-400 tracking-wider">
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
                    {
                        rdlevel.seizure_warning && (
                            <Alert variant="warning" className="mt-6">
                                Level is marked with a seizure warning.
                            </Alert>
                        )
                    }
                    {
                        jamTagsIfAny.length > 0 && (
                            <Alert variant="info" className="mt-6">
                                Level is tagged with Jam tag(s): {jamTagsIfAny.join(', ')}.
                            </Alert>
                        )
                    }
                    {
                        blockedArtistsIfAny.length > 0 && (
                            <Alert variant="error" className="mt-6">
                                Level artist contains blocked artists: {blockedArtistsIfAny.join(', ')}.
                            </Alert>
                        )
                    }
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
                <div className="absolute top-2 right-4 flex flex-col items-end z-10 space-y-1">
                    <div className="text-xs text-gray-700 dark:text-gray-300 font-medium">
                        {new Date(rdlevel.last_updated).toLocaleString()}
                    </div>
                </div>

                {/* form display */}
                <div className="mt-4">
                    {
                        BAD_THING_CATS.map(cat => (
                            <Fieldset legend={cat} key={cat} className="capitalize">
                                <div className="normal-case grid lg:grid-cols-3 md:grid-cols-2">
                                    {
                                        BAD_THINGS.filter(bt => bt.category === cat).map(bt => (
                                            <Checkbox
                                                key={bt.name}
                                                label={bt.name}
                                                description={bt.description}
                                                showDescriptionAsTooltip
                                                checked={reasons[bt.name]}
                                                onChange={() => toggleReason(bt.name)}
                                            />
                                        ))
                                    }
                                </div>
                            </Fieldset>
                        ))
                    }
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
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <TextInput label="Private Comments" description="Only shown in #pathology-lab." value={privateComments} onChange={e => setPrivateComments(e.target.value)} />
                        <TextInput label="Public Comments" description="Shown publicly." value={publicComments} onChange={e => setPublicComments(e.target.value)} />
                        {/* First Level Checkbox and User ID */}
                        <div className="flex flex-col">
                            <div className="flex items-center mb-2">
                                <Checkbox id="firstLevel"
                                    label="First level"
                                    showDescriptionAsTooltip
                                    className="mr-2"
                                    description="If this is the creator's first time uploading a level."
                                    checked={isFirstLevel}
                                    onChange={() => setIsFirstLevel(!isFirstLevel)}
                                />
                            </div>
                            { isFirstLevel && (
                                <div>
                                    <TextInput
                                        label="Discord ID"
                                        description="For pinging the user in #pathology-reports. Autofills when a Discord ID is found on a level."
                                        value={firstLevelDiscordID}
                                        onChange={e => setFirstLevelDiscordID(e.target.value)}
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
                { /* submit and toggles */ }
                <div className="mt-4 flex flex-row items-center gap-4">
                    <Button
                        variant="primary"
                        className="w-32"
                        onClick={() => formRef.current?.submit()}
                    >
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
                        title={forcePrivatePost ? "Private posting is forced in configuration" : undefined}
                        description="Posts to #pathology-lab"
                        showDescriptionAsTooltip
                        checked={doPrivatePost || forcePrivatePost}
                        onChange={() => setDoPrivatePost(!doPrivatePost)}
                    />
                </div>
            </Surface>
        </PeerReviewShell>
    )
}