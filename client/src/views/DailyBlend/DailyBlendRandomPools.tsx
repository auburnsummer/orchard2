import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { BlendPool } from "@cafe/types/blends"
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { Link } from "@cafe/minibridge/components/Link";
import { Button } from "@cafe/components/ui/Button";

type DailyBlendRandomPoolsProps = {
    pools: BlendPool[];
}

export function DailyBlendRandomPools({pools}: DailyBlendRandomPoolsProps) {
    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <title>Daily Blend Pools | Rhythm Café</title>
            <Surface className="m-3 p-4">
                <Words variant="header" className="mb-4">
                    Daily Blend Pools
                </Words>
                <Words as="p">
                    Select pool to edit:
                </Words>
                <ul>
                    {
                        pools.map(pool => (
                            <Words as="li" variant="link">
                                <Link href={`/daily-blend/random-pools/${pool.id}`}>{pool.name}</Link>
                            </Words>
                        ))
                    }
                </ul>
                <Button className="mt-2" variant="primary">
                    Add Pool
                </Button>
            </Surface>
        </Shell>
    )
}