import HomeBackground from "./HomeBackground";
import SearchBar from "./SearchBar";

import { AuroraText } from "@/components/ui/aurora-text";

export default function Home() {
    return (
        <div>
            <HomeBackground />
            <div>
                <div className="w-[95%] max-w-300 mx-auto mt-36 flex flex-col items-center bg-neutral-50/80 py-20 rounded-4xl px-12 relative shadow-xl">
                    <h1 className="text-5xl font-semibold text-center px-4 pt-12">
                        <AuroraText colors={["#96D5E0", "#79B8C3", "#35707A", "#144E58"]}>Achieve</AuroraText> your
                        Academic Potential with AI
                    </h1>
                    <p className="text-xl italic text-center mt-4 text-neutral-600 font-normal px-4">
                        Get instant help with homework, concepts, and study plans tailored just for you.
                    </p>
                    <div className="mt-20 flex space-x-4">
                        <a href="#search">
                            <button className="px-8 py-3 rounded-full bg-cyan-900 text-neutral-50 text-lg font-bold hover:bg-cyan-800 transition-all ease-linear duration-50">
                                Get Started
                            </button>
                        </a>
                        <button className="px-8 py-3 rounded-full border-2 border-cyan-900 text-cyan-900 text-lg font-bold hover:bg-neutral-100 transition-all ease-linear duration-50">
                            Learn More
                        </button>
                    </div>
                </div>
                <SearchBar />
            </div>
        </div>
    );
}
