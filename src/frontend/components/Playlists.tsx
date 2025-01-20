"use client";


import React, { useEffect, useState } from "react";
import PlaylistCard from "./PlaylistCard";
import api from "@/api";
import { useAlbumStore } from "@/store/AlbumStore";


const Playlists = () => {
  const setPlaylists = useAlbumStore((state) => state.setPlaylists);
  const playlists = useAlbumStore((state) => state.playlists);
  const [page, setPage] = useState(1);
  // const [limit, setLimit] = useState(10);
  const [maxPage, setMaxPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");


  // Pagination
  const fetchPlaylists = async (page: number) => {
    try {
      const response = await api.get("/get-playlists-paginated", {
        params: {
          page: page,
          limit: 12,
        },
      });
      if (response.data && response.data.playlists) {
        setPlaylists(response.data.playlists);
        setMaxPage(response.data.maxPage);
      }
    } catch (error) {
      console.error("Error fetching playlists:", error);
    }
  };


  useEffect(() => {
    fetchPlaylists(page);
  }, [page]);


  const previousClicked = async () => {
    setPage((prev) => (prev > 1 ? prev - 1 : 1));
  };


  const nextClicked = async () => {
    setPage((prev) => (prev < maxPage ? prev + 1 : maxPage));
  };


  // Search Playlist
  const handleSearch = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();


    try {
      const response = await api.get("search-playlists", {
        params: {
          playlist_name: searchQuery,
        },
      });


      if (response.data && response.data.playlists) {
        setPlaylists(response.data.playlists);
      } else {
        setPlaylists([]);
      }
    } catch (error) {
      console.error("Error searching playlists:", error);
      setPlaylists([]);
    }
  };


  return (
    <div className="w-full flex flex-col justify-center items-center text-white">
      <div className="w-2/3 text-left text-2xl font-semibold ml-10 mb-5">{"Made For You"}</div>
      <form className="flex justify-center items-center gap-5 mb-4" onSubmit={handleSearch}>
        <input
          className="rounded-full ring-1 ring-spotify-green px-3 py-[3px]"
          type="text"
          placeholder="Playlist Name"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="btn btn-success btn-sm flex items-center text-white text-lg w-1/8 rounded-3xl">
          Search
        </button>
      </form>
      <div className="w-2/3 justify-center items-center flex-wrap flex gap-10">
        {!playlists && <div>No Playlist Available.</div>}
        {playlists && playlists.map((playlist, index) => <PlaylistCard key={index} playlist={playlist} />)}
      </div>
      <div className="justify-around items-center w-4/5 flex mt-10">
        <button className="btn btn-success text-white text-lg w-1/8 rounded-3xl" onClick={previousClicked}>
          {"< Previous"}
        </button>
        <p>
          Page: {page} / {maxPage}
        </p>
        <button className="btn btn-success text-white text-lg w-1/8 rounded-3xl" onClick={nextClicked}>
          {"Next >"}
        </button>
      </div>
    </div>
  );
};


export default Playlists;
