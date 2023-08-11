import * as tg from "generic-type-guard";

export type User = {
    id: string
    name: string
    avatar_url: string
    // we don't care about cutoff here.
}

export const isUser: tg.TypeGuard<User> = tg.isLikeObject({
    id: tg.isString,
    name: tg.isString,
    avatar_url: tg.isString
});

export type UserObject = {
    user: User | null
}

export const isUserObject: tg.TypeGuard<UserObject> = tg.isLikeObject({
    user: tg.isNullable(isUser)
});