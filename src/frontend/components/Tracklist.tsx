import { useAlbumStore } from "@/store/AlbumStore";
import React from "react";
import TracklistCard from "./TracklistCard";

const Tracklist = () => {
  const trackList = useAlbumStore((state) => state.trackList);

  if (trackList)
    return (
      <div className="min-h-screen w-full flex justify-center items-center flex-col bg-spotify-black-1/50 text-white py-3">
        {trackList.map((track, index) => (
          <TracklistCard key={index} track={track} />
        ))}
      </div>
    );

  if (!trackList) return <div>No track found.</div>;
};

export default Tracklist;
