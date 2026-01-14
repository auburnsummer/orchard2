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
                    Daily Blend
                </Words>
                <Words as="p">
                    The current time in GMT is {new Date().toUTCString()}.
                </Words>
                {/* <Words as="p">
                    Blends occur at <span className="font-bold">05:00 GMT.</span>
                </Words> */}
                <Words as="p">
                    Select "Blend Now" from the navigation to trigger an immediate blend.
                    Doing so disables the scheduled blend for the day.
                </Words>
                <Words as="p">
                    Please ping Auburn for any issues or feature requests.
                </Words>
            </Surface>
        </Shell>
    )
}