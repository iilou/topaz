import ChatArea from "./ChatArea";

import SideBar from "./Sidebar";
import SidebarHistory from "./SidebarHistory";

export default function ChatPage() {
    return (
        <div className="w-full bg-neutral-50 h-screen">
            <div className="w-[95%] flex mx-auto h-full pt-28 pb-14 relative">
                <SideBar>
                    <SidebarHistory />
                </SideBar>
                <ChatArea />
            </div>
        </div>
    );
}
