"use client";

import React, { useState } from "react";
import PlaylistCard from "./PlaylistCard";

const playlist = {
  name: "Playlist Name",
  image:
    "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/terakhir%20banget%20tes%20ini_2024-12-16T02%3A11%3A34.066589/images/Master%20of%20Puppet_2024-12-16T02%3A11%3A35.486325.png",
};

const Playlists = () => {
  const [title, setTitle] = useState<string>("Made For You");

  return (
    <div className="w-full flex flex-col justify-center items-center text-white">
      <div className="w-2/3 text-left text-2xl font-semibold ml-10 mb-5">{title}</div>
      <div className="w-2/3 justify-center items-center flex-wrap flex gap-10">
        {Array.from({ length: 10 }).map((_, index) => (
          <PlaylistCard key={index} playlist={playlist} />
        ))}
      </div>
    </div>
  );
};

export default Playlists;
