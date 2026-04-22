import { Metadata } from "./metadata";

export type MessageLevel = "info" | "success" | "warning" | "error";

export interface Message {
  level: MessageLevel;
  html: string;
}

interface ReloadResponse {
  action: "reload";
}

interface RedirectResponse {
  action: "redirect";
  path: string;
}

export interface RenderResponse {
  action: "render";
  overlay: boolean;
  metadata: Metadata;
  view: string;
  props: Record<string, unknown>;
  context: Record<string, unknown>;
  messages: Message[];
}

interface ServerErrorResponse {
  action: "server-error";
}

interface NetworkErrorResponse {
  action: "network-error";
}

export type DjangoBridgeResponse =
  | ReloadResponse
  | RedirectResponse
  | RenderResponse
  | ServerErrorResponse
  | NetworkErrorResponse;

/**
 * The server will respond with JSON if you give it _bridge=1, otherwise with HTML
 */
function bridgeUrl(url: string): string {
  const u = new URL(url, window.location.origin);
  u.searchParams.set("_bridge", "1");
  return u.pathname + u.search + u.hash;
}

export async function djangoGet(url: string): Promise<DjangoBridgeResponse> {
  let response: Response;

  try {
    response = await fetch(bridgeUrl(url));
  } catch (e) {
    return {
      action: "network-error",
    };
  }

  if (response.status === 500) {
    return {
      action: "server-error",
    };
  }
  // e.g. 404, where it returns normal HTML
  if (!response.headers.get("X-DjangoBridge-Action")) {
    return {
      action: "reload",
    };
  }
  return response.json() as Promise<DjangoBridgeResponse>;
}

export async function djangoPost(
  url: string,
  data: FormData,
): Promise<DjangoBridgeResponse> {
  let response: Response;

  try {
    response = await fetch(bridgeUrl(url), {
      method: "post",
      body: data,
    });
  } catch (e) {
    return {
      action: "network-error",
    };
  }

  if (response.status === 500) {
    return {
      action: "server-error",
    };
  }
  // e.g. 404, where it returns normal HTML
  if (!response.headers.get("X-DjangoBridge-Action")) {
    return {
      action: "reload",
    };
  }
  return response.json() as Promise<DjangoBridgeResponse>;
}
