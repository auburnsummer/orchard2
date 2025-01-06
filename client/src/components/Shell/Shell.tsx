import { AppShell, Avatar, Button, Menu, UnstyledButton } from "@mantine/core";
import { Logo } from "./Logo";
import styles from './Shell.module.css';
import { useUser } from "@cafe/hooks/useUser";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faDiscord } from '@fortawesome/free-brands-svg-icons'
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useRef } from "react";

type ShellProps = {
    children: React.ReactNode;
}

export function Shell({children}: ShellProps) {
    const user = useUser();
    const csrfInput = useCSRFTokenInput();

    const logOutForm = useRef<HTMLFormElement>(null);

    return (
        <AppShell header={{height: '3rem'}}>
            <AppShell.Header className={styles.header}>
                <Logo />
                <div className={styles.spacer} />
                <div className={styles.userSection}>
                    {
                        user.authenticated
                            ? (
                                <>
                                    <form method="post" action="/accounts/logout/" ref={logOutForm}>
                                        { csrfInput }
                                    </form>
                                    <Menu shadow="md" width={200}>
                                        <Menu.Target>
                                            <UnstyledButton className={styles.userSectionButton}>
                                                <Avatar src={user.avatarURL} name={user.displayName} alt={user.username} radius="xl" />
                                            </UnstyledButton>
                                        </Menu.Target>
                                        <Menu.Dropdown>
                                            <Menu.Label>{user.displayName}</Menu.Label>
                                            <Menu.Item
                                                component="a"
                                                href="/accounts/profile/"
                                            >
                                                Profile
                                            </Menu.Item>
                                            <Menu.Item
                                                onClick={() => {
                                                    logOutForm.current?.submit();
                                                }}
                                            >
                                                Log out
                                            </Menu.Item>
                                        </Menu.Dropdown>
                                    </Menu>
                                </>
                            )
                            : (
                                <form method="post" action="/accounts/discord/login/">
                                    { csrfInput }
                                    <Button
                                        type="submit"
                                        leftSection={
                                            <FontAwesomeIcon icon={faDiscord} />
                                        }
                                    >
                                        Sign in with Discord
                                    </Button>
                                </form>
                            )
                    }
                </div>
            </AppShell.Header>
            <AppShell.Main>
                {children}
            </AppShell.Main>
        </AppShell>
    )
}