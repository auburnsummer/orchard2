import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { LevelCard } from "@cafe/components/LevelCard/LevelCard";
import { Form } from "@cafe/minibridge/components/Form";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Button } from "@cafe/components/ui/Button";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

type DailyBlendRandomPoolProps = {
    pool: {
        level: RDLevel;
    }[];
};

export function DailyBlendRandomPool({ pool }: DailyBlendRandomPoolProps) {
    const csrfInput = useCSRFTokenInput();

    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <Surface className="m-3 p-4">
                <Words variant="header" className="mb-4">
                    Random Pool
                </Words>
                <Form className="flex flex-row gap-2 items-end" method="POST">
                    {csrfInput}
                    <TextInput label="Level ID" name="level_id" />
                    <Button type="submit" name="action" value="add" className="h-10" variant="primary">
                        Add Level
                    </Button>
                    <Button type="submit" name="action" value="remove" className="h-10" variant="danger">
                        Remove Level
                    </Button>
                </Form>
                {
                    pool.map(level => <LevelCard key={level.level.id} level={level.level} showId />)
                }
            </Surface>
        </Shell>
    )
}