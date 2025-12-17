import { createContext, useContext, useState, ReactNode, CSSProperties } from 'react';

interface TooltipPosition {
  top: number;
  left: number;
}

interface TooltipContextValue {
  description: string;
  position: TooltipPosition;
  show: (description: string, element: HTMLElement) => void;
  hide: () => void;
}

const TooltipContext = createContext<TooltipContextValue | null>(null);

export function TooltipProvider({ children }: { children: ReactNode }) {
  const [description, setDescription] = useState('');
  const [position, setPosition] = useState<TooltipPosition>({ top: 0, left: 0 });

  const show = (desc: string, element: HTMLElement) => {
    const rect = element.getBoundingClientRect();
    setDescription(desc);
    setPosition({
      top: rect.bottom + window.scrollY + 8, // 8px offset below the element
      left: rect.left + window.scrollX, // Align with the left edge
    });
  };

  const hide = () => {
    setDescription('');
    setPosition({ top: 0, left: 0 });
  };

  return (
    <TooltipContext.Provider value={{ description, position, show, hide }}>
      {children}
      {description && (
        <div
          style={{
            position: 'fixed',
            top: `${position.top}px`,
            left: `${position.left}px`,
            pointerEvents: 'none',
            maxWidth: '16rem',
            wordWrap: 'break-word',
            zIndex: 9999,
            boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
          } as CSSProperties}
          className="bg-gray-600 dark:bg-gray-700 text-white text-xs p-2"
        >
          {description}
        </div>
      )}
    </TooltipContext.Provider>
  );
}

export function useTooltip() {
  const context = useContext(TooltipContext);
  if (!context) {
    throw new Error('useTooltip must be used within a TooltipProvider');
  }
  return context;
}
