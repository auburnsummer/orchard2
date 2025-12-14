import { Context, FunctionComponent, LazyExoticComponent } from "react";

export interface Config {
  contextProviders: Record<string, Context<any>>;
  views: Record<string, FunctionComponent | LazyExoticComponent<FunctionComponent<any>>>;
}
