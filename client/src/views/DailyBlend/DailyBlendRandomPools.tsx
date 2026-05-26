import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { BlendPool } from "@cafe/types/blends"
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { Link } from "@cafe/minibridge/components/Link";
import { Button } from "@cafe/components/ui/Button";
import { useDisclosure } from "@mantine/hooks";
import { Dialog } from "@cafe/components/ui/Dialog";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { TextInput } from "@cafe/components/ui/TextInput";

type DailyBlendRandomPoolsProps = {
    pools: BlendPool[];
}

function CreateBlendPoolForm({onSubmit}: {onSubmit?: () => void}) {
    const csrfInput = useCSRFTokenInput();
    
    return (
        <Form method="POST" onSubmit={onSubmit}>
            <div className="flex flex-col gap- items-start">
                <TextInput
                    name="name"
                    label="Pool name"
                    description="You can change this at any time."
                />
                <Button type="submit" variant="primary" className="mt-4">Create pool</Button>
            </div>
            {csrfInput}
        </Form>
    )
}

export function DailyBlendRandomPools({pools}: DailyBlendRandomPoolsProps) {
  const [createPoolOpen, { open: openCreatePool, close: closeCreatePool }] =
    useDisclosure(false);

    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <title>Daily Blend Pools | Rhythm Café</title>
            <Dialog open={createPoolOpen} onClose={closeCreatePool}>
                <CreateBlendPoolForm onSubmit={closeCreatePool} />
            </Dialog>
        
            <Surface className="m-3 p-4">
                <Words variant="header" className="mb-4">
                    Daily Blend Pools
                </Words>
                <Words as="p">
                    Select pool:
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
                <Button className="mt-4" variant="primary" onClick={openCreatePool}>
                    Add Pool
                </Button>
            </Surface>
        </Shell>
    )
}