import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter/ShellDramaticCenter";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@django-bridge/react";
import { Button, Paper, Select, Stack } from "@mantine/core";
import { useState } from "react";

type LevelAddTypeSelectProps = {
    code: string;
}

export function LevelAddTypeSelect({code}: LevelAddTypeSelectProps) {
    const [addType, setAddType] = useState<string| null>(null);
    const csrfInput = useCSRFTokenInput();

    const selectData = [
        {value: 'new', label: 'New Level'},
        {value: 'update', label: 'Update Existing Level'},
    ];

    return (
        <ShellDramaticCenter>
            <Paper shadow="md" p="xl">
                <Form
                    method="POST"
                >
                    {csrfInput}
                    <Stack align="start" justify="start">
                        <Select
                            clearable
                            value={addType}
                            label="Is this a new level or an update to an existing level?"
                            data={selectData}
                            onChange={setAddType}
                            name="prefill_type"
                        >
                        </Select>
                        <Button type="submit" disabled={addType == null}>Continue</Button>
                    </Stack>
                </Form>
            </Paper>
        </ShellDramaticCenter>
    )
}