"use client";

import { sendNewChatMessage } from "@/lib/data/chatHistoryMessages";
import { CreateChatHistoryMessage, CreateChatHistoryMessageResponse, ChatHistory } from "@/lib/types/chat";

import { Search } from "lucide-react";

export default function SearchBar() {
    const handleInputSubmission = async (input: string) => {
        const messageData: CreateChatHistoryMessage = {
            message: input,
            llm: "gemini-2.5-flash",
        };

        try {
            const res: CreateChatHistoryMessageResponse = await sendNewChatMessage(messageData);

            if (res.history) {
                // router.push(`/chat/${res.history.history_id}`);
                window.location.href = `/chat/${res.history.history_id}`;
            }
        } catch (error) {
            console.error("Error sending new chat message:", error);
        }
    };

    const handleInputChange = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") {
            e.preventDefault();
            const input = (e.target as HTMLInputElement).value.trim();
            if (input) {
                handleInputSubmission(input);
                (e.target as HTMLInputElement).value = "";
            }
        }
    };

    return (
        <div className="w-[95%] max-w-350 mx-auto mt-20 mb-16" id="search">
            <div className="mt-2 w-full py-1 bg-neutral-200 rounded-md flex items-center justify-center shadow-xl relative">
                <input
                    className="w-[calc(100%-3.5rem)] bg-none px-4 outline-none text-base h-12 rounded-md"
                    type="text"
                    placeholder={`Ask me anything...`}
                    onKeyDown={handleInputChange}
                />
                <Search className="w-6 text-neutral-500 hover:text-neutral-700 hover:font-bold" />
            </div>
        </div>
    );
}
