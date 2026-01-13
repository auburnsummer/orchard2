import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { useSearchParams } from "@cafe/minibridge/hooks";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Table, TableBody, TableCell, TableHead, TableHeaderCell, TableRow } from "@cafe/components/ui/Table";
import { useMemo, useState } from "react";
import { Link } from "@cafe/minibridge/components/Link";
import { Button } from "@cafe/components/ui/Button";
import { Dialog } from "@cafe/components/ui/Dialog";
import { Form } from "@cafe/minibridge/components/Form";
import { TextInput } from "@cafe/components/ui/TextInput";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

type DailyBlend = {
    level: RDLevel,
    featured_date: string, // ISO format YYYY-MM-DD
    blended: boolean,
}

type DailyBlendScheduleProps = {
    blends: DailyBlend[];
    year: number;
    month: number;
}

type DailyBlendCellProps = {
    day: number;
    level: RDLevel | null;
    onEditClick?: () => void;
}

function DailyBlendCell({ day, level, onEditClick }: DailyBlendCellProps) {
    return (
        <TableCell>
            <div className="flex flex-col">
                <div className="flex flex-row justify-items">
                    <Words variant="muted" className="text-xs">{day}</Words>
                    <Words variant="link" className="text-xs ml-2 hover:cursor-pointer" onClick={onEditClick}>
                        (edit)
                    </Words>
                </div>
                <div className="mt-1">
                    {
                        level !== null ? (
                            <Link href={`/levels/${level.id}/`}>
                                <Words variant="link">{level.song}</Words>
                            </Link>
                        ) : (
                            <Words variant="muted">Pool</Words>
                        )
                    }
                </div>
            </div>
        </TableCell>
    )
}

export function DailyBlendSchedule(props: DailyBlendScheduleProps) {
    const [, navigateViaSearchParams] = useSearchParams();
    const csrfInput = useCSRFTokenInput();

    const year = props.year;
    const monthOneIndexed = props.month; // this came from python, Jan = 1 in python, Jan = 0 in JS
    const month = monthOneIndexed - 1;

    // setting day to 0 gets last day of previous month
    const daysInThisMonth = new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
    // but here we'll subtract 1 for JS 0-indexed months
    const [selectedDate, setSelectedDate] = useState<Date>(new Date(Date.UTC(year, month, 1)));
    const [showEditDialog, setShowEditDialog] = useState<boolean>(false);

    console.log(props.blends);

    const levelMap = useMemo(() => {
        const map: Record<number, RDLevel> = {};
        props.blends.forEach(blend => {
            const date = new Date(blend.featured_date);
            map[date.getUTCDate()] = blend.level;
        });
        return map;
    }, [props.blends]);

    const rows = useMemo(() => {
        const cells = [];
        for (let day = 1; day <= daysInThisMonth; day++) {
            cells.push(
                <DailyBlendCell
                    key={day}
                    day={day}
                    level={levelMap[day] || null}
                    onEditClick={() => {
                        setShowEditDialog(true);
                        setSelectedDate(new Date(Date.UTC(year, month, day)));
                    }}
                />
            );
        }
        // add padding cells to align first day of month correctly
        const firstDayOfMonth = new Date(year, month, 1).getDay(); // 0 (Sun) to 6 (Sat)
        const paddingCells = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;
        for (let i = 0; i < paddingCells; i++) {
            cells.unshift(
                <TableCell key={`pad-${i}`}><></></TableCell>
            );
        }
        // break into groups of 7
        const rows = [];
        for (let i = 0; i < cells.length; i += 7) {
            rows.push(
                <TableRow key={`row-${i / 7}`}>
                    {cells.slice(i, i + 7)}
                </TableRow>
            );
        }
        return rows;
    }, [props.blends, year, month, daysInThisMonth]);

    const forwardOneMonth = () => {
        navigateViaSearchParams(params => {
            params.set('month', (monthOneIndexed % 12 + 1).toString());
            if (monthOneIndexed === 12) {
                params.set('year', (year + 1).toString());
            }
        });
    };

    const backwardOneMonth = () => {
        navigateViaSearchParams(params => {
            params.set('month', ((monthOneIndexed + 10) % 12 + 1).toString());
            if (monthOneIndexed === 1) {
                params.set('year', (year - 1).toString());
            }
        });
    };

    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <Dialog
                open={showEditDialog}
                onClose={() => setShowEditDialog(false)}
            >
                <Form method="POST" onSubmit={() => setShowEditDialog(false)}>
                    {csrfInput}
                    <input type="hidden" name="featured_date" value={selectedDate?.toISOString().split("T")[0]} />
                    <Words variant="header">Edit Daily Blend for {selectedDate?.toDateString()}</Words>
                    <TextInput label="Level ID (leave blank to clear schedule)" name="level_id" />
                    <Button className="mt-2" type="submit" variant="primary">Save</Button>
                </Form>
            </Dialog>
            <Surface className="m-3 p-4 flex flex-col gap-2">
                <Words variant="header" className="mb-4">
                    Schedule for {year}-{(month+1).toString().padStart(2, '0')}
                </Words>
                <div className="flex justify-between mb-2">
                    <Button
                        onClick={backwardOneMonth}
                    >
                        Previous Month
                    </Button>
                    <Button
                        onClick={forwardOneMonth}
                    >
                        Next Month
                    </Button>
                </div>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableHeaderCell>Mon</TableHeaderCell>
                            <TableHeaderCell>Tue</TableHeaderCell>
                            <TableHeaderCell>Wed</TableHeaderCell>
                            <TableHeaderCell>Thu</TableHeaderCell>
                            <TableHeaderCell>Fri</TableHeaderCell>
                            <TableHeaderCell>Sat</TableHeaderCell>
                            <TableHeaderCell>Sun</TableHeaderCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {rows}
                    </TableBody>
                </Table>
            </Surface>
        </Shell>
    )
}