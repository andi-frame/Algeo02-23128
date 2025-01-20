"use client";

import React, { useState } from "react";
import { Card, CardContent } from "./ui/card";
import api from "@/api";
import { useAlbumStore } from "@/store/AlbumStore";

const QueryHumming = () => {
  const [top, setTop] = useState<number>(0);
  const [midi, setMidi] = useState<File | null>(null);
  const [responseTime, setResponseTime] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const setTracks = useAlbumStore((state) => state.setTracks); // Use the same setTracks function
  const setIsHumming = useAlbumStore((state) => state.setIsHumming);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.name === "top" && e.target.value) {
      setTop(Number(e.target.value));
    }
    if (e.target.name === "midi" && e.target.files) setMidi(e.target.files[0]);
  };

  const handleOnSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setErrorMessage(null);

    if (!midi) {
      setErrorMessage("Please select a MIDI file.");
      return;
    }

    if (top <= 0) {
      setErrorMessage("Please enter a positive number.");
      return;
    }

    const formData = new FormData();
    formData.append("top_k", String(top));
    formData.append("query_midi", midi as File);

    const startTime = Date.now();

    try {
      const response = await api.post("/query-by-humming", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total ?? 100));
          setUploadProgress(percentCompleted);
        },
      });

      const endTime = Date.now();
      const duration = endTime - startTime;

      setResponseTime(duration);
      setTracks(response.data["top_tracks"]);
      setIsHumming(true);

      console.log("Upload success:", response.data);
      setUploadProgress(0);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadProgress(0);
    }
  };

  return (
    <Card className="h-[400px] flex justify-center items-center flex-col bg-spotify-black-2 text-white">
      <CardContent className="flex flex-col gap-5 aspect-square items-center justify-center p-6">
        <div className="text-3xl text-semibold">Query By Humming</div>
        <form onSubmit={handleOnSubmit} className="flex flex-col justify-center items-center gap-5">
          <div className="flex flex-col items-start justify-center gap-1">
            <label className="rounded-full ring-1 ring-spotify-green px-2 py-1">Masukkan Suara:</label>{" "}
            <input
              className="file-input file-input-success file-input-bordered bg-white text-spotify-black-2"
              type="file"
              accept=".mid"
              name="midi"
              onChange={handleChange}
            />
          </div>
          <div className="flex justify-center items-center mt-5 gap-3">
            <label className="rounded-full ring-1 ring-spotify-green px-2 py-1">Masukkan Jumlah:</label>{" "}
            <input
              className="py-1 w-20 rounded-xl px-2 text-center bg-white text-spotify-black-2"
              type="number"
              name="top"
              onChange={handleChange}
            />
          </div>
          <div>
            {uploadProgress > 0 && (
              <div className="w-full bg-gray-200 rounded-full mt-4">
                <div
                  className="bg-blue-500 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full"
                  style={{ width: `${uploadProgress}%` }}>
                  {uploadProgress}%
                </div>
              </div>
            )}
            {errorMessage && <div className="text-red-500 mt-3 text-sm">{errorMessage}</div>}
            {responseTime !== null && <div className="mt-3 text-green-500 text-sm">Response Time: {responseTime} ms</div>}
          </div>
          <button type="submit" className="btn w-1/2 btn-success text-white text-lg">
            Upload
          </button>
        </form>
      </CardContent>
    </Card>
  );
};

export default QueryHumming;
