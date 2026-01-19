import { ChatHistory, EditChatHistory } from "../types/chat";

export async function fetchChatHistories(): Promise<ChatHistory[]> {
    const response = await fetch(`/api/chat/histories`);
    console.log("Fetch Chat Histories Response:", response);

    if (!response.ok) {
        throw new Error("Failed to fetch chat histories");
    }

    // transfrom json response to ChatHistory[]
    const data = await response.json();

    // //temp
    // console.log("Chat Histories Data:", data);

    // validate data structure
    return data as ChatHistory[];
}
