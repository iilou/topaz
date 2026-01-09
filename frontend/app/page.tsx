"use client";

import Image from "next/image";

import Header from "./header";
import DropdownButton from "./DropdownButton";

import { useState } from "react";

import { Search } from "lucide-react";

export default function Home() {
  // const [selectedOption, setSelectedOption] = useState("option1");
  const [topic, setTopic] = useState("genetics");
  const [tier, setTier] = useState("free");

  return (
    <div>
      <div>
        <Header />
        <div className="w-[95%] max-w-250 mx-auto mt-20 flex flex-col items-center bg-neutral-50/80 py-16 rounded-4xl shadow-lg px-12">
          <h1 className="text-7xl font-semibold text-center px-4">
            Achieve your Academic Potential with AI
          </h1>
          <p className="text-2xl italic text-center mt-4 text-neutral-600 font-normal px-4">
            Get instant help with homework, concepts, and study plans tailored
            just for you.
          </p>
          <div className="mt-14 flex space-x-4">
            <button className="px-8 py-3 rounded-full bg-cyan-900 text-neutral-50 text-lg font-bold hover:bg-cyan-800 transition-all ease-linear duration-50">
              Get Started
            </button>
            <button className="px-8 py-3 rounded-full border-2 border-cyan-900 text-cyan-900 text-lg font-bold hover:bg-neutral-100 transition-all ease-linear duration-50">
              Learn More
            </button>
          </div>
        </div>

        <div className="w-[95%] max-w-250 mx-auto mt-32 mb-16">
          <div className="flex gap-4">
            <DropdownButton
              setStateFunc={setTopic}
              values={["genetics", "calculus", "organic-chemistry"]}
              labels={["Genetics", "Calculus", "Organic Chemistry"]}
              currentIndex={0}
            />
            <DropdownButton
              setStateFunc={setTier}
              values={["free", "pro", "premium"]}
              labels={["Free", "Pro", "Premium"]}
              currentIndex={0}
            />
          </div>
          <div className="mt-2 w-full py-2 bg-neutral-200 rounded-2xl flex items-center justify-center">
            {/* <input
              className="w-[90%] bg-none outline-none text-lg"
              placeholder={`Ask me anything about ${topic}...`}
            /> */}
            <textarea
              className="w-[90%] bg-none outline-none text-lg resize-none h-24 p-2"
              placeholder={`Ask me anything about ${topic}...`}
            />
            <Search className=" text-neutral-500 hover:text-neutral-700 hover:font-bold" />
          </div>
        </div>
      </div>
    </div>
  );
}
