import React from "react";
import { useAlbumStore } from "@/store/AlbumStore";
import TrackHummingCard from "./TrackHummingCard";

const TracksHumming = () => {
  const tracks = useAlbumStore((state) => state.trackHummingList);
  return (
    <div className="w-full flex flex-col justify-center items-center text-white cursor-pointer">
      <div className="w-2/3 text-left text-2xl font-semibold ml-10 mb-5">Tracks Only For You</div>
      <div className="w-2/3 justify-center items-center flex gap-5 flex-col">
        {tracks && tracks.map((track, index) => <TrackHummingCard key={index} track={track} />)}
        {!tracks && <div>Error: No Data Returned</div>}
      </div>
    </div>
  );
};

export default TracksHumming;
