export const DIFFICULTY_STRINGS = ["Easy", "Medium", "Tough", "Very Tough"];

export function getRdzipDownloadUrl(level: {
  rdzip_url: string;
  song: string;
  authors: string[];
  id: string;
}): string {
  const filename = `${level.song} - ${level.authors.join(", ")} ${level.id}.rdzip`;
  return `${level.rdzip_url}?filename=${encodeURIComponent(filename)}`;
}
