import { create } from "zustand";

export interface PlaylistType {
  id: string;
  name: string;
  img_url: string;
}

export interface TrackType {
  distance: number;
  similarity_percentage: number;
  playlist_id: string;
  playlist_name: string;
  track_idx: number;
  image_url: string;
  music_url: string;
  track_name: string;
}

export interface TrackListType {
  id: string;
  name: string;
  image_url: string;
  music_url: string;
}

interface TrackAlbumType {
  nowPlaying: TrackType | null;
  tracks: TrackType[] | null;
  playlists: PlaylistType[] | null;
  trackList: TrackListType[] | null;
  setTracks: (tracksData: TrackType[] | null) => void;
  setPlaylists: (playlistsData: PlaylistType[] | null) => void;
  setNowPlaying: (trackNow: TrackType | null) => void;
  setTrackList: (tracksData: TrackListType[] | null) => void;
}

export const useAlbumStore = create<TrackAlbumType>((set) => ({
  nowPlaying: null,
  tracks: null,
  playlists: null,
  trackList: null,
  setTracks: (tracksData) => {
    set({ tracks: tracksData });
  },
  setPlaylists: (playlistsData) => {
    set({ playlists: playlistsData });
  },
  setNowPlaying: (trackNow) => {
    set({ nowPlaying: trackNow });
  },
  setTrackList: (tracksData) => {
    set({ trackList: tracksData });
  },
}));
