export function removeDuplicates<T>(array: T[]): T[] {
  const seen = new Set();
  return array.filter((item) => {
    if (seen.has(item)) {
      return false;
    } else {
      seen.add(item);
      return true;
    }
  });
}
