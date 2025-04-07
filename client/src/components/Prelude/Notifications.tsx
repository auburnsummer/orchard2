import { useEffect } from "react";

import { Notifications as MantineNotifications, notifications } from '@mantine/notifications';
import { useAtom } from "jotai";
import { messagesAtom } from "@cafe/minibridge/atoms";


export function Notifications() {
    const [messages, setMessages] = useAtom(messagesAtom);

    useEffect(() => {
        if (messages.length > 0) {
            const message = messages.at(0);
            if (message) {
                const color = {
                    "error": "red",
                    "success": "green",
                    "info": "blue",
                    "warning": "yellow"
                }[message.level];
                notifications.show({
                    message: message.html,
                    color
                });
            }
            setMessages(prev => prev.slice(1));
        }
    }, [messages]);

    return <MantineNotifications />;
}