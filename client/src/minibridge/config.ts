import { Context, FunctionComponent } from "react";

export interface Config {
    contextProviders: Record<string, Context<any>>;
    views: Record<string, FunctionComponent>;
}