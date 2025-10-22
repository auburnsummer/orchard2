import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaste } from "@fortawesome/free-solid-svg-icons";
import { useClipboard } from "@mantine/hooks";
import { useState } from "react";
import cc from "clsx";

type CopyIconButtonProps = {
  value: string;
  className?: string;
};

export function CopyIconButton({ value, className }: CopyIconButtonProps) {
  const { copy, copied } = useClipboard({ timeout: 300 });
  const [showTooltip, setShowTooltip] = useState(false);

  const handleClick = () => {
    copy(value);
    setShowTooltip(true);

    // Hide tooltip after 1 second
    setTimeout(() => {
      setShowTooltip(false);
    }, 1000);
  };

  return (
    <div className={cc("relative inline-block", className)}>
      <button
        onClick={handleClick}
        className={cc(
          "w-8 h-8",
          "flex items-center justify-center transition-all duration-150 ease-out",
          "text-slate-600 hover:text-slate-800 hover:cursor-pointer focus:outline-none",
          " dark:text-slate-300  dark:hover:text-slate-100",
          copied && "animate-pulse scale-95"
        )}
        title="Copy to clipboard"
      >
        <FontAwesomeIcon 
          icon={faPaste} 
          className={cc(
            "w-4 h-4 transition-all duration-150",
            copied && "-rotate-6 text-violet-800 dark:text-violet-200"
          )}
        />
      </button>
      
      {/* Tooltip */}
      {showTooltip && (
        <div
          className={cc(
            "absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1",
            "bg-slate-800 text-white text-xs rounded-md shadow-lg whitespace-nowrap",
            "animate-in fade-in slide-in-from-bottom-1 duration-200",
            "dark:bg-slate-200 dark:text-slate-800"
          )}
        >
          Copied!
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-2 border-r-2 border-t-2 border-transparent border-t-slate-800 dark:border-t-slate-200" />
        </div>
      )}
    </div>
  );
}
