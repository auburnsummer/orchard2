import { shadcnCssVariableResolver } from "@cafe/theme/cssVariableResolver";
import { shadcnTheme } from "@cafe/theme/theme";
import { MantineProvider, Overlay, useMantineTheme } from "@mantine/core";
import { ComponentType, useEffect, useState } from "react";
import { Notifications } from "../Notifications/Notifications";
import { useUser } from "@cafe/hooks/useUser";
import { useNavigationContext } from "@cafe/hooks/useNavigationContext";
import { LoadingBarContainer, useLoadingBar } from "react-top-loading-bar";

function LoadingBar() {
    const theme = useMantineTheme();
    const color = theme.colors.blue[4];
    const { pageLoading } = useNavigationContext();
    const [barStarted, setBarStarted] = useState(false);
    const { start, complete } = useLoadingBar({ color, height: 1 });

    useEffect(() => {
        if (pageLoading && !barStarted) {
            setBarStarted(true);
            start('static');
        } else {
            if (!pageLoading && barStarted) {
                setBarStarted(false);
                complete();
            }
        }
    }, [pageLoading, barStarted]);

    return null;
}

/**
 * Wraps a component to add global contexts, etc.
 * nb: Prelude is not itself a component. It's uppercase to allow fast-refresh to work:
 * https://github.com/vitejs/vite/discussions/4583#discussioncomment-1802717
 * @param Component 
 * @returns 
 */
export function Prelude<P extends {}>(Component: ComponentType<P>) {
    // -- not in a component so cannot use hooks in this area
    function Inner(props: P) {
        // -- now we are in a component
        const user = useUser();
        const theme = user.authenticated ? user.theme_preference : 'light';

        return (
            <>
                <MantineProvider theme={shadcnTheme} cssVariablesResolver={shadcnCssVariableResolver} forceColorScheme={theme}>
                    <LoadingBarContainer>
                        <LoadingBar />
                        <Notifications />
                        <Component {...props} />
                    </LoadingBarContainer>
                </MantineProvider>
            </>
        )
    }

    return Inner;
}