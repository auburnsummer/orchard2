import { shadcnCssVariableResolver } from "@cafe/theme/cssVariableResolver";
import { shadcnTheme } from "@cafe/theme/theme";
import { MantineProvider } from "@mantine/core";
import { ReactNode } from "react";
import { Notifications } from "./Notifications";
import { useUser } from "@cafe/hooks/useUser";
import { LoadingBarContainer } from "react-top-loading-bar";
import { LoadingBar } from "./LoadingBar";


export function Prelude({children}: {children: ReactNode}) {
    const user = useUser();
    const theme = user.authenticated ? user.theme_preference : 'light';

    return (
        <>
            <MantineProvider theme={shadcnTheme} cssVariablesResolver={shadcnCssVariableResolver} forceColorScheme={theme}>
                <LoadingBarContainer>
                    <LoadingBar />
                    <Notifications />
                    { children }
                </LoadingBarContainer>
            </MantineProvider>
        </>
    )
}