import React, { useRef, useState, useCallback } from "react";
import cc from "clsx";

type SliderProps = {
    label?: string | null;
    step?: number;
    min: number;
    max: number;
    value: number;
    onChange: (value: number) => void;
    // if true, the slider will snap to marks and not allow intermediate values
    restrictToMarks?: boolean;
    marks?: { value: number; label: string }[];
    className?: string;
    disabled?: boolean;
}

export function Slider({
    label,
    step = 1,
    min,
    max,
    value,
    onChange,
    restrictToMarks = false,
    marks = [],
    className,
    disabled = false,
}: SliderProps) {
    const trackRef = useRef<HTMLDivElement>(null);
    const [isDragging, setIsDragging] = useState(false);

    const percentage = ((value - min) / (max - min)) * 100;

    const getValueFromPosition = useCallback((clientX: number) => {
        if (!trackRef.current) return value;
        
        const rect = trackRef.current.getBoundingClientRect();
        const position = (clientX - rect.left) / rect.width;
        const clampedPosition = Math.max(0, Math.min(1, position));
        
        let newValue = min + clampedPosition * (max - min);

        if (restrictToMarks && marks.length > 0) {
            // Snap to nearest mark
            const markValues = marks.map(m => m.value);
            newValue = markValues.reduce((prev, curr) => 
                Math.abs(curr - newValue) < Math.abs(prev - newValue) ? curr : prev
            );
        } else if (step) {
            // Snap to step
            newValue = Math.round(newValue / step) * step;
        }

        return Math.max(min, Math.min(max, newValue));
    }, [min, max, step, restrictToMarks, marks, value]);

    const handleMouseDown = (e: React.MouseEvent) => {
        if (disabled) return;
        e.preventDefault();
        setIsDragging(true);
        const newValue = getValueFromPosition(e.clientX);
        onChange(newValue);
    };

    const handleMouseMove = useCallback((e: MouseEvent) => {
        if (!isDragging || disabled) return;
        e.preventDefault();
        const newValue = getValueFromPosition(e.clientX);
        onChange(newValue);
    }, [isDragging, disabled, getValueFromPosition, onChange]);

    const handleMouseUp = useCallback(() => {
        setIsDragging(false);
    }, []);

    React.useEffect(() => {
        if (isDragging) {
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', handleMouseUp);
            return () => {
                document.removeEventListener('mousemove', handleMouseMove);
                document.removeEventListener('mouseup', handleMouseUp);
            };
        }
    }, [isDragging, handleMouseMove, handleMouseUp]);

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (disabled) return;
        
        let newValue = value;
        const effectiveStep = restrictToMarks && marks.length > 0 
            ? undefined 
            : (step || 1);

        if (restrictToMarks && marks.length > 0) {
            const sortedMarks = [...marks].sort((a, b) => a.value - b.value);
            const currentIndex = sortedMarks.findIndex(m => m.value === value);
            
            if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
                e.preventDefault();
                if (currentIndex < sortedMarks.length - 1) {
                    const nextMark = sortedMarks[currentIndex + 1];
                    if (nextMark) newValue = nextMark.value;
                }
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
                e.preventDefault();
                if (currentIndex > 0) {
                    const prevMark = sortedMarks[currentIndex - 1];
                    if (prevMark) newValue = prevMark.value;
                }
            } else if (e.key === 'Home') {
                e.preventDefault();
                const firstMark = sortedMarks[0];
                if (firstMark) newValue = firstMark.value;
            } else if (e.key === 'End') {
                e.preventDefault();
                const lastMark = sortedMarks[sortedMarks.length - 1];
                if (lastMark) newValue = lastMark.value;
            }
        } else {
            if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
                e.preventDefault();
                newValue = Math.min(max, value + (effectiveStep || 1));
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
                e.preventDefault();
                newValue = Math.max(min, value - (effectiveStep || 1));
            } else if (e.key === 'Home') {
                e.preventDefault();
                newValue = min;
            } else if (e.key === 'End') {
                e.preventDefault();
                newValue = max;
            }
        }

        if (newValue !== value) {
            onChange(newValue);
        }
    };

    return (
        <div className={cc("w-full", className)}>
            {label && (
                <label className="block text-sm/6 font-medium text-slate-900 dark:text-white mb-2">
                    {label}
                </label>
            )}
            
            <div className="relative px-2 py-4">
                {/* Track */}
                <div
                    ref={trackRef}
                    className={cc(
                        "relative h-2 rounded-full bg-slate-200 dark:bg-slate-700",
                        !disabled && "cursor-pointer"
                    )}
                    onMouseDown={handleMouseDown}
                >
                    {/* Filled track */}
                    <div
                        className="absolute h-full rounded-full bg-violet-500 dark:bg-violet-600 transition-all"
                        style={{ width: `${percentage}%` }}
                    />
                    
                    {/* Marks */}
                    {marks.map((mark) => {
                        const markPercentage = ((mark.value - min) / (max - min)) * 100;
                        const isActive = mark.value <= value;
                        return (
                            <div
                                key={mark.value}
                                className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2"
                                style={{ left: `${markPercentage}%` }}
                            >
                                <div
                                    className={cc(
                                        "w-2 h-2 rounded-full border-2 border-white dark:border-slate-900 transition-colors",
                                        isActive 
                                            ? "bg-violet-500 dark:bg-violet-600" 
                                            : "bg-slate-300 dark:bg-slate-600"
                                    )}
                                />
                            </div>
                        );
                    })}
                    
                    {/* Thumb */}
                    <div
                        className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 transition-all"
                        style={{ left: `${percentage}%` }}
                    >
                        <div
                            role="slider"
                            aria-valuemin={min}
                            aria-valuemax={max}
                            aria-valuenow={value}
                            aria-disabled={disabled}
                            tabIndex={disabled ? -1 : 0}
                            onKeyDown={handleKeyDown}
                            className={cc(
                                "w-5 h-5 rounded-full bg-white shadow-md ring-2 ring-violet-500 dark:ring-violet-600 transition-transform",
                                !disabled && "hover:scale-110 focus:outline-none focus:ring-4 focus:ring-violet-500/30 dark:focus:ring-violet-600/30",
                                isDragging && "scale-110",
                                disabled && "opacity-50 cursor-not-allowed"
                            )}
                        />
                    </div>
                </div>

                {/* Mark labels */}
                {marks.length > 0 && (
                    <div className="relative mt-2">
                        {marks.map((mark) => {
                            const markPercentage = ((mark.value - min) / (max - min)) * 100;
                            return (
                                <div
                                    key={mark.value}
                                    className="absolute -translate-x-1/2"
                                    style={{ left: `${markPercentage}%` }}
                                >
                                    <span className="text-xs text-slate-600 dark:text-slate-400 inline-block">
                                        {mark.label}
                                    </span>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
}
