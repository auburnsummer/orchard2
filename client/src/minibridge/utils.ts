export function makeCanonicalURL(path: string) {
  // if path is fully qualified (ex: https://example.com)
  // this will remain as that URL
  // if path is relative, it will add window.document.baseURI to it.
  return new URL(path, window.document.baseURI);
}

export function formDataToSearchParams(formData: FormData): URLSearchParams {
  const searchParams = new URLSearchParams();
  for (const pair of formData.entries()) {
    const [key, value] = pair;
    if (typeof value === "string") {
      searchParams.set(key, value);
    } else {
      console.error(
        "A file was passed into a GET form. This has been ignored.",
      );
    }
  }
  return searchParams;
}
