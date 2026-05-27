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
import { useRef, useState } from "react";
import { Link } from "@cafe/minibridge/components/Link";
import { BlendPool } from "@cafe/types/blends";
import { useDisclosure } from "@mantine/hooks";
import { Dialog } from "@cafe/components/ui/Dialog";
import { extractIdFromUrlInput } from "@cafe/utils/extractIdFromUrlInput";
import Select from "@cafe/components/ui/Select";

type DailyBlendRandomPoolProps = {
    pool: BlendPool;
    pool_items: {
        level: RDLevel;
        tickets: number;
    }[];
};

function EditDailyBlendRandomPoolForm({ pool, onSubmit }: { pool: BlendPool, onSubmit: () => void }) {
    const csrfInput = useCSRFTokenInput();

    const deleteFormRef = useRef<HTMLFormElement>(null);

    const [confirmDelete, setConfirmDelete] = useState(false);

    const onDeleteClick = () => {
        if (!confirmDelete) {
            setConfirmDelete(true);
        } else {
            deleteFormRef.current?.submit();
        }
    }

    return (
        <>
        {/* invisible delete form */}
        <Form
            method="POST"
            action={`/daily-blend/random-pools/${pool.id}/delete/`}
            ref={deleteFormRef}
        >
            {csrfInput}
        </Form>
        <Form
            method="POST"
            action={`/daily-blend/random-pools/${pool.id}/edit/`}
            className="flex flex-col gap-4"
            onSubmit={onSubmit}
        >
            {csrfInput}
            <TextInput
                label="Pool name"
                name="name"
                defaultValue={pool.name}
            />
            <Select
                data={[
                    { value: "flat", label: "Flat -- equal chance for all levels" },
                    { value: "aging", label: "Aging -- levels become more likely over time" },
                ]}
                label="Weighting system"
                name="weighting_system"
                defaultValue={pool.weighting_system}
            >
            </Select>

            <div className="flex flex-row gap-2 items-end justify-stretch mt-6">
                <Button type="submit" variant="primary">
                    Save
                </Button>
                <Button type="button" variant="danger" onClick={onDeleteClick}>
                    {confirmDelete ? "Click again to confirm delete" : "Delete pool"}
                </Button>
            </div>
        </Form>
        </>
    );
}

export function DailyBlendRandomPool({ pool, pool_items }: DailyBlendRandomPoolProps) {
    const csrfInput = useCSRFTokenInput();

    const [levelId, setLevelId] = useState("");
    const submittedId = extractIdFromUrlInput(levelId);

    const [isOpen, { open, close }] = useDisclosure(false);

    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <title>Daily Blend Random Pool | Rhythm Café</title>
            <Dialog
                open={isOpen}
                onClose={close}
            >
                <EditDailyBlendRandomPoolForm pool={pool} onSubmit={close} />
            </Dialog>
            <Surface className="m-3 p-4">
                <div className="flex flex-row mb-4 items-baseline">
                    <Words variant="header">
                        {pool.name}
                    </Words>
                    <Words variant="muted" className="text-xs ml-2">
                        (id: {pool.id})
                    </Words>
                    <Button variant="default" className="ml-4" onClick={open}>
                        Pool settings
                    </Button>
                </div>
                <Form className="flex flex-row gap-2 items-end" method="POST" onSubmit={() => setLevelId("")}>
                    {csrfInput}
                    <input type="hidden" name="level_id" value={submittedId} />
                    <TextInput
                        label="Level ID"
                        value={levelId}
                        onChange={(e) => setLevelId(e.target.value)}
                    />
                    <Button type="submit" name="action" value="add" className="h-10" variant="primary">
                        Add level to pool
                    </Button>
                    <Button type="submit" name="action" value="remove" className="h-10" variant="secondary">
                        Remove level from pool
                    </Button>
                    {
                        pool.weighting_system === "aging" && (
                            <>
                                <div className="flex-grow" />
                                <div className="flex flex-row ml-4 justify-end items-end gap-4">
                                    <TextInput
                                        label="Change tickets"
                                        className="w-32"
                                        name="tickets"
                                        type="number"
                                        defaultValue={1}
                                        min={0}
                                    />
                                    <Button type="submit" name="action" value="ticket" variant="default">
                                        Set tickets
                                    </Button>
                                </div>
                            </>
                        )
                    }
                </Form>
                <Table className="mt-4">
                    <TableHead>
                        <TableRow>
                            <TableHeaderCell firstColumn>Song</TableHeaderCell>
                            <TableHeaderCell>Artist</TableHeaderCell>
                            <TableHeaderCell>User</TableHeaderCell>
                            {
                                pool.weighting_system === "aging" && (
                                    <TableHeaderCell>Tickets</TableHeaderCell>
                                )
                            }
                            <TableHeaderCell lastColumn>ID (click to select)</TableHeaderCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            pool_items.map(({ level, tickets }) => (
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
                                    {
                                        pool.weighting_system === "aging" && (
                                            <TableCell>
                                                {tickets}
                                            </TableCell>
                                        )
                                    }
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