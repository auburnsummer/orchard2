import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter/ShellDramaticCenter";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Button, Paper, Select, Stack } from "@mantine/core";
import { useState } from "react";

type LevelAddTypeSelectProps = {
    code: string;
    code_valid: boolean;
}

export function LevelAddTypeSelect({code: _code, code_valid}: LevelAddTypeSelectProps) {
    const [addType, setAddType] = useState<string| null>(null);
    const csrfInput = useCSRFTokenInput();

    const selectData = [
        {value: 'new', label: 'New Level'},
        {value: 'update', label: 'Update Existing Level'},
    ];

    const content = code_valid
        ? (
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
        ) : (
            <>
                <p>This link to add a level is invalid or has expired.</p>
                <p>Please run the command again to get a fresh link.</p>
            </>
        )


    return (
        <ShellDramaticCenter>
            <Paper shadow="md" p="xl">
                { content }
            </Paper>
        </ShellDramaticCenter>
    )
}