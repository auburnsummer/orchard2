import { Cookie, CookieSerializeOptions, createCookie } from "@remix-run/node";

type TypedCookie<T>  = {
    cookie: Cookie;
    serialize: (v: T, options?: CookieSerializeOptions) => Promise<string>;
    parse: (s: string | null) => Promise<T | null>;
}

type createTypedCookieArgs<T> = {
    cookie: Cookie,
    serializeFunc: (t: T) => string,
    deserializeFunc: (s: string) => T
}

function createTypedCookie<T>({cookie, serializeFunc, deserializeFunc}: createTypedCookieArgs<T>): TypedCookie<T> {
    return {
        cookie,
        serialize: function(t: T, options?: CookieSerializeOptions) {
            const serializedValue = serializeFunc(t);
            return this.cookie.serialize(serializedValue, options)
        },
        parse: async function(s: string | null) {
            const stringValue = await this.cookie.parse(s);
            return deserializeFunc(stringValue);
        }
    }
}

function createStringCookie(cookie: Cookie): TypedCookie<string> {
    return createTypedCookie({
        cookie,
        serializeFunc: (s) => s,
        deserializeFunc: (s) => s
    })
}

export const createAuthCookie = (expires_in?: number) => createStringCookie(createCookie("discord-token", {
    maxAge: expires_in || 0,
    // ♫ i love my baby, she's the best ♫
    sameSite: /* ♫ she picks me up at ♫ */ "lax"
}));