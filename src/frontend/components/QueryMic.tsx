import React from "react";
import { Card, CardContent } from "./ui/card";

const QueryMic = () => {
  return (
    <Card className="h-[400px] flex justify-center items-center flex-col bg-spotify-black-2 text-white">
      <CardContent className="flex flex-col gap-5 aspect-square items-center justify-center p-6">
        <div className="text-3xl text-semibold">Query By Mic</div>
        <form className="flex flex-col justify-center items-center gap-5">
          <div className="flex flex-col items-start justify-center gap-1">
            <label className="rounded-full ring-1 ring-spotify-green px-2 py-1">Masukkan Suara Anda:</label>{" "}
            <input
              className="file-input file-input-success file-input-bordered bg-white text-spotify-black-2"
              type="file"
              accept=".png"
            />
          </div>
          <button type="submit" className="btn w-1/2 btn-success text-white text-lg">
            Upload
          </button>
        </form>
      </CardContent>
    </Card>
  );
};

export default QueryMic;
