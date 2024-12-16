import Link from "next/link";
import React from "react";

const Navbar = () => {
  return (
    <div className="h-20 bg-spotify-black-2 w-full text-white flex justify-between items-center px-20 sticky top-0 z-50 shadow-xl">
      <Link href={"/"} className="text-2xl">
        HearMeOut
      </Link>
      <div className="flex items-center justify-center gap-20 text-xl">
        <Link href={"/"}>Home</Link>
        <Link href={"/contribute"}>Contribute</Link>
      </div>
    </div>
  );
};

export default Navbar;
