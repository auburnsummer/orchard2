import * as tg from "generic-type-guard";

export type DiscordUser = {
   id: string,
   discord_id: string,  // nb: identical to id
   username: string,
   avatar: string,
   discriminator: string,
   anyone_can_add: boolean,
   banned: boolean
}

export const isDiscordUser: tg.TypeGuard<DiscordUser> = tg.isLikeObject({
    id: tg.isString,
    discord_id: tg.isString,
    username: tg.isString,
    avatar: tg.isString,
    discriminator: tg.isString,
    anyone_can_add: tg.isBoolean,
    banned: tg.isBoolean
});

export type DiscordUserObj = {
    user: DiscordUser | null
}

export const isDiscordUserObj: tg.TypeGuard<DiscordUserObj> = tg.isLikeObject({
    user: tg.isNullable(isDiscordUser)
});