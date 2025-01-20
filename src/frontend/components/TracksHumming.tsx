import React, { useState, useEffect, useMemo } from "react";
import { TrackType, useAlbumStore } from "@/store/AlbumStore";
import TrackHummingCard from "./TrackHummingCard";

const TracksHumming = () => {
  const tracks = useAlbumStore((state) => state.tracks);
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [maxPage, setMaxPage] = useState(1);
  const [paginatedTracks, setPaginatedTracks] = useState<TrackType[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredTracks = useMemo(() => {
    return tracks ? tracks.filter((track) => track.track_name.toLowerCase().includes(searchQuery.toLowerCase())) : [];
  }, [tracks, searchQuery]);

  useEffect(() => {
    if (filteredTracks && filteredTracks.length > 0) {
      const totalTracks = filteredTracks.length;
      const calculatedMaxPage = Math.ceil(totalTracks / limit);
      setMaxPage(calculatedMaxPage);

      const startIndex = (page - 1) * limit;
      const endIndex = startIndex + limit;
      const currentPageTracks = filteredTracks.slice(startIndex, endIndex);
      setPaginatedTracks(currentPageTracks);
    } else {
      setPaginatedTracks([]);
      setMaxPage(1);
    }
  }, [filteredTracks, page, limit]);

  const previousClicked = () => {
    setPage((prev) => (prev > 1 ? prev - 1 : 1));
  };

  const nextClicked = () => {
    setPage((prev) => (prev < maxPage ? prev + 1 : maxPage));
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
    setPage(1);
  };

  return (
    <div className="w-full flex flex-col justify-center items-center text-white cursor-pointer">
      <div className="w-2/3 text-left text-2xl font-semibold ml-10 mb-5">Tracks You Looking For {"(by Humming)"}</div>
      <div className="w-2/3 mb-5">
        <input
          type="text"
          placeholder="Search by track name..."
          value={searchQuery}
          onChange={handleSearchChange}
          className="w-full p-2 rounded-lg text-white ring-1 ring-spotify-green"
        />
      </div>
      <div className="w-2/3 justify-center items-center flex gap-5 flex-col">
        {paginatedTracks.length > 0 ? (
          paginatedTracks.map((track, index) => <TrackHummingCard key={index} track={track} />)
        ) : (
          <div>No tracks found. Please try another query.</div>
        )}
      </div>
      <div className="justify-around items-center w-4/5 flex mt-10">
        <button className="btn btn-success text-white text-lg w-1/8 rounded-3xl" onClick={previousClicked} disabled={page === 1}>
          {"< Previous"}
        </button>
        <p>
          Page: {page} / {maxPage}
        </p>
        <button
          className="btn btn-success text-white text-lg w-1/8 rounded-3xl"
          onClick={nextClicked}
          disabled={page === maxPage}>
          {"Next >"}
        </button>
      </div>
    </div>
  );
};

export default TracksHumming;
