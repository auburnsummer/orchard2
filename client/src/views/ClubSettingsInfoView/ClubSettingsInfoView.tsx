import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";

type ClubSettingsInfoViewProps = {
    club: Club
};

export function ClubSettingsInfoView({club}: ClubSettingsInfoViewProps) {
    return (
        <Shell>
            <p>club settings info view</p>
            <p>name: {club.name}</p>
            <pre>
            </pre>
        </Shell>
    )
}