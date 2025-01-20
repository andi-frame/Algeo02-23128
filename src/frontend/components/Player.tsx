"use client";

import React, { useState, useRef, useEffect } from "react";
import { Play, Pause, Repeat, Shuffle, SkipBack, SkipForward } from "lucide-react";
import Image from "next/image";
import { useAlbumStore } from "@/store/AlbumStore";
import * as Tone from "tone";
import MidiPlayer from "midi-player-js";

// Helper function to convert ticks to seconds
function ticksToSeconds(ticks: number): number {
  return (ticks / 480) * (60 / 120); // Default PPQ = 480, BPM = 120
}

// Helper function to convert seconds to ticks
function secondsToTicks(seconds: number): number {
  return seconds * 480 * (120 / 60); // Default PPQ = 480, BPM = 120
}

const Player = () => {
  const nowPlaying = useAlbumStore((state) => state.nowPlaying);

  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const audioRef = useRef<HTMLAudioElement>(null);
  const midiPlayerRef = useRef<MidiPlayer.Player | null>(null); // Ref for midi-player-js

  useEffect(() => {
    if (nowPlaying?.music_url && nowPlaying.music_url.endsWith(".mid")) {
      // Initialize Tone.js
      Tone.start().then(async () => {
        console.log("Tone.js initialized");

        // Ensure the URL starts with https://storage.googleapis.com/
        const midiUrl = nowPlaying.music_url.startsWith("https://storage.googleapis.com/")
          ? nowPlaying.music_url
          : `https://storage.googleapis.com/${nowPlaying.music_url}`;

        console.log("MIDI URL:", midiUrl);

        try {
          // Fetch the MIDI file as an ArrayBuffer
          const response = await fetch(midiUrl);
          if (!response.ok) {
            throw new Error(`Failed to fetch MIDI file: ${response.statusText}`);
          }

          const arrayBuffer = await response.arrayBuffer();
          console.log("Fetched ArrayBuffer:", arrayBuffer);

          // Initialize the MIDI player
          const midiPlayer = new MidiPlayer.Player((event) => {
            console.log(event); // Log MIDI events
            if (event.name === "Note on" && event.velocity > 0) {
              const synth = new Tone.Synth().toDestination();
              synth.triggerAttackRelease(Tone.Frequency(event.noteNumber, "midi").toNote(), "8n");
            }
          });

          // Load the MIDI file
          midiPlayer.loadArrayBuffer(arrayBuffer);
          midiPlayerRef.current = midiPlayer;

          // Set duration based on the MIDI file
          const totalTicks = midiPlayer.getTotalTicks();
          const totalDuration = ticksToSeconds(totalTicks);
          setDuration(totalDuration);

          console.log("MIDI file loaded. Total duration:", totalDuration);
        } catch (error) {
          console.error("Error fetching or parsing MIDI file:", error);
        }
      });
    }
  }, [nowPlaying]);

  // Handle play/pause for MIDI and audio files
  const togglePlayPause = async () => {
    if (nowPlaying?.music_url.endsWith(".mid")) {
      if (midiPlayerRef.current) {
        if (isPlaying) {
          midiPlayerRef.current.stop();
        } else {
          midiPlayerRef.current.play();
        }
        setIsPlaying(!isPlaying);
      }
    } else {
      const audio = audioRef.current;
      if (audio) {
        if (isPlaying) {
          audio.pause();
        } else {
          audio.play();
        }
        setIsPlaying(!isPlaying);
      }
    }
  };

  // Skip to the end of the track
  const skipToNext = () => {
    if (nowPlaying?.music_url.endsWith(".mid")) {
      if (midiPlayerRef.current) {
        midiPlayerRef.current.stop();
        setIsPlaying(false);
      }
    } else {
      const audio = audioRef.current;
      if (audio) {
        audio.currentTime = duration;
        setCurrentTime(duration);
      }
    }
  };

  // Skip to the beginning of the track
  const skipToPrevious = () => {
    if (nowPlaying?.music_url.endsWith(".mid")) {
      if (midiPlayerRef.current) {
        midiPlayerRef.current.stop();
        midiPlayerRef.current.play();
        setIsPlaying(true);
      }
    } else {
      const audio = audioRef.current;
      if (audio) {
        audio.currentTime = 0;
        setCurrentTime(0);
      }
    }
  };

  // Format time for display
  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

  // Handle progress bar click
  const handleProgressClick = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    if (nowPlaying?.music_url.endsWith(".mid")) {
      if (midiPlayerRef.current) {
        const rect = e.currentTarget.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const newTime = (clickX / rect.width) * duration;
        const newTicks = secondsToTicks(newTime);
        midiPlayerRef.current.skipToTick(newTicks);
        setCurrentTime(newTime);
      }
    } else {
      const audio = audioRef.current;
      if (audio && duration) {
        const rect = e.currentTarget.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const newTime = (clickX / rect.width) * duration;
        audio.currentTime = newTime;
        setCurrentTime(newTime);
      }
    }
  };

  // Update current time for MIDI playback
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (nowPlaying?.music_url.endsWith(".mid") && isPlaying) {
      interval = setInterval(() => {
        if (midiPlayerRef.current) {
          const currentTicks = midiPlayerRef.current.getCurrentTick();
          const currentTime = ticksToSeconds(currentTicks);
          setCurrentTime(currentTime);
        }
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isPlaying, duration, nowPlaying]);

  if (!nowPlaying) return null;

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
          <p>{formatTime(duration)}</p> {/* Display duration here */}
        </div>
      </div>
      <div className="flex items-center justify-center gap-2 opacity-75 cursor-default w-1/5">Hear Me Out</div>
      {!nowPlaying.music_url.endsWith(".mid") && (
        <audio ref={audioRef} src={nowPlaying.music_url} preload="metadata" autoPlay={isPlaying} />
      )}
    </div>
  );
};

export default Player;
