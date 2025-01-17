import { Message, MessagesContext } from "@django-bridge/react";

import { useContext, useEffect } from "react";

import { Notifications as MantineNotifications, notifications } from '@mantine/notifications';

function getMessageText(message: Message) {
    if ('text' in message) {
        return message.text;
    }
    return message.html;
}

export function Notifications() {
    const { messages } = useContext(MessagesContext);

    useEffect(() => {
        messages.forEach((message, i) => {
            notifications.show({
                id: `from-django-bridge-${i}`,
                message: getMessageText(message)
              })
        })
    }, [messages]);

    return <MantineNotifications />;
}