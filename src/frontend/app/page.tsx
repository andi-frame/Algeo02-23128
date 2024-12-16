import Playlists from "@/components/Playlists";
import Query from "@/components/query";

export default function Home() {
  return (
    <div className="bg-spotify-black-1/50 flex flex-col justify-center items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <Query />
      <Playlists />
    </div>
  );
}
