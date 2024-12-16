import React from "react";
import TrackCard from "./TrackCard";
import { useAlbumStore } from "@/store/AlbumStore";

const Tracks = () => {
  const tracks = useAlbumStore((state) => state.tracks);

  return (
    <div className="w-full flex flex-col justify-center items-center text-white">
      <div className="w-2/3 text-left text-2xl font-semibold ml-10 mb-5">Tracks Only For You</div>
      <div className="w-2/3 justify-center items-center flex gap-5 flex-col">
        {tracks && tracks.map((track, index) => <TrackCard key={index} track={track} />)}
        {!tracks && <div>Error: No Data Returned</div>}
      </div>
    </div>
  );
};

export default Tracks;

// const DefaultTracks = [
//   {
//     distance: 0.00019789301690862582,
//     similarity_percentage: 100,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 7,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Dancing_2024-12-16T13%3A42%3A05.240715.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/Dancing_2024-12-16T13%3A42%3A07.334911.wav",
//     track_name: "Dancing",
//   },
//   {
//     distance: 228.40172537305656,
//     similarity_percentage: 86.51,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 3,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Bad_2024-12-16T13%3A41%3A43.589111.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/Bad_2024-12-16T13%3A41%3A46.238193.wav",
//     track_name: "Bad",
//   },
//   {
//     distance: 389.4583754290122,
//     similarity_percentage: 77,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 4,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Thrift%20Shop_2024-12-16T13%3A41%3A49.224552.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/Thrift%20Shop_2024-12-16T13%3A41%3A51.504098.wav",
//     track_name: "Thrift Shop",
//   },
//   {
//     distance: 564.71279258037,
//     similarity_percentage: 66.65,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 8,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Locked%20Away_2024-12-16T13%3A42%3A10.241145.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/Locked%20Away_2024-12-16T13%3A42%3A12.041477.wav",
//     track_name: "Locked Away",
//   },
//   {
//     distance: 1028.8374170755146,
//     similarity_percentage: 39.23,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 1,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Take%20Away_2024-12-16T13%3A41%3A28.976295.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/Take%20Away_2024-12-16T13%3A41%3A32.017400.wav",
//     track_name: "Take Away",
//   },
//   {
//     distance: 1098.8616366666179,
//     similarity_percentage: 35.1,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 0,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Master%20of%20Puppet_2024-12-16T13%3A41%3A21.854716.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/Master%20of%20Puppet_2024-12-16T13%3A41%3A25.605323.wav",
//     track_name: "Master of Puppet",
//   },
//   {
//     distance: 1350.8767570368987,
//     similarity_percentage: 20.21,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 9,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/SkyFall_2024-12-16T13%3A42%3A14.901718.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/SkyFall_2024-12-16T13%3A42%3A16.951552.wav",
//     track_name: "SkyFall",
//   },
//   {
//     distance: 1362.473283151196,
//     similarity_percentage: 19.53,
//     playlist_id: "65e0e567-06aa-43e0-a632-3414b848e12c",
//     playlist_name: "Testing Integration 2",
//     track_idx: 2,
//     image_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/images/Solo_2024-12-16T13%3A41%3A36.560786.png",
//     music_url:
//       "https://storage.googleapis.com/maca-deb33.appspot.com/HMO/Testing%20Integration%202_2024-12-16T13%3A41%3A18.968806/audios/Solo_2024-12-16T13%3A41%3A39.401629.wav",
//     track_name: "Solo",
//   },
// ];
