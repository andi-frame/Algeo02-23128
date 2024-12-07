import { NextRequest, NextResponse } from "next/server";
import axios from "axios";

export async function POST(request: NextRequest) {
  try {
    const body = await request.formData();

    const formData = new FormData();
    formData.append("file", body.get("file") as File);
    formData.append("upload_type", body.get("upload_type") as string);

    const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND_URL}/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return NextResponse.json(response.data, {
      status: response.status,
    });
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    console.error("Upload error:", error);

    if (error.response) {
      return NextResponse.json(error.response.data, {
        status: error.response.status,
      });
    } else if (error.request) {
      return NextResponse.json(
        {
          message: "No response received from server",
        },
        {
          status: 500,
        }
      );
    } else {
      return NextResponse.json(
        {
          message: "Error in upload request",
          error: error.message,
        },
        {
          status: 500,
        }
      );
    }
  }
}

export const config = {
  api: {
    bodyParser: false,
  },
};
