"use client";

import DropdownButton from "../DropdownButton";
import { Search } from "lucide-react";
import { AuroraText } from "@/components/ui/aurora-text";
import { useState } from "react";

const MAX_TEXTAREA_ROWS = 6;

export default function ChatArea() {
    const [topic, setTopic] = useState("genetics");
    const [tier, setTier] = useState("free");

    const [inputLineCount, setInputLineCount] = useState(0);

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const lineCount = e.target.value.split("\n").length;
        setInputLineCount(lineCount);
    };

    const handleInputKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            // document.querySelector("textarea")!.value = "";
            (e.target as HTMLTextAreaElement).value = "";
            setInputLineCount(0);
        }

        if (e.key === "Enter" && e.shiftKey) {
            // check if last line is empty
            return;
        }
    };

    return (
        <div className="mx-4 flex flex-col justify-end items-center h-full w-full">
            <div className="h-full flex flex-col justify-center items-center">
                <h1 className="text-5xl font-semibold text-center px-4">
                    Welcome to{" "}
                    <AuroraText colors={["#96D5E0", "#79B8C3", "#35707A", "#144E58"]}>TutorMonkey Chat</AuroraText>
                    {/* Welcome to <span className="text-cyan-900">TutorMonkey Chat</span> */}
                </h1>
                <p className="text-xl italic text-center mt-4 text-neutral-600 font-normal px-4">
                    Get personalized academic assistance powered by AI.
                </p>
            </div>
            <div className="flex gap-4 w-full ml-8">
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
            <div className="mt-3 w-full shadow-xl rounded-2xl">
                <div className="flex items-center justify-center shadow-[0_0_0_1px_#00000099] px-4 py-2 bg-white rounded-2xl">
                    <textarea
                        className="w-full bg-none outline-none text-lg resize-none px-2"
                        placeholder={`Ask me anything about ${topic}...`}
                        rows={Math.max(Math.min(inputLineCount, MAX_TEXTAREA_ROWS), 1)}
                        onChange={handleInputChange}
                        onKeyDown={handleInputKeyDown}
                    />
                    <div className="flex justify-center items-center h-full px-2 flex-col">
                        <Search className=" text-neutral-500 hover:text-neutral-700 hover:font-bold" />
                    </div>
                </div>
            </div>
        </div>
    );
}
