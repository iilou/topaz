"use client";

import ChatArea from "./ChatArea";
import SideBar from "./Sidebar";

import { useParams } from "next/navigation";

export default function ChatShell() {
    const params = useParams();
    const { id } = params;

    return (
        <div className="w-[95%] flex mx-auto h-full pt-28 pb-14 relative">
            <SideBar chatId={typeof id === "string" ? id : undefined} />
            <ChatArea chatId={typeof id === "string" ? id : undefined} />
        </div>
    );
}
