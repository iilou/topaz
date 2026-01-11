export default function Button({
    children,
    onClick,
    disabled = false,
    className = "",
}: {
    children: React.ReactNode;
    onClick: () => void;
    disabled?: boolean;
    className?: string;
}) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={
                "px-6 py-1 rounded-full bg-dropdown-button-bg text-neutral-50 hover:text-neutral-200 font-bold text-base shadow-lg hover:bg-dropdown-button-hover-bg transition-all ease-linear duration-50 " +
                className
            }
        >
            {children}
        </button>
    );
}
