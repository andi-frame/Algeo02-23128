import React from "react";
import Image from "next/image";
import { TrackHumming } from "@/store/AlbumStore";

const TrackHummingCard = ({ track }: { track: TrackHumming }) => {
  // const setNowPlaying = useAlbumStore((state) => state.setNowPlaying);

  const handleTrackOnClick = () => {
    // setNowPlaying(null);
    // setNowPlaying(track);
  };

  return (
    <div
      onClick={handleTrackOnClick}
      className="w-full card card-compact hover:bg-spotify-black-1 p-2 rounded-xl cursor-pointer flex flex-row">
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
        <div>Similarity: {track.similarity * 100}%</div>
      </div>
    </div>
  );
};

export default TrackHummingCard;
