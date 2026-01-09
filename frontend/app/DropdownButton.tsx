"use client";
import { useState } from "react";

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
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={disabled}
        className="px-8 py-2 rounded-full bg-dropdown-button-bg text-neutral-50 font-bold text-lg shadow-lg hover:bg-dropdown-button-hover-bg transition-all ease-linear duration-50"
      >
        {labels[values.indexOf(value)]}
      </button>
      {isOpen && (
        <div className="absolute rounded-xl mt-12 bg-dropdown-button-bg shadow-lg z-10 py-2">
          {labels.map((label, index) => (
            <div
              key={index}
              onClick={() => handleOptionClick(index)}
              className={`px-12 pt-2 pb-2 text-neutral-200 border-neutral-300/50 text-lg font-semibold ${
                index > 0 && "border-t"
              } hover:bg-dropdown-button-hover-bg cursor-pointer select-none whitespace-nowrap`}
            >
              {label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
