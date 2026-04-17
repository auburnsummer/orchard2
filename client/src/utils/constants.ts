export const DIFFICULTY_STRINGS = ["Easy", "Medium", "Tough", "Very Tough"];

export function getLevelDownloadUrl(level: { id: string }): string {
  return `${window.location.origin}/levels/${level.id}/download/`;
}
