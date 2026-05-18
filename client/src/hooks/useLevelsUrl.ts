import { useUser } from "./useUser";

/**
 * Build a /levels URL respecting default PR preference.
 * If the URL already has a PR param, keep it (i.e. they explicitly changed the setting in search)
 */
export function useLevelsUrl() {
  const { default_pr_preference } = useUser();

  return (params: Record<string, string> = {}): string => {
    const sp = new URLSearchParams(params);
    if (!sp.has("peer_review") && default_pr_preference !== "approved") {
      sp.set("peer_review", default_pr_preference);
    }
    const qs = sp.toString();
    return qs ? `/levels/?${qs}` : "/levels/";
  };
}
