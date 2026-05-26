
/**
 * If the input is a URL, extract the last path segment as the ID. Otherwise, return the input as-is.
 * @param input The input string, which can be a URL or an ID.
 * @returns The extracted ID or the original input if it's not a URL.
 */
export function extractIdFromUrlInput(input: string): string {
    try {
        const url = new URL(input.trim());
        const match = url.pathname.match(/\/([^/]+)\/?$/);
        if (match) {
            const id = match[1];
            if (id) {
                return id;
            }
        }
    } catch {
        // not a URL
    }
    return input.trim();
}