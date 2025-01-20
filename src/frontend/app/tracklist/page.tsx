"use client";
import Tracklist from "@/components/Tracklist";
import { useAlbumStore } from "@/store/AlbumStore";
import React from "react";
import Image from "next/image";

const Page = () => {
  const selectedPlaylist = useAlbumStore((state) => state.selectedPlaylist);

  if (!selectedPlaylist) {
    return (
      <div className="flex justify-center items-center w-full h-screen bg-spotify-black-1">Error: Playlist Not Selected!</div>
    );
  }

  return (
    <div className="min-h-screen bg-spotify-black-1">
      <div className="flex justify-center items-center gap-10 py-5 pt-10 text-white">
        <Image
          className="hover:scale-105 duration-500 transition-all rounded-2xl w-40 h-40"
          priority
          width={300}
          height={300}
          src={selectedPlaylist.img_url}
          alt="Shoes"
        />
        <div className="flex flex-col gap-2">
          <div className="text-4xl font-bold">Playlist</div>
          <div className="text-4xl font-bold">{selectedPlaylist.name}</div>
        </div>
      </div>
      <Tracklist />
    </div>
  );
};

export default Page;
