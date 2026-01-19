import { useRouter } from "next/navigation";

interface SidebarHistoryItemProps {
    title: string;
    chatId?: string;
    current: boolean;
}

export default function SidebarHistoryItem({ title, chatId, current }: SidebarHistoryItemProps) {
    const router = useRouter();
    return (
        <div
            className={`w-full px-4 py-2 rounded-sm text-sm cursor-pointer font-base
                transition-all ease-linear duration-50 ${current ? "bg-dropdown-button-bg text-neutral-300 italic" : "bg-neutral-200 text-neutral-800 hover:bg-neutral-300 hover:text-neutral-900"}`}
            onClick={() => {
                if (chatId && !current) {
                    router.push(`/chat/${chatId}`);
                }
            }}
        >
            {title}
        </div>
    );
}
