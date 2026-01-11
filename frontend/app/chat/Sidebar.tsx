"use client";

import { X } from "lucide-react";
import { ChevronFirst, ChevronLast } from "lucide-react";

import { useState } from "react";

interface SideBarProps {
    children?: React.ReactNode;
}

export default function SideBar({ children }: SideBarProps) {
    const [sideBarOpen, setSidebarOpen] = useState(false);

    return (
        <>
            {!sideBarOpen && (
                <button
                    className="absolute flex gap-1 items-center px-3 py-1 rounded-full bg-dropdown-button-bg text-neutral-50 hover:text-neutral-200 font-bold text-base shadow-lg hover:bg-dropdown-button-hover-bg transition-all ease-linear duration-50 left-4 top-30"
                    onClick={() => setSidebarOpen(true)}
                >
                    <ChevronLast size={20} strokeWidth={3} />
                </button>
            )}
            {sideBarOpen && (
                <div
                    className={`md:w-1/4 bg-neutral-200 rounded-2xl shadow-xl mx-4 min-w-80 absolute md:relative md:h-full md:left-0 md:bottom-0 md:top-0 md:right-0 -right-2 -left-2 top-24 bottom-8 z-20`}
                >
                    <div className="mr-2 mt-2 flex justify-end">
                        <button
                            onClick={() => setSidebarOpen(false)}
                            className="flex gap-1 items-center px-3 py-1 rounded-full bg-dropdown-button-bg text-neutral-50 hover:text-neutral-200 font-bold text-base shadow-lg hover:bg-dropdown-button-hover-bg transition-all ease-linear duration-50"
                        >
                            <X size={20} strokeWidth={3} />
                        </button>
                    </div>
                    {children}
                </div>
            )}
        </>
    );
}
