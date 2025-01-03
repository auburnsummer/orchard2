import { AppShell } from "@mantine/core";
import { Logo } from "./Logo";

import styles from './Shell.module.css';
import { useUser } from "@cafe/hooks/useUser";
import { Button } from '@mantine/core';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faDiscord } from '@fortawesome/free-brands-svg-icons'

type ShellProps = {
    children: React.ReactNode;
}

export function Shell({children}: ShellProps) {
    const user = useUser();

    return (
        <AppShell header={{height: '3rem'}}>
            <AppShell.Header className={styles.header}>
                <Logo />
                <div className={styles.spacer} />
                <div className={styles.userSection}>
                    <Button
                        leftSection={
                            <FontAwesomeIcon icon={faDiscord} />
                        }
                    >
                        Sign in with Discord
                    </Button>
                </div>
            </AppShell.Header>
            <AppShell.Main>
                {children}
            </AppShell.Main>
        </AppShell>
    )
}