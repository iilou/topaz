import { ChatHistoryMessage, CreateChatHistoryMessage, CreateChatHistoryMessageResponse } from "../types/chat";

export async function fetchChatHistoryMessages(chatHistoryId: string): Promise<ChatHistoryMessage[]> {
    const response = await fetch(`/api/chat/history/${chatHistoryId}/messages`);

    if (!response.ok) {
        throw new Error("Failed to fetch chat history messages");
    }

    const data = await response.json();
    return data as ChatHistoryMessage[];
}

export async function sendNewChatMessage(
    messageData: CreateChatHistoryMessage,
    historyId?: string,
): Promise<CreateChatHistoryMessageResponse> {
    const response = await fetch(historyId ? `/api/chat/history/${historyId}/messages` : `/api/chat/history/messages`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(messageData),
    });

    if (!response.ok) {
        throw new Error("Failed to send new chat message");
    }

    // console.log("msg response", response.json());
    return response.json();
}
