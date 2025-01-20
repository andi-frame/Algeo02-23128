"use client";
import api from "@/api";
import { PlaylistType, useAlbumStore } from "@/store/AlbumStore";
import Image from "next/image";
import { useRouter } from "next/navigation";
import React from "react";

const PlaylistCard = ({ playlist }: { playlist: PlaylistType }) => {
  const router = useRouter();
  const setTrackList = useAlbumStore((state) => state.setTrackList);
  const setSelectedPlaylist = useAlbumStore((state) => state.setSelectedPlaylist);

  const handlePlaylistOnClick = async () => {
    setSelectedPlaylist(playlist);
    try {
      const response = await api.get(`/get-tracks-by-playlistId?playlistId=${playlist.id}`);
      if (response.data && response.data.tracks) {
        setTrackList(response.data.tracks);
        router.push("tracklist");
      }
    } catch (error) {
      console.error("Error fetching tracks:", error);
    }
  };

  return (
    <div
      onClick={handlePlaylistOnClick}
      className="card card-compact w-48 hover:bg-spotify-black-1 p-3 rounded-xl cursor-pointer">
      <figure>
        <Image
          className="hover:scale-105 duration-500 transition-all rounded-2xl w-40 h-40"
          priority
          width={300}
          height={300}
          src={playlist.img_url}
          alt="Shoes"
        />
      </figure>
      <h2 className="text-md mt-2 ml-1">{playlist.name}</h2>
    </div>
  );
};

export default PlaylistCard;
