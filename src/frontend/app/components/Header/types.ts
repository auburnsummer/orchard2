import * as tg from "generic-type-guard";

export type DiscordUser = {
   id: string,
   username: string,
   avatar: string,
   discriminator: string
}

export const isDiscordUser: tg.TypeGuard<DiscordUser> = tg.isLikeObject({
    id: tg.isString,
    username: tg.isString,
    avatar: tg.isString,
    discriminator: tg.isString
});