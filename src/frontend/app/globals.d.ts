
export type Environment = {
    SITE_URL: string
    DISCORD_LOGIN_APPLICATION_ID: string
    API_URL: string
}

declare global {
    interface Window {
        ENV: Environment
    }
    
}