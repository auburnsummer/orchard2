/// <reference types="vite/client" />


interface ImportMetaEnv {
    readonly VITE_DISCORD_APPLICATION_ID: string
    readonly VITE_API_URL: string
    // more env variables...
}
  
interface ImportMeta {
    readonly env: ImportMetaEnv
}