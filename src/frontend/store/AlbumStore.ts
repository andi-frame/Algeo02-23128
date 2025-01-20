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

export interface TrackHumming {
  id: string;
  name: string;
  similarity: number;
  music_url: string;
  image_url: string;
}

interface TrackAlbumType {
  isHumming: boolean | null;
  nowPlaying: TrackType | null;
  tracks: TrackType[] | null;
  playlists: PlaylistType[] | null;
  trackList: TrackListType[] | null;
  trackHummingList: TrackHumming[] | null;
  selectedPlaylist: PlaylistType | null;
  setTracks: (tracksData: TrackType[] | null) => void;
  setPlaylists: (playlistsData: PlaylistType[] | null) => void;
  setNowPlaying: (trackNow: TrackType | null) => void;
  setTrackList: (tracksData: TrackListType[] | null) => void;
  setIsHumming: (isHummingData: boolean | null) => void;
  setTrackHummingList: (trackHummingData: TrackHumming[] | null) => void;
  setSelectedPlaylist: (selectedPlaylist: PlaylistType | null) => void;
}

export const useAlbumStore = create<TrackAlbumType>((set) => ({
  nowPlaying: null,
  tracks: null,
  playlists: null,
  trackList: null,
  isHumming: null,
  trackHummingList: null,
  selectedPlaylist: null,
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
  setIsHumming: (isHummingData) => {
    set({ isHumming: isHummingData });
  },
  setTrackHummingList: (trackHummingData) => {
    set({ trackHummingList: trackHummingData });
  },
  setSelectedPlaylist: (selectedPlaylist) => {
    set({ selectedPlaylist: selectedPlaylist });
  },
}));
