import { RDLevel } from "@cafe/types/rdLevelBase";
import { PeerReviewShell } from "./PeerReviewShell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Toggle } from "@cafe/components/ui/Toggle";
import { Button } from "@cafe/components/ui/Button";
import Fieldset from "@cafe/components/ui/Fieldset";
import { atomWithStorage } from "jotai/utils";
import { useAtom, useAtomValue } from "jotai";

// Simple CRC32 implementation for verification codes
function crc32(str: string): string {
    if (!str) return "";
    let crc = 0xFFFFFFFF;
    for (let i = 0; i < str.length; i++) {
        crc ^= str.charCodeAt(i);
        for (let j = 0; j < 8; j++) {
            crc = (crc >>> 1) ^ (0xEDB88320 & -(crc & 1));
        }
    }
    return ((crc ^ 0xFFFFFFFF) >>> 0).toString(16).toUpperCase().padStart(8, '0');
}

type PeerReviewConfigurationProps = {
    levels: RDLevel[];
};

export const pathlabWebhookUrlAtom = atomWithStorage("pathlabWebhookUrl", ""); // Pathology-Lab Webhook
export const publicWebhookUrlAtom = atomWithStorage("publicWebhookUrl", ""); // Pathology-Reports Webhook
export const prAvatarAtom = atomWithStorage("prAvatar", "");
export const nrAvatarAtom = atomWithStorage("nrAvatar", "");
export const pdAvatarAtom = atomWithStorage("pdAvatar", "");
export const prFlairTextAtom = atomWithStorage("prFlairText", "");
export const nrFlairTextAtom = atomWithStorage("nrFlairText", "");
export const pdFlairTextAtom = atomWithStorage("pdFlairText", "");
export const dcNickAtom = atomWithStorage("dcNick", ""); // Discord Nickname
export const dcIDAtom = atomWithStorage("dcID", ""); // Discord ID

export const forcePrivatePostAtom = atomWithStorage("forcePrivatePost", true);
export const doPrivatePostAtom = atomWithStorage("doPrivatePost", true);
export const doPublicPostAtom = atomWithStorage("doPublicPost", true);
export const doIPCAtom = atomWithStorage("doIPC", true); // Include Public Comments in Private Comments

export function useIsConfigured() {
    const pathlabWebhookUrl = useAtomValue(pathlabWebhookUrlAtom);
    const publicWebhookUrl = useAtomValue(publicWebhookUrlAtom);
    return pathlabWebhookUrl !== "" && publicWebhookUrl !== "";
}

export function PeerReviewConfiguration({ levels }: PeerReviewConfigurationProps) {
    const [pathlabWebhookUrl, setPathlabWebhookUrl] = useAtom(pathlabWebhookUrlAtom);
    const [publicWebhookUrl, setPublicWebhookUrl] = useAtom(publicWebhookUrlAtom);
    const [prAvatar, setPrAvatar] = useAtom(prAvatarAtom);
    const [nrAvatar, setNrAvatar] = useAtom(nrAvatarAtom);
    const [pdAvatar, setPdAvatar] = useAtom(pdAvatarAtom);
    const [prFlairText, setPrFlairText] = useAtom(prFlairTextAtom);
    const [nrFlairText, setNrFlairText] = useAtom(nrFlairTextAtom);
    const [pdFlairText, setPdFlairText] = useAtom(pdFlairTextAtom);
    const [dcNick, setDcNick] = useAtom(dcNickAtom);
    const [dcID, setDcID] = useAtom(dcIDAtom);
    const [forcePrivatePost, setForcePrivatePost] = useAtom(forcePrivatePostAtom);
    const [doPrivatePost, setDoPrivatePost] = useAtom(doPrivatePostAtom);
    const [doPublicPost, setDoPublicPost] = useAtom(doPublicPostAtom);
    const [doIPC, setDoIPC] = useAtom(doIPCAtom);

    return <PeerReviewShell pendingLevels={levels}>
        <Surface className="m-3 p-4">
            <div className="flex items-center justify-between mb-4">
                <Words variant="subheader">
                    Peer Review Configuration
                </Words>
            </div>

            <div className="space-y-6">
                <Fieldset legend="Webhooks">
                    <div className="space-y-4">
                        <TextInput
                            id="pathlabWebhookUrl"
                            label="Pathology-Lab (Private) Webhook URL"
                            description={pathlabWebhookUrl 
                                ? `Verification: ${crc32(pathlabWebhookUrl)}`
                                : "See pins in #pathology-lab for more information."}
                            value={pathlabWebhookUrl}
                            onChange={(e) => setPathlabWebhookUrl(e.target.value)}
                            placeholder="https://discord.com/api/webhooks/..."
                            className="w-full"
                            required
                        />
                        <TextInput
                            id="publicWebhookUrl"
                            label="Pathology-Reports (Public) Webhook URL"
                            description={publicWebhookUrl 
                                ? `Verification: ${crc32(publicWebhookUrl)}`
                                : "See pins in #pathology-reports for more information."}
                            value={publicWebhookUrl}
                            onChange={(e) => setPublicWebhookUrl(e.target.value)}
                            placeholder="https://discord.com/api/webhooks/..."
                            className="w-full"
                            required
                        />
                    </div>
                </Fieldset>

                <Fieldset legend="Avatar URLs">
                    <div className="space-y-4">
                        <TextInput
                            id="prAvatar"
                            label="Peer Reviewed (PR) Avatar"
                            description="A direct link to an image to show in #pathology-lab for when you Peer-Review a level."
                            value={prAvatar}
                            onChange={(e) => setPrAvatar(e.target.value)}
                            placeholder="https://..."
                            className="w-full"
                        />
                        <TextInput
                            id="nrAvatar"
                            label="Non-Refereed (NR) Avatar"
                            description="A direct link to an image to show in #pathology-lab for when you Non-Referee a level."
                            value={nrAvatar}
                            onChange={(e) => setNrAvatar(e.target.value)}
                            placeholder="https://..."
                            className="w-full"
                        />
                        <TextInput
                            id="pdAvatar"
                            label="Pending (PD) Avatar"
                            description="A direct link to an image to show in #pathology-lab for when you set a level as Pending."
                            value={pdAvatar}
                            onChange={(e) => setPdAvatar(e.target.value)}
                            placeholder="https://..."
                            className="w-full"
                        />
                    </div>
                </Fieldset>

                <Fieldset legend="Flair Text">
                    <div className="space-y-4">
                        <TextInput
                            id="prFlairText"
                            label="PR Flair Text"
                            description="A little blurb of text sent in #pathology-lab for when you Peer-Review a level."
                            value={prFlairText}
                            onChange={(e) => setPrFlairText(e.target.value)}
                            placeholder="Peer Reviewed"
                            className="w-full"
                        />
                        <TextInput
                            id="nrFlairText"
                            label="NR Flair Text"
                            description="A little blurb of text sent in #pathology-lab for when you Non-Referee a level."
                            value={nrFlairText}
                            onChange={(e) => setNrFlairText(e.target.value)}
                            placeholder="Non-Refereed"
                            className="w-full"
                        />
                        <TextInput
                            id="pdFlairText"
                            label="PD Flair Text"
                            description="A little blurb of text sent in #pathology-lab for when you set a level as Pending."
                            value={pdFlairText}
                            onChange={(e) => setPdFlairText(e.target.value)}
                            placeholder="Pending"
                            className="w-full"
                        />
                    </div>
                </Fieldset>

                <Fieldset legend="Discord Info">
                    <div className="space-y-4">
                        <TextInput
                            id="dcNick"
                            label="Discord Nickname"
                            description="Your Discord Username or Nickname, sent in #pathology-lab to show who reviewed the level."
                            value={dcNick}
                            onChange={(e) => setDcNick(e.target.value)}
                            placeholder="Your Discord username"
                            className="w-full"
                        />
                        <TextInput
                            id="dcID"
                            label="Discord ID"
                            description="Your Discord ID, pinged in #pathology-lab to show who reviewed the level. This ping does not notify you."
                            value={dcID}
                            onChange={(e) => setDcID(e.target.value)}
                            placeholder="123456789012345678"
                            className="w-full"
                        />
                    </div>
                </Fieldset>

                <Fieldset legend="Posting Options">
                    <div className="space-y-4">
                        <Toggle
                            id="forcePrivatePost"
                            label="Force Private Post"
                            description="Force posts to be private."
                            checked={forcePrivatePost}
                            onChange={(e) => setForcePrivatePost(e.target.checked)}
                        />
                        <Toggle
                            id="doPrivatePost"
                            label="Do Private Post"
                            checked={doPrivatePost}
                            onChange={(e) => setDoPrivatePost(e.target.checked)}
                        />
                        <Toggle
                            id="doPublicPost"
                            label="Do Public Post"
                            checked={doPublicPost}
                            onChange={(e) => setDoPublicPost(e.target.checked)}
                        />
                        <Toggle
                            id="doIPC"
                            label="Include Public Comments in Private Comments"
                            checked={doIPC}
                            onChange={(e) => setDoIPC(e.target.checked)}
                        />
                    </div>
                </Fieldset>
            </div>
        </Surface>
    </PeerReviewShell>;
}