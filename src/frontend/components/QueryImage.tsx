"use client";

import React, { useState } from "react";
import { Card, CardContent } from "./ui/card";
import api from "@/api";
import { useAlbumStore } from "@/store/AlbumStore";

const QueryImage = () => {
  const [top, setTop] = useState<number>(0);
  const [image, setImage] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const setTracks = useAlbumStore((state) => state.setTracks);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.name === "top" && e.target.value) {
      setTop(Number(e.target.value));
    }
    if (e.target.name === "image" && e.target.files) setImage(e.target.files[0]);
  };

  const handleOnSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("top_k", String(top));
    formData.append("query_image", image as File);

    try {
      const response = await api.post("/query-by-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total ?? 100));
          setUploadProgress(percentCompleted);
        },
      });

      setTracks(response.data["top_tracks"]);

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
        <div className="text-3xl text-semibold">Query By Image</div>
        <form onSubmit={handleOnSubmit} className="flex flex-col justify-center items-center gap-5">
          <div className="flex flex-col items-start justify-center gap-1">
            <label className="rounded-full ring-1 ring-spotify-green px-2 py-1">Masukkan gambar:</label>{" "}
            <input
              className="file-input file-input-success file-input-bordered bg-white text-spotify-black-2"
              type="file"
              accept=".png"
              name="image"
              onChange={handleChange}
            />
            <div className="flex justify-center items-center mt-5 gap-3">
              <label className="rounded-full ring-1 ring-spotify-green px-2 py-1">Masukkan Jumlah:</label>{" "}
              <input
                className="py-1 w-20 rounded-xl px-2 text-center bg-white text-spotify-black-2"
                type="number"
                name="top"
                onChange={handleChange}
              />
            </div>
            {uploadProgress > 0 && (
              <div className="w-full bg-gray-200 rounded-full mt-4">
                <div
                  className="bg-blue-500 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full"
                  style={{ width: `${uploadProgress}%` }}>
                  {uploadProgress}%
                </div>
              </div>
            )}
          </div>
          <button type="submit" className="btn w-1/2 btn-success text-white text-lg">
            Upload
          </button>
        </form>
      </CardContent>
    </Card>
  );
};

export default QueryImage;
