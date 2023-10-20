import * as tg from "generic-type-guard";

import { client } from "./client";

export type Publisher = {
    id: string;
    name: string;
}

export const isPublisher: tg.TypeGuard<Publisher> = tg.isLikeObject({
    id: tg.isString,
    name: tg.isString
})

export async function createNewDiscordPublisher(name: string, guildToken: string) {
    return client.post("publisher/new/discord", {
        guard: isPublisher,
        headers: {
            Authorization: `Bearer ${guildToken}`
        },
        json: {
            "publisher_name": name
        }
    });
}