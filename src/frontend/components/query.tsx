import React from "react";
import { Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext } from "./ui/carousel";
import QueryImage from "./QueryImage";
import QueryHumming from "./QueryHumming";
import QueryMic from "./QueryMic";

const Query = () => {
  return (
    <Carousel className="w-full max-w-lg">
      <CarouselContent className="">
        <CarouselItem className="flex justify-center items-center ring-none outline-none">
          <div className="p-1 w-[1400px]">
            <QueryImage />
          </div>
        </CarouselItem>
        <CarouselItem className="flex justify-center items-center ring-none outline-none">
          <div className="p-1 w-[1400px]">
            <QueryHumming />
          </div>
        </CarouselItem>
        <CarouselItem className="flex justify-center items-center ring-none outline-none">
          <div className="p-1 w-[1400px]">
            <QueryMic />
          </div>
        </CarouselItem>
      </CarouselContent>
      <CarouselPrevious />
      <CarouselNext />
    </Carousel>
  );
};

export default Query;
