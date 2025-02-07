"use client";

import Playlists from "@/components/Playlists";
import Query from "@/components/query";
import Tracks from "@/components/Tracks";
import TracksHumming from "@/components/TracksHumming";
import { useAlbumStore } from "@/store/AlbumStore";
import { useState } from "react";

export default function Home() {
  const [type, setType] = useState<"playlists" | "tracks">("tracks");
  const resetOnClick = () => {
    if (type == "playlists") setType("tracks");
    if (type == "tracks") setType("playlists");
  };

  const isHumming = useAlbumStore((state) => state.isHumming);

  return (
    <div className="bg-spotify-black-1/50 flex flex-col justify-center items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <Query />
      <button className="btn-success btn text-white" onClick={resetOnClick}>
        {type == "playlists" ? "Back" : "See Playlists"}
      </button>
      {type == "playlists" && <Playlists />}
      {type == "tracks" && !isHumming && <Tracks />}
      {type == "tracks" && isHumming && <TracksHumming />}
    </div>
  );
}
