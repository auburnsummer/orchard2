export function makeCanonicalURL(path: string) {
    // if path is fully qualified (ex: https://example.com)
    // this will remain as that URL
    // if path is relative, it will add window.document.baseURI to it.
    return new URL(path, window.document.baseURI);
}