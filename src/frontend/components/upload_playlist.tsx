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
  const [errorMessage, setErrorMessage] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.name === "playlistName") {
      setPlaylistName(e.target.value);
    }
    const { name, files } = e.target;
    setFiles((prevFiles) => ({ ...prevFiles, [name]: files?.[0] }));
  };

  const validateForm = (): boolean => {
    if (!playlistName) {
      setErrorMessage("Playlist name is required.");
      return false;
    }
    if (!files.images || !files.audios || !files.mapper) {
      setErrorMessage("All files (images, audios, and mapper) are required.");
      return false;
    }
    if (files.images && files.images.name.split(".").pop() !== "zip") {
      setErrorMessage("Images file must be a zip file.");
      return false;
    }
    if (files.audios && files.audios.name.split(".").pop() !== "zip") {
      setErrorMessage("Audios file must be a zip file.");
      return false;
    }
    if (files.mapper && files.mapper.name.split(".").pop() !== "json") {
      setErrorMessage("Mapper file must be a JSON file.");
      return false;
    }
    setErrorMessage("");
    return true;
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!validateForm()) return;

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
    <div className="max-w-lg mx-auto p-6 bg-spotify-black-2 text-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Upload Playlist</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <div className="flex flex-col">
          <div className="flex flex-col rounded-xl p-3 ring-1 ring-spotify-green pt-2">
            <label className="mb-2">Playlist Name:</label>
            <input
              type="text"
              name="playlistName"
              onChange={handleFileChange}
              value={playlistName}
              className="p-2 border rounded-full px-4"
            />
          </div>
        </div>
        <div className="flex flex-col">
          <div className="flex flex-col rounded-xl p-3 ring-1 ring-spotify-green pt-2">
            <label className="mb-2">Images Zip:</label>
            <input
              type="file"
              name="images"
              accept=".zip"
              onChange={handleFileChange}
              className="file-input file-input-success file-input-bordered bg-white text-spotify-black-2"
            />
          </div>
        </div>
        <div className="flex flex-col">
          <div className="flex flex-col rounded-xl p-3 ring-1 ring-spotify-green pt-2">
            <label className="mb-2">Audios Zip:</label>
            <input
              type="file"
              name="audios"
              accept=".zip"
              onChange={handleFileChange}
              className="file-input file-input-success file-input-bordered bg-white text-spotify-black-2"
            />
          </div>
        </div>
        <div className="flex flex-col">
          <div className="flex flex-col rounded-xl p-3 ring-1 ring-spotify-green pt-2">
            <label className="mb-2">Mapper JSON:</label>
            <input
              type="file"
              name="mapper"
              accept=".json"
              onChange={handleFileChange}
              className="file-input file-input-success file-input-bordered bg-white text-spotify-black-2"
            />
          </div>
        </div>
        {errorMessage && <div className="text-red-500 text-sm mt-2">{errorMessage}</div>}
        <button type="submit" className="btn btn-success">
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
