"use client";

import React, { useState, useRef, useEffect } from "react";
import { Play, Pause, Repeat, Shuffle, SkipBack, SkipForward } from "lucide-react";
import Image from "next/image";
import { useAlbumStore } from "@/store/AlbumStore";

const Player = () => {
  const nowPlaying = useAlbumStore((state) => state.nowPlaying);

  const [isPlaying, setIsPlaying] = useState(true);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    const audio = audioRef.current;

    const updateTime = () => setCurrentTime(audio?.currentTime || 0);
    const updateDuration = () => setDuration(audio?.duration || 0);

    if (audio) {
      audio.addEventListener("timeupdate", updateTime);
      audio.addEventListener("loadedmetadata", updateDuration);

      // Load the metadata to update the duration
      if (audio.readyState >= 1) {
        updateDuration();
      }

      return () => {
        audio.removeEventListener("timeupdate", updateTime);
        audio.removeEventListener("loadedmetadata", updateDuration);
      };
    }
  }, [audioRef.current]);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (audio) {
      if (isPlaying) {
        audio.pause();
      } else {
        audio.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const skipToNext = () => {
    const audio = audioRef.current;
    if (audio) {
      audio.currentTime = duration;
      setCurrentTime(duration);
    }
  };

  const skipToPrevious = () => {
    const audio = audioRef.current;
    if (audio) {
      setIsPlaying(false);
      audio.currentTime = 0;
      setCurrentTime(0);
    }
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

  const handleProgressClick = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    const audio = audioRef.current;
    if (audio && duration) {
      const rect = e.currentTarget.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const newTime = (clickX / rect.width) * duration;
      audio.currentTime = newTime;
      setCurrentTime(newTime);
    }
  };

  if (nowPlaying)
    return (
      <div className="h-28 bg-spotify-black-2 w-full flex justify-between items-center sticky bottom-0 text-white px-10 z-50 shadow-xl">
        <div className="h-full flex gap-4 justify-center items-center w-1/5">
          <div className="relative w-16 h-16">
            <Image className="object-contain" src={nowPlaying.image_url} layout="fill" alt={"Track Image"} />
          </div>
          <div>
            <div>{nowPlaying.track_name}</div>
            <div>{nowPlaying.playlist_name}</div>
          </div>
        </div>
        <div className="flex flex-col items-center gap-1 m-auto">
          <div className="flex gap-4">
            <Shuffle className="w-8 cursor-pointer" />
            <SkipBack className="w-8 cursor-pointer" onClick={skipToPrevious} />
            {isPlaying ? (
              <Pause className="w-8 cursor-pointer" onClick={togglePlayPause} />
            ) : (
              <Play className="w-8 cursor-pointer" onClick={togglePlayPause} />
            )}
            <SkipForward className="w-8 cursor-pointer" onClick={skipToNext} />
            <Repeat className="w-8 cursor-pointer" />
          </div>
          <div className="flex items-center gap-5">
            <p>{formatTime(currentTime)}</p>
            <div className="w-[60vh] max-w-[500px] bg-gray-300 rounded-full cursor-pointer" onClick={handleProgressClick}>
              <div className="h-1 bg-spotify-green rounded-full" style={{ width: `${(currentTime / duration) * 100}%` }}></div>
            </div>
            <p>{formatTime(duration)}</p>
          </div>
        </div>
        <div className="flex items-center justify-center gap-2 opacity-75 cursor-default w-1/5">Hear Me Out</div>
        <audio ref={audioRef} src={nowPlaying.music_url} preload="metadata" autoPlay />
      </div>
    );
};

export default Player;
