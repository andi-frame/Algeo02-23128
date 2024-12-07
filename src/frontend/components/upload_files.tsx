"use client";
import React, { useState } from "react";
import axios from "axios";

interface UploadComponentProps {
  uploadType: "images" | "audios" | "mapper";
}

const UploadComponent: React.FC<UploadComponentProps> = ({ uploadType }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [uploadStatus, setUploadStatus] = useState<string>("");

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.name.endsWith(".zip")) {
      setSelectedFile(file);
      setUploadStatus("");
    } else {
      setSelectedFile(null);
      setUploadStatus("Please select a valid ZIP file");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("No file selected");
      return;
    }

    if (!navigator.onLine) {
      setUploadStatus("No internet connection. Please check your connection and try again.");
      return;
    }

    try {
      setUploadStatus("Uploading...");
      setUploadProgress(0);

      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("upload_type", uploadType);

      const response = await axios.post("/api/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / (progressEvent.total || 1));
          setUploadProgress(percentCompleted);
        },
      });

      setUploadStatus("Upload successful");
      console.log("Upload response:", response.data);
    } catch (error) {
      console.error("Upload error:", error);
      if (axios.isAxiosError(error) && error.response) {
        setUploadStatus(`Upload failed: ${error.response.data.message || error.message}`);
      } else {
        setUploadStatus("Upload failed. Please try again.");
      }
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <h2 className="text-xl mb-4">Upload {uploadType.charAt(0).toUpperCase() + uploadType.slice(1)} ZIP</h2>
      <input
        type="file"
        accept=".zip"
        onChange={handleFileChange}
        className="mb-4 block w-full text-sm text-slate-500
          file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-violet-50 file:text-violet-700
          hover:file:bg-violet-100"
      />
      {selectedFile && (
        <div className="mb-4">
          <p>Selected file: {selectedFile.name}</p>
        </div>
      )}
      <button
        onClick={handleUpload}
        disabled={!selectedFile}
        className="bg-blue-500 text-white py-2 px-4 rounded 
          disabled:bg-gray-300 disabled:cursor-not-allowed
          hover:bg-blue-600 transition-colors">
        Upload
      </button>
      {uploadProgress > 0 && (
        <div className="mt-4">
          <div className="bg-blue-500 h-2" style={{ width: `${uploadProgress}%` }}></div>
          <p>{uploadProgress}%</p>
        </div>
      )}
      {uploadStatus && (
        <p className={`mt-4 ${uploadStatus.includes("successful") ? "text-green-600" : "text-red-600"}`}>{uploadStatus}</p>
      )}
    </div>
  );
};

export default UploadComponent;
