import SidebarHistoryItem from "./SidebarHistoryItem";

const getChats = async () => [
    "Genetics | Understanding DNA Replication",
    "Genetics | Mendelian Inheritance Patterns",
    "Calculus | Solving Derivatives",
];

export default async function SidebarHistory() {
    const exampleChats = await getChats();

    return (
        <div className="flex flex-col items-center justify-center px-4 mt-4">
            <h2 className="text-3xl font-bold text-center px-4 text-cyan-950">Your Chats</h2>
            <p className="text-md italic text-center text-neutral-600 font-normal px-4">
                Continue your learning journey
            </p>
            <div className="w-full mt-4 space-y-1">
                {exampleChats.map((chatTitle, index) => (
                    <SidebarHistoryItem key={index} title={chatTitle} />
                ))}
            </div>
        </div>
    );
}
