export interface ChatHistoryMessage {
    message: string;
    response: string;
    timestamp: string;
    llm: string;
    id: string;
}

export interface ChatHistory {
    user_id: string;
    history_id: string;
    created_at: string;
    name: string;
    description?: string;
}

export interface EditChatHistory {
    name?: string;
    description?: string;
}

export interface CreateChatHistoryMessage {
    message: string;
    llm: string;
}

export interface CreateChatHistoryMessageResponse {
    message: ChatHistoryMessage;
    history?: ChatHistory;
}