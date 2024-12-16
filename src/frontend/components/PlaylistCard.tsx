"use client";
import Image from "next/image";
import { useRouter } from "next/navigation";
import React from "react";

export interface PlaylistType {
  name: string;
  image: string;
}

const PlaylistCard = ({ playlist }: { playlist: PlaylistType }) => {
  const router = useRouter();

  const handlePlaylistOnClick = () => {
    
  };

  return (
    <div
      onClick={handlePlaylistOnClick}
      className="card card-compact w-48 hover:bg-spotify-black-1 p-2 rounded-xl cursor-pointer">
      <figure>
        <Image
          className="hover:scale-105 duration-500 transition-all rounded-2xl w-40 h-40"
          priority
          width={300}
          height={300}
          src={playlist.image}
          alt="Shoes"
        />
      </figure>
      <h2 className="text-md mt-2">{playlist.name}</h2>
    </div>
  );
};

export default PlaylistCard;
