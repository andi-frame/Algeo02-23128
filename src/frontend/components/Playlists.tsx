"use client";

import React, { useEffect } from "react";
import PlaylistCard from "./PlaylistCard";
import api from "@/api";
import { useAlbumStore } from "@/store/AlbumStore";

// const playlist = {
//   id: "1",
//   name: "Playlist Name",
//   image:
//     "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Solo_2024-12-16T13%3A41%3A36.560786.png",
// };

const Playlists = () => {
  const setPlaylists = useAlbumStore((state) => state.setPlaylists);
  const playlists = useAlbumStore((state) => state.playlists);

  useEffect(() => {
    const fetchPlaylists = async () => {
      try {
        const response = await api.get("/get-all-playlist");
        if (response.data && response.data.playlists) {
          setPlaylists(response.data.playlists);
        }
      } catch (error) {
        console.error("Error fetching playlists:", error);
      }
    };

    if (!playlists) {
      fetchPlaylists();
    }
  }, []);

  return (
    <div className="w-full flex flex-col justify-center items-center text-white">
      <div className="w-2/3 text-left text-2xl font-semibold ml-10 mb-5">{"Made For You"}</div>
      <div className="w-2/3 justify-center items-center flex-wrap flex gap-10">
        {!playlists && <div>No Playlist Available.</div>}
        {playlists && playlists.map((playlist, index) => <PlaylistCard key={index} playlist={playlist} />)}
      </div>
    </div>
  );
};

export default Playlists;
