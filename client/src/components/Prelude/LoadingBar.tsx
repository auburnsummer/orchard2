import { useNavigationContext } from "@cafe/hooks/useNavigationContext";
import { isLoadingAtom } from "@cafe/minibridge/atoms";
import { useMantineTheme } from "@mantine/core";
import { useAtomValue } from "jotai";
import { useState, useEffect } from "react";
import { useLoadingBar } from "react-top-loading-bar";

export function LoadingBar() {
    const theme = useMantineTheme();
    const pageLoading = useAtomValue(isLoadingAtom);
    const [barStarted, setBarStarted] = useState(false);

    const color = theme.colors.blue[4];
    const { start, complete } = useLoadingBar({ color, height: 1 });


    useEffect(() => {
        if (pageLoading && !barStarted) {
            setBarStarted(true);
            start('continuous');
        } else {
            if (!pageLoading && barStarted) {
                setBarStarted(false);
                complete();
            }
        }
    }, [pageLoading, barStarted]);

    return null;
}