import { useCurrentRequestId, useIsLoading } from "@cafe/minibridge/hooks";
import { useMantineTheme } from "@mantine/core";
import { useState, useEffect } from "react";
import { useLoadingBar } from "react-top-loading-bar";

export function LoadingBar() {
    const theme = useMantineTheme();
    const pageLoading = useIsLoading();
    const currentRequestId = useCurrentRequestId();
    const [barStarted, setBarStarted] = useState(false);

    const color = theme.colors.blue[4];
    const { start, complete } = useLoadingBar({ color, height: 1 });


    useEffect(() => {
        if (pageLoading && !barStarted) {
            setBarStarted(true);
            start('continuous');
        } else if (!pageLoading && barStarted) {
            setBarStarted(false);
            complete();
        }
    }, [pageLoading, barStarted]);

    useEffect(() => {
        if (barStarted) {
            // if the request id changes, we should restart the bar
            // because it means they clicked something else while the bar was still loading
            start('continuous');
        }
    }, [currentRequestId]);

    return null;
}