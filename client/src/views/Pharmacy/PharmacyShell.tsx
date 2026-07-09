import { Shell } from "@cafe/components/Shell";
import { PharmacyNavbar } from "./PharmacyNavbar";
import { Surface } from "@cafe/components/ui/Surface";

export function PharmacyShell({ children }: { children: React.ReactNode }) {
    return (
        <Shell
            navbar={<PharmacyNavbar />}
        >
            <Surface className="m-3 p-4">
                {children}
            </Surface>
        </Shell>
    )
}