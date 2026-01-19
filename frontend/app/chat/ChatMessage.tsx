interface ChatMessageProps {
    message: string;
    isUser?: boolean;
}

export default function ChatMessage({ message, isUser = false }: ChatMessageProps) {
    // let messageStyle = "";
    // if (type === ChatMessageType.USER) {
    //     messageStyle = "bg-neutral-100 text-neutral-800 self-end";
    // } else if (type === ChatMessageType.BOT) {
    //     messageStyle = "bg-neutral-200 text-neutral-800 self-start";
    // } else if (type === ChatMessageType.BOT_LOADING) {
    //     messageStyle = "bg-neutral-200 text-neutral-800 self-start italic";
    // }
    const messageStyle = isUser
        ? "bg-neutral-100 text-neutral-800 self-end"
        : "bg-neutral-200 text-neutral-800 self-start";

    return (
        <div className="flex flex-col w-full">
            <div className={`mb-1 text-neutral-800 text-base font-semibold ${isUser ? "self-end" : "self-start"}`}>
                {isUser ? "You:" : "TutorMonkey:"}
            </div>
            <div className={`max-w-[80%] ${messageStyle} px-4 py-2 rounded-md mb-2 shadow-md text-sm`}>{message}</div>
        </div>
    );
}
