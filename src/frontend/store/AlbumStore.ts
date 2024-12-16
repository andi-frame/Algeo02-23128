import { create } from "zustand";

export interface PlaylistType {
  name: string;
  image: string;
}

export interface TrackType {
  distance: number;
  similarity_percentage: number;
  playlist_id: string;
  track_idx: number;
  image_url: string;
  music_url: string;
  track_name: string;
}

interface TrackAlbumType {
  tracks: TrackType[] | null;
  playlists: PlaylistType[] | null;
  setTracks: (tracksData: TrackType[] | null) => void;
  setPlaylists: (playlistsData: PlaylistType[] | null) => void;
}

export const useAlbumStore = create<TrackAlbumType>((set) => ({
  tracks: null,
  playlists: null,
  setTracks: (tracksData) => {
    set({ tracks: tracksData });
  },
  setPlaylists: (playlistsData) => {
    set({ playlists: playlistsData });
  },
}));
