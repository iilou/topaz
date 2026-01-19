"use client";

import { X } from "lucide-react";
import { ChevronFirst, ChevronLast } from "lucide-react";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

import { fetchChatHistories } from "@/lib/data/chatHistories";
import { ChatHistory } from "@/lib/types/chat";

import SidebarHistoryItem from "./SidebarHistoryItem";

interface SideBarProps {
    chatId?: string;
}

export default function SideBar({ chatId }: SideBarProps) {
    const [sideBarOpen, setSidebarOpen] = useState(false);
    const [chatHistoryList, setChatHistoryList] = useState<ChatHistory[]>([]);

    const router = useRouter();

    useEffect(() => {
        async function loadChatHistories() {
            try {
                const histories = await fetchChatHistories();
                setChatHistoryList(histories);
            } catch (error) {
                console.error("Error fetching chat histories:", error);
            }
        }

        loadChatHistories();
    }, []);

    return (
        <>
            <button
                className="absolute flex gap-1 items-center px-3 py-1 rounded-md bg-dropdown-button-bg text-neutral-50 hover:text-neutral-200 font-bold text-base shadow-lg hover:bg-dropdown-button-hover-bg transition-all ease-linear duration-50 left-4 top-30"
                onClick={() => setSidebarOpen(true)}
                {...(!sideBarOpen ? {} : { style: { display: "none" } })}
            >
                <ChevronLast size={20} strokeWidth={3} />
            </button>
            <div
                className={`md:w-1/4 bg-neutral-100 rounded-md shadow-xl mx-4 min-w-80 absolute md:relative md:h-full md:left-0 md:bottom-0 md:top-0 md:right-0 -right-2 -left-2 top-24 bottom-8 z-20`}
                {...(!sideBarOpen ? { style: { display: "none" } } : {})}
            >
                <div className="absolute left-0 right-0 top-0 bottom-0 z-30 shadow-[0_0_0_1px_#00000099] rounded-md pointer-events-none"></div>
                <div className="mr-2 mt-2 flex justify-end">
                    <button
                        onClick={() => setSidebarOpen(false)}
                        className="flex gap-1 items-center px-3 py-1 rounded-md bg-dropdown-button-bg text-neutral-50 hover:text-neutral-200 font-bold text-base shadow-lg hover:bg-dropdown-button-hover-bg transition-all ease-linear duration-50"
                    >
                        <X size={20} strokeWidth={3} />
                    </button>
                </div>
                <div className="flex flex-col items-center justify-center px-8 mt-6">
                    <h2 className="text-3xl font-bold text-center px-4 text-cyan-950">Your Chats</h2>
                    <p className="text-md italic text-center text-neutral-600 font-normal px-4">
                        Continue your learning journey
                    </p>
                    <div className="w-full mt-8 space-y-1">
                        {chatHistoryList.map((item, index) => (
                            <SidebarHistoryItem
                                key={index}
                                title={item.name || "Untitled Chat"}
                                chatId={item.history_id}
                                current={chatId === item.history_id}
                            />
                        ))}
                    </div>
                </div>
                <div className="absolute bottom-2 right-2">
                    <button
                        className="px-4 py-2 rounded-md text-sm cursor-pointer bg-dropdown-button-bg text-neutral-50 font-semibold hover:bg-dropdown-button-hover-bg transition-all ease-linear duration-50"
                        onClick={() => router.push("/chat")}
                    >
                        New Chat
                    </button>
                </div>
            </div>
        </>
    );
}
