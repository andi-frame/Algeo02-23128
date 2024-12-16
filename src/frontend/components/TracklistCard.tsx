"use client";

import { TrackListType, TrackType, useAlbumStore } from "@/store/AlbumStore";
import React from "react";
import Image from "next/image";

const TracklistCard = ({ track }: { track: TrackListType }) => {
  const setNowPlaying = useAlbumStore((state) => state.setNowPlaying);
  const trackToPlay: TrackType = {
    distance: 0,
    similarity_percentage: 0,
    playlist_id: "",
    playlist_name: "",
    track_idx: 0,
    track_name: track.name,
    image_url: track.image_url,
    music_url: track.music_url,
  };

  const handleTrackOnClick = () => {
    setNowPlaying(null);
    setNowPlaying(trackToPlay);
  };

  return (
    <div
      onClick={handleTrackOnClick}
      className="w-2/3 card card-compact hover:bg-spotify-black-1 p-2 rounded-xl cursor-pointer flex flex-row">
      <figure>
        <Image
          className="hover:scale-105 duration-500 transition-all rounded-2xl w-40 h-40"
          priority
          width={300}
          height={300}
          src={track.image_url}
          alt="track_image"
        />
      </figure>
      <div className="mx-5">
        <div className="text-xl font-semibold mb-5">{track.name}</div>
        <div>{track.name}</div>
      </div>
    </div>
  );
};

export default TracklistCard;
