import { RDLevel } from "@cafe/types/rdLevelBase";
import { PeerReviewShell } from "./PeerReviewShell";
import { Surface } from "@cafe/components/ui/Surface";
import { PixelButton } from "./PixelButton";
import { useState } from "react";
import { BAD_THING_CATS, BAD_THINGS } from "./constants";
import Fieldset from "@cafe/components/ui/Fieldset";
import { Checkbox } from "@cafe/components/ui/Checkbox";

type PeerReviewMainViewProps = {
    levels: RDLevel[];
    rdlevel: RDLevel;
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
    if (approval > 0) return { text: 'Peer-Reviewed', variant: 'pr' };
    if (approval < 0) return { text: 'Non-Refereed', variant: 'nr' };
    return { text: 'Pending', variant: 'pd' };
}

export function PeerReviewLevelView({ levels, rdlevel }: PeerReviewMainViewProps) {
    const approvalStatus = getApprovalStatus(rdlevel.approval);

    const [reasons, setReasons] = useState<Set<string>>(new Set());

    return (
        <PeerReviewShell pendingLevels={levels}>
            <Surface className="m-4 relative p-6 shadow-xl border border-gray-300 dark:border-gray-700 bg-white/70 dark:bg-slate-800/70 backdrop-blur-lg overflow-hidden">
                {/* Background Blur Image */}
                <div 
                    className="absolute inset-0 opacity-10 blur-xl"
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

                {/* Approval Badge */}
                <br />
                <PixelButton variant={approvalStatus.variant}>
                    {approvalStatus.text}
                </PixelButton>

                {/* Timestamp */}
                <div className="absolute top-2 right-4 flex flex-col items-end z-10 space-y-1">
                    <div className="text-xs text-gray-700 dark:text-gray-300 font-medium">
                        {new Date(rdlevel.last_updated).toLocaleString()}
                    </div>
                </div>

                {/* form display */}
                {
                    BAD_THING_CATS.map(cat => (
                        <Fieldset legend={cat} key={cat} className="capitalize">
                            <div className="normal-case">
                                {
                                    BAD_THINGS.filter(bt => bt.category === cat).map(bt => (
                                        <Checkbox
                                            key={bt.name}
                                            label={bt.name}
                                            description={bt.description}
                                            showDescriptionAsTooltip
                                        />
                                    ))
                                }
                            </div>
                        </Fieldset>
                    ))
                }
            </Surface>
        </PeerReviewShell>
    )
}