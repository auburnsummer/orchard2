import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { DailyBlendNavbar } from "./DailyBlendNavbar";

export function DailyBlendMainView() {
    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <Surface className="m-3 p-4">
                <Words variant="header" className="mb-4">
                    Daily Blend (WIP)
                </Words>
            </Surface>
        </Shell>
    )
}