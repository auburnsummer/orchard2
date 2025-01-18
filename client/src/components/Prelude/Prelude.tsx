import { shadcnCssVariableResolver } from "@cafe/theme/cssVariableResolver";
import { shadcnTheme } from "@cafe/theme/theme";
import { MantineProvider } from "@mantine/core";
import { ComponentType } from "react";
import { Notifications } from "../Notifications/Notifications";
import { useUser } from "@cafe/hooks/useUser";

/**
 * Wraps a component to add global contexts, etc.
 * nb: Prelude is not itself a component. It's uppercase to allow fast-refresh to work:
 * https://github.com/vitejs/vite/discussions/4583#discussioncomment-1802717
 * @param Component 
 * @returns 
 */
export function Prelude<P extends {}>(Component: ComponentType<P>) {
    function Inner(props: P) {
        const user = useUser();
        const theme = user.authenticated ? user.theme_preference : 'light';

        return (
            <>
                <MantineProvider theme={shadcnTheme} cssVariablesResolver={shadcnCssVariableResolver} forceColorScheme={theme}>
                    <Notifications />
                    <Component {...props} />
                </MantineProvider>
            </>
        )
    }

    return Inner;
}