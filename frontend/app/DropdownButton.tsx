"use client";
import { useState } from "react";
import Button from "./Button";

interface DropdownButtonProps {
    setStateFunc: (val: any) => void;
    values: string[];
    labels: string[];
    currentIndex: number;
    disabled?: boolean;
    disabledIndices?: number[];
}

export default function DropdownButton({
    setStateFunc,
    values,
    labels,
    currentIndex,
    disabled = false,
    disabledIndices = [],
}: DropdownButtonProps) {
    const [value, setValue] = useState(values[currentIndex]);
    const [isOpen, setIsOpen] = useState(false);

    const handleOptionClick = (index: number) => {
        if (disabledIndices.includes(index)) return;
        const selectedValue = values[index];
        setValue(selectedValue);
        setStateFunc(selectedValue);
        setIsOpen(false);
    };

    return (
        <div className="relative text-center flex items-center flex-col">
            <Button onClick={() => setIsOpen(!isOpen)} disabled={disabled}>
                {labels[values.indexOf(value)]}
            </Button>
            {isOpen && (
                <div className="absolute rounded-xl mt-9 bg-dropdown-button-bg/95 shadow-[2px_2px_6px_1px_#00000033] z-10 py-2 px-2">
                    {labels.map((label, index) => (
                        <div
                            key={index}
                            onClick={() => handleOptionClick(index)}
                            className={`px-4 pt-1 pb-1 text-neutral-200 border-neutral-300/50 hover:text-neutral-300 text-base font-semibold ${
                                index > 0 && "border-t"
                            } ${index < labels.length - 1 && "border-b"}
                                hover:bg-dropdown-button-hover-bg cursor-pointer select-none whitespace-nowrap transition-all ease-linear duration-50 rounded-md ${
                                    disabledIndices.includes(index)
                                        ? "opacity-50 cursor-not-allowed hover:text-neutral-200 hover:bg-dropdown-button-bg"
                                        : ""
                                }`}
                        >
                            {label}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
