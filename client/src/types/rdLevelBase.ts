import { Club } from "./club";
import { UserPublic } from "./user";

// output of the prefill job if update
export type RDLevelUpdatePrefillData = {
  sha1: string;
  rdlevel_sha1: string;
  is_animated: boolean;
  last_updated: string;
  artist_raw: string;
  song_raw: string;
  authors_raw: string;
  rd_md5: string;
  rdzip_url: string;
  image_url: string;
  icon_url: string | null;
  thumb_url: string;
};

// output of the prefill job
export type RDLevelBase = RDLevelUpdatePrefillData & {
  artist: string;
  artist_tokens: string[];
  song: string;
  seizure_warning: boolean;
  description: string;
  hue: number;
  authors: string[];
  max_bpm: number;
  min_bpm: number;
  difficulty: number;
  single_player: boolean;
  two_player: boolean;
  tags: string[];
};

// some additional fields
export type RDLevel = RDLevelBase & {
  id: string;
  song_alt: string;
  submitter: UserPublic;
  club: Club;
  // 10 = peer-reviewed, 0 = pending, -1 = non-refereed
  // other numbers are unused. I had some idea about 0-9 being different kinds
  // of pending a la http status codes
  // like you could mark a level as "pending minor changes" or "i want a second opinion"
  approval: number;
};
