"use client";

import DropdownButton from "../DropdownButton";
import ChatMessage from "./ChatMessage";

import { Search } from "lucide-react";
import { AuroraText } from "@/components/ui/aurora-text";
import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";

import { ChatHistoryMessage } from "@/lib/types/chat";
import { fetchChatHistoryMessages, sendNewChatMessage } from "@/lib/data/chatHistoryMessages";
import { CreateChatHistoryMessage } from "@/lib/types/chat";

const MAX_TEXTAREA_ROWS = 6;

interface ChatAreaProps {
    chatId?: string;
}

export default function ChatArea({ chatId }: ChatAreaProps) {
    const [topic, setTopic] = useState("genetics");
    const [tier, setTier] = useState("gemini-2.0-flash");

    const [chatHistory, setChatHistory] = useState<ChatHistoryMessage[]>([]);
    const [canType, setCanType] = useState<string | null>(null);
    const [inputLineCount, setInputLineCount] = useState(0);

    const scrollRef = useRef<HTMLDivElement>(null);

    const router = useRouter();

    async function sendMessage(message: string, tempId: string) {
        const messageData: CreateChatHistoryMessage = {
            message: message,
            llm: tier,
        };

        try {
            const res = await sendNewChatMessage(messageData, chatId || undefined);

            // check if res is empty
            if (!res) {
                throw new Error("No response from server");
            }

            if (res.history && !chatId) {
                router.push(`/chat/${res.history.history_id}`);
            }

            console.log("msg data", res);

            const message = res.message;

            setChatHistory((prev) => {
                return prev.map((msg) => {
                    if (msg.id === tempId) {
                        return message;
                    }
                    return msg;
                });
            });

            setCanType(null);
        } catch (error) {
            console.error("Error sending new chat message:", error);
        }
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const lineCount = e.target.value.split("\n").length;
        setInputLineCount(lineCount);
    };

    const handleInputKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            if (canType) {
                return;
            }

            e.preventDefault();

            const inputField = e.target as HTMLTextAreaElement;
            const message = inputField.value.trim();

            const tempId = crypto.randomUUID();
            setCanType(() => tempId);
            setChatHistory((prev) => [
                ...prev,
                {
                    message: message,
                    response: "Thinking...",
                    timestamp: new Date().toISOString(),
                    llm: "gemini-2.5-flash",
                    id: tempId,
                },
            ]);

            inputField.value = "";
            setInputLineCount(0);

            sendMessage(message, tempId);
        }

        if (e.key === "Enter" && e.shiftKey) {
            // check if last line is empty
            const textarea = e.target as HTMLTextAreaElement;

            return;
        }
    };

    useEffect(() => {
        async function fetchChatHistory() {
            if (!chatId) {
                setCanType(() => null);
                setChatHistory([]);
                return;
            }
            try {
                setCanType(() => "loading");
                const messages = await fetchChatHistoryMessages(chatId);
                setCanType(() => null);

                setChatHistory(messages);
                console.log("Fetched chat history messages:", messages);
            } catch (error) {
                console.error("Error fetching chat history messages:", error);
            }
        }

        fetchChatHistory();
    }, [chatId]);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatHistory]);

    return (
        <div className="flex flex-col justify-end items-center h-full w-full">
            <div
                className="h-full flex flex-col justify-center items-center"
                {...(chatHistory.length > 0 ? { style: { display: "none" } } : {})}
            >
                <h1 className="text-5xl font-semibold text-center px-4">
                    Welcome to{" "}
                    <AuroraText colors={["#96D5E0", "#79B8C3", "#35707A", "#144E58"]}>TutorMonkey Chat</AuroraText>
                </h1>
                <p className="text-xl italic text-center mt-4 text-neutral-600 font-normal px-4">
                    Get personalized academic assistance powered by AI.
                </p>
            </div>
            <div className="w-full grow overflow-y-auto mb-4 max-w-5xl px-4 mx-auto">
                {chatHistory.map((item, index) => (
                    <>
                        <ChatMessage key={"user-" + index} message={item.message} isUser={true} />
                        <ChatMessage key={"bot-" + index} message={item.response} isUser={false} />
                    </>
                ))}
                <div ref={scrollRef} />
            </div>
            <div className="w-full max-w-5xl mb-0 px-4 mx-auto">
                <div className="flex gap-4 w-full justify-end items-center">
                    <DropdownButton
                        setStateFunc={setTier}
                        values={["gemini-2.5-flash"]}
                        labels={["Gemini 2.5 Flash"]}
                        currentIndex={0}
                    />
                </div>
                <div className="mt-3 w-full shadow-xl rounded-md">
                    <div
                        className="flex items-center justify-center px-4 py-3 bg-white rounded-md"
                        style={{
                            boxShadow: canType ? "0 0 0 1px #d4d4d4" : "0 0 0 1px #00000099",
                        }}
                    >
                        <textarea
                            className="w-full bg-none outline-none text-base resize-none px-2"
                            placeholder={`Ask me anything about ${topic}...`}
                            rows={Math.max(Math.min(inputLineCount, MAX_TEXTAREA_ROWS), 1)}
                            onChange={handleInputChange}
                            onKeyDown={handleInputKeyDown}
                        />
                        <div className="flex justify-center items-center h-full px-2 flex-col">
                            <Search
                                className={` hover:font-bold ${canType ? "text-neutral-300" : "text-neutral-500 hover:text-neutral-700"}`}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
