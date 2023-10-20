import * as tg from "generic-type-guard";
import ky from "ky";

const base = ky.extend({prefixUrl: import.meta.env.VITE_API_URL, timeout: false})

type Input = Parameters<typeof ky>[0];
type KyOptions = NonNullable<Parameters<typeof ky>[1]>;

type Options<T> = KyOptions & {
    guard: tg.TypeGuard<T>
}

export const req = (method: string) => async <T>(url: Input, options: Options<T>) => {
    const { guard, ...rest } = options;
    const resp = await base(url, {
        ...rest,
        method
    });
    const data = await resp.json();
    if (guard(data)) {
        return data;
    }
    throw new Error(`Response from ${url} did not match schema ${guard.name}`);
}

export const client = {
    get: req("get"),
    post: req("post"),
    put: req("put"),
    delete: req("delete"),
    patch: req("patch"),
    options: req("options"),
    head: req("head")
}