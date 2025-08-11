import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter/ShellDramaticCenter";
import { navigateAtom } from "@cafe/minibridge/atoms";
import { djangoGet } from "@cafe/minibridge/fetch";
import { RDLevelPrefill } from "@cafe/types/rdLevelPrefill";
import { Loader, Paper, Stack, Text, Alert } from "@mantine/core";
import { useSetAtom } from "jotai";
import { useEffect } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faExclamationCircle } from "@fortawesome/free-solid-svg-icons";

type PrefillLoadingProps = {
    error: string;
}

export function PrefillLoading({error}: PrefillLoadingProps) {
    const navigate = useSetAtom(navigateAtom);
    
    useEffect(() => {
        const interval = setInterval(async () => {
            const url = `${window.location.origin}${window.location.pathname}?_cache=${Math.random()}`;
            const resp = await djangoGet(url);
            if (resp.action === "render") {
                const props = resp.props.prefill as RDLevelPrefill;
                if (props.ready || props.errors) {
                    clearInterval(interval);
                    navigate(new URL(window.location.href), true);
                }
            }
        }, 500);
        return () => {
            clearInterval(interval);
        }
    }, []);

    return (
        <ShellDramaticCenter>
            <Paper shadow="md" p="xl">
                {
                    error === ""
                        ? (
                        <Stack align="center">
                            <Loader size="2rem" />
                            <Text>Analysing level...</Text>
                        </Stack>
                        )
                        : (
                            <Stack>
                                <Text>An error occurred while attempting to analyse this level:</Text>
                                <Alert variant="light" color="red" title="Error Trace" icon={<FontAwesomeIcon icon={faExclamationCircle} />}>
                                    <pre>{error}</pre>
                                </Alert>
                                <Text>Please try the command again. If it still doesn't work, let Auburn know, thanks</Text>
                            </Stack>
                        )
                }
            </Paper>
        </ShellDramaticCenter>
    )
}