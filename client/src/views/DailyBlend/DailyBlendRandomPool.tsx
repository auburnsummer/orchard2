import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Form } from "@cafe/minibridge/components/Form";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Button } from "@cafe/components/ui/Button";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Table, TableBody, TableCell, TableHead, TableHeaderCell, TableRow } from "@cafe/components/ui/Table";
import { useState } from "react";
import { Link } from "@cafe/minibridge/components/Link";

type DailyBlendRandomPoolProps = {
    pool: {
        level: RDLevel;
    }[];
};

export function DailyBlendRandomPool({ pool }: DailyBlendRandomPoolProps) {
    const csrfInput = useCSRFTokenInput();

    const [levelId, setLevelId] = useState("");

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
                    <TextInput
                        label="Level ID"
                        name="level_id"
                        value={levelId}
                        onChange={(e) => setLevelId(e.target.value)}
                    />
                    <Button type="submit" name="action" value="add" className="h-10" variant="primary">
                        This level dives into the pool.
                    </Button>
                    <Button type="submit" name="action" value="remove" className="h-10" variant="secondary">
                        A lifeguard rescues this level from the pool.
                    </Button>
                </Form>
                <Table className="mt-4">
                    <TableHead>
                        <TableRow>
                            <TableHeaderCell firstColumn>Song</TableHeaderCell>
                            <TableHeaderCell>Artist</TableHeaderCell>
                            <TableHeaderCell>User</TableHeaderCell>
                            <TableHeaderCell lastColumn>ID (click to select)</TableHeaderCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            pool.map(({ level }) => (
                                <TableRow key={level.id}>
                                    <TableCell firstColumn>
                                        <Link
                                            href={`/levels/${level.id}/`}
                                        >
                                            <Words variant="link">
                                                {level.song}
                                            </Words>
                                        </Link>
                                    </TableCell>
                                    <TableCell>
                                        <Words>{level.artist}</Words>
                                    </TableCell>
                                    <TableCell>
                                        <Words>{level.authors.join(', ')}</Words>
                                    </TableCell>
                                    <TableCell lastColumn>
                                        <Button
                                            variant="secondary"
                                            onClick={() => setLevelId(level.id)}
                                        >
                                            {level.id}
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))
                        }
                    </TableBody>
                </Table>
            </Surface>
        </Shell>
    )
}