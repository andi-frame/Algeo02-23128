"use client";

import React, { useState } from "react";
import axios from "axios";

const UploadPlaylist = () => {
  const [files, setFiles] = useState<{
    playlistName: string | null;
    images: File | null;
    audios: File | null;
    mapper: File | null;
  }>({ playlistName: null, images: null, audios: null, mapper: null });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, files } = e.target;
    setFiles((prevFiles) => ({ ...prevFiles, [name]: files?.[0] }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("playlistName", files.playlistName as string);
    formData.append("images", files.images as File);
    formData.append("audios", files.audios as File);
    formData.append("mapper", files.mapper as File);

    try {
      const response = await axios.post("/api/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Upload success:", response.data);
    } catch (error) {
      console.error("Upload error:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Playlist Name:</label>
        <input type="text" name="playlistName" />
      </div>
      <div>
        <label>Images Zip:</label>
        <input type="file" name="images" accept=".zip" onChange={handleFileChange} />
      </div>
      <div>
        <label>Audios Zip:</label>
        <input type="file" name="audios" accept=".zip" onChange={handleFileChange} />
      </div>
      <div>
        <label>Mapper JSON:</label>
        <input type="file" name="mapper" accept=".json" onChange={handleFileChange} />
      </div>
      <button type="submit">Upload</button>
    </form>
  );
};

export default UploadPlaylist;
