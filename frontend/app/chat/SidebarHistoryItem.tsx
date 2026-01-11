interface SidebarHistoryItemProps {
    title: string;
    chatId?: string;
}

export default function SidebarHistoryItem({ title }: SidebarHistoryItemProps) {
    return (
        <div className="w-full px-4 py-2 rounded-lg cursor-pointer text-neutral-800 font-semibold hover:bg-neutral-300 transition-all ease-linear duration-50">
            {title}
        </div>
    );
}
