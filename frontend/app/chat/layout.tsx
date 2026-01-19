import ChatShell from "./ChatShell";

export default function ChatLayout({ children }: { children: React.ReactNode }) {
    return (
        <main className="w-full h-screen bg-neutral-50">
            <ChatShell />
            {children}
        </main>
    );
}
