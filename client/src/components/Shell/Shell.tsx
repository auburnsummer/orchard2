import { AppShell, Avatar, Button, Menu, UnstyledButton } from "@mantine/core";
import { Logo } from "./Logo";
import styles from './Shell.module.css';
import { useUser } from "@cafe/hooks/useUser";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faDiscord } from '@fortawesome/free-brands-svg-icons'
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useRef } from "react";
import cc from "clsx";
import { Link } from "@cafe/minibridge/components/Link";

export type ShellProps = {
    children: React.ReactNode;
    navbar?: React.ReactNode;
    aside?: React.ReactNode;
}

export function Shell({ children, navbar, aside }: ShellProps) {
    const user = useUser();
    const csrfInput = useCSRFTokenInput();

    const logOutForm = useRef<HTMLFormElement>(null);

    return (
        <AppShell
            header={{ height: '3rem' }}
            navbar={navbar !== undefined ? { width: '16rem', breakpoint: 0 } : undefined}
            aside={aside !== undefined ? { width: '24rem', breakpoint: 0 } : undefined}
            className={styles.shell}
        >
            <AppShell.Header className={styles.header}>
                <Logo />
                <div className={styles.spacer} />
                <div className={styles.userSection}>
                    {
                        user.authenticated
                            ? (
                                <>
                                    <form method="post" action="/accounts/logout/" ref={logOutForm}>
                                        {csrfInput}
                                    </form>
                                    <Menu shadow="md" width={200}>
                                        <Menu.Target>
                                            <UnstyledButton className={styles.userSectionButton}>
                                                <Avatar src={user.avatarURL} name={user.displayName} alt={user.displayName} radius="xl" />
                                            </UnstyledButton>
                                        </Menu.Target>
                                        <Menu.Dropdown>
                                            <Menu.Label>{user.displayName}</Menu.Label>
                                            <Menu.Item
                                                component={Link}
                                                href="/accounts/profile/"
                                            >
                                                Profile
                                            </Menu.Item>
                                            {
                                                user.is_superuser && (
                                                    <Menu.Item
                                                        component={Link}
                                                        href="/adminnn/"
                                                    >
                                                        Admin
                                                    </Menu.Item>
                                                )
                                            }
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
                                    {csrfInput}
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
            {navbar && (
                <AppShell.Navbar>
                    {navbar}
                </AppShell.Navbar>
            )}
            {aside && (
                <AppShell.Aside>
                    {aside}
                </AppShell.Aside>
            )}
            <AppShell.Main className={styles.mainArea}>
                <div className={cc(navbar && styles.mainAreaWithNavbar, styles.mainAreaInner)}>
                    {children}
                </div>
            </AppShell.Main>
        </AppShell>
    )
}