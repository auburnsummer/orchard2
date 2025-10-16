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

export async function djangoGet(url: string): Promise<DjangoBridgeResponse> {
  let response: Response;

  const headers: HeadersInit = { "X-Requested-With": "DjangoBridge" };

  try {
    response = await fetch(url, { headers });
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

  const headers: HeadersInit = { "X-Requested-With": "DjangoBridge" };

  try {
    response = await fetch(url, {
      method: "post",
      headers,
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
