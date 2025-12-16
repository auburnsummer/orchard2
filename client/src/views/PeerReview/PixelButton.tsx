import cc from "clsx";
import "./pixelFont.css";

type PixelButtonProps = {
    variant: 'pr' | 'nr' | 'pd';
    children: React.ReactNode;
    onClick?: () => void;
    className?: string;
};

export function PixelButton({ variant, children, onClick, className }: PixelButtonProps) {
    const textColor = variant === 'pd' ? 'black' : 'white';

    return (
        <div className={cc("pixel-button-wrapper", className)}>
            <button
                type="button"
                className={cc("status-button-display", variant)}
                style={{ 
                    fontFamily: "Pixel-Font, 'Courier New', monospace", 
                    color: textColor 
                }}
                onClick={onClick}
            >
                {children}
            </button>
            <div className="pixel-outline">
                <div className="side left" style={{ backgroundColor: '#e2e2e2' }}></div>
                <div className="side right" style={{ backgroundColor: '#e2e2e2' }}></div>
                <div className="corner-dot tl" style={{ backgroundColor: '#e2e2e2' }}></div>
                <div className="corner-dot tr" style={{ backgroundColor: '#e2e2e2' }}></div>
                <div className="corner-dot bl" style={{ backgroundColor: '#e2e2e2' }}></div>
                <div className="corner-dot br" style={{ backgroundColor: '#e2e2e2' }}></div>
            </div>
        </div>
    );
}
