import React from "react";
import TrackCard from "./TrackCard";
import { useAlbumStore } from "@/store/AlbumStore";

const Tracks = () => {
  const tracks = useAlbumStore((state) => state.tracks);
  return (
    <div className="w-full flex flex-col justify-center items-center text-white cursor-pointer">
      <div className="w-2/3 text-left text-2xl font-semibold ml-10 mb-5">Tracks You Looking For {"(by Image)"}</div>
      <div className="w-2/3 justify-center items-center flex gap-5 flex-col">
        {tracks && tracks.map((track, index) => <TrackCard key={index} track={track} />)}
        {!tracks && <div>Error: No Data Returned</div>}
      </div>
    </div>
  );
};

export default Tracks;
