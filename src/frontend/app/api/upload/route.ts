import { NextResponse } from "next/server";
import api from "@/api";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function POST(request: { formData: () => any }) {
  const formData = await request.formData();
  const playlistName = formData.get("playlistName");
  const images = formData.get("images");
  const audios = formData.get("audios");
  const mapper = formData.get("mapper");
  console.log("Playlist Name:", playlistName);

  const formDataToSend = new FormData();
  formDataToSend.append("playlistName", playlistName);
  formDataToSend.append("images", images);
  formDataToSend.append("audios", audios);
  formDataToSend.append("mapper", mapper);

  try {
    const response = await api.post("/upload", formDataToSend, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return NextResponse.json(response.data);
  } catch (error) {
    return NextResponse.json(error, { status: 500 });
  }
}
