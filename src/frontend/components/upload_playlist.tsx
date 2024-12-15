"use client";

import React, { useState } from "react";
import axios from "axios";

const UploadPlaylist = () => {
  const [playlistName, setPlaylistName] = useState<string>("");
  const [files, setFiles] = useState<{
    images: File | null;
    audios: File | null;
    mapper: File | null;
  }>({ images: null, audios: null, mapper: null });
  const [uploadProgress, setUploadProgress] = useState<number>(0);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.name === "playlistName") {
      setPlaylistName(e.target.value);
    }
    const { name, files } = e.target;
    setFiles((prevFiles) => ({ ...prevFiles, [name]: files?.[0] }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("playlistName", playlistName as string);
    formData.append("images", files.images as File);
    formData.append("audios", files.audios as File);
    formData.append("mapper", files.mapper as File);

    try {
      const response = await axios.post("/api/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total ?? 100));
          setUploadProgress(percentCompleted);
        },
      });
      console.log("Upload success:", response.data);
      setUploadProgress(0);
    } catch (error) {
      console.error("Upload error:", error);
      setUploadProgress(0);
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Upload Playlist</h2>
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <div className="flex flex-col">
          <label className="mb-2 font-semibold">Playlist Name:</label>
          <input
            type="text"
            name="playlistName"
            onChange={handleFileChange}
            value={playlistName}
            className="p-2 border rounded"
          />
        </div>
        <div className="flex flex-col">
          <label className="mb-2 font-semibold">Images Zip:</label>
          <input type="file" name="images" accept=".zip" onChange={handleFileChange} className="p-2 border rounded" />
        </div>
        <div className="flex flex-col">
          <label className="mb-2 font-semibold">Audios Zip:</label>
          <input type="file" name="audios" accept=".zip" onChange={handleFileChange} className="p-2 border rounded" />
        </div>
        <div className="flex flex-col">
          <label className="mb-2 font-semibold">Mapper JSON:</label>
          <input type="file" name="mapper" accept=".json" onChange={handleFileChange} className="p-2 border rounded" />
        </div>
        <button type="submit" className="self-end bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
          Upload
        </button>
      </form>
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
  );
};

export default UploadPlaylist;
