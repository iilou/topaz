import { AuroraText } from "@/components/ui/aurora-text";
import HeaderAuth from "./HeaderAuth";

export default async function Header() {
    return (
        <div className="w-[95%] mx-auto bg-neutral-50 h-14 flex items-center rounded-full mt-4 shadow-lg fixed top-0 left-0 right-0 z-20">
            <a href="/" className="text-xl font-extrabold px-12 hidden lg:block cursor-default select-none">
                <AuroraText colors={["#96D5E0", "#79B8C3", "#35707A", "#144E58"]}>TutorMonkey</AuroraText>
            </a>
            <div className="flex mx-auto">
                <a className="px-6 text-base font-semibold cursor-pointer" href="/">
                    Home
                </a>
                <a className="px-6 text-base font-semibold cursor-pointer" href="/chat">
                    Chat
                </a>
                <a className="px-6 text-base font-semibold cursor-pointer">Features</a>
            </div>
            <HeaderAuth />
        </div>
    );
}
