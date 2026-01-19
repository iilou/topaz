"use client";

import SidebarHistoryItem from "./SidebarHistoryItem";

import { useEffect, useState } from "react";

import { fetchChatHistories } from "@/lib/data/chatHistories";
import { ChatHistory } from "@/lib/types/chat";

interface SidebarHistoryProps {
    chatId?: string;
}

export default function SidebarHistory() {
    const [chatHistoryList, setChatHistoryList] = useState<ChatHistory[]>([]);

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
        <div className="flex flex-col items-center justify-center px-4 mt-3">
            <h2 className="text-3xl font-bold text-center px-4 text-cyan-950">Your Chats</h2>
            <p className="text-md italic text-center text-neutral-600 font-normal px-4">
                Continue your learning journey
            </p>
            <div className="w-full mt-4 space-y-1">
                {chatHistoryList.map((item, index) => (
                    <SidebarHistoryItem key={index} title={item.name || "Untitled Chat"} chatId={item.history_id} />
                ))}
            </div>
        </div>
    );
}
