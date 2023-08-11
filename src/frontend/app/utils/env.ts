import type { Environment } from "~/globals"


export const getEnv = (key: keyof Environment) => {
    return typeof window === 'undefined'
        ? process.env[key]
        : window.ENV[key]
}