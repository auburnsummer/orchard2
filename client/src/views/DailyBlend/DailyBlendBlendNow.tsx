import { Shell } from "@cafe/components/Shell";
import { Words } from "@cafe/components/ui/Words";
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { Form } from "@cafe/minibridge/components/Form";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

export function DailyBlendBlendNow() {
    const csrfInput = useCSRFTokenInput();

    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <div className="flex flex-col items-center justify-center min-h-[70vh] p-8">
                <Words variant="header" className="mb-8 text-center text-3xl tracking-wider uppercase text-red-500 animate-pulse">
                    DAILY BLEND CONTROL PANEL
                </Words>
                
                {/* The Console/Table Surface */}
                <div 
                    className="relative"
                    style={{
                        perspective: "800px",
                    }}
                >
                    {/* Table top surface with perspective */}
                    <div 
                        className="relative bg-gradient-to-b from-zinc-700 via-zinc-800 to-zinc-900 rounded-xl p-12 border-4 border-zinc-600"
                        style={{
                            transform: "rotateX(15deg)",
                            boxShadow: `
                                0 20px 40px rgba(0,0,0,0.5),
                                inset 0 2px 0 rgba(255,255,255,0.1),
                                inset 0 -2px 0 rgba(0,0,0,0.3)
                            `,
                        }}
                    >
                        {/* Warning stripes border */}
                        <div 
                            className="absolute inset-4 rounded-lg pointer-events-none"
                            style={{
                                background: `repeating-linear-gradient(
                                    45deg,
                                    #facc15,
                                    #facc15 10px,
                                    #1a1a1a 10px,
                                    #1a1a1a 20px
                                )`,
                                padding: "4px",
                                WebkitMask: "linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)",
                                WebkitMaskComposite: "xor",
                                maskComposite: "exclude",
                            }}
                        />
                        
                        {/* Button housing/socket */}
                        <div 
                            className="relative w-48 h-48 rounded-full bg-zinc-900 mx-auto flex items-center justify-center"
                            style={{
                                boxShadow: `
                                    inset 0 8px 16px rgba(0,0,0,0.8),
                                    inset 0 -2px 4px rgba(255,255,255,0.05),
                                    0 0 0 8px #3f3f46,
                                    0 0 0 12px #27272a
                                `,
                            }}
                        >
                            {/* The actual button */}
                            <Form method="POST" className="relative">
                                {csrfInput}
                                <button 
                                    type="submit"
                                    className="
                                        relative w-36 h-36 rounded-full
                                        font-black text-xl text-white uppercase tracking-widest
                                        transition-all duration-100 ease-out
                                        hover:brightness-110
                                        active:translate-y-2
                                        focus:outline-none focus:ring-4 focus:ring-red-400 focus:ring-opacity-50
                                        cursor-pointer
                                        group
                                    "
                                    style={{
                                        background: `
                                            radial-gradient(ellipse at 30% 20%, #ff6b6b 0%, transparent 50%),
                                            radial-gradient(ellipse at 70% 80%, #7f1d1d 0%, transparent 50%),
                                            linear-gradient(180deg, #ef4444 0%, #b91c1c 50%, #7f1d1d 100%)
                                        `,
                                        boxShadow: `
                                            0 8px 0 #5c0a0a,
                                            0 10px 10px rgba(0,0,0,0.5),
                                            0 0 30px rgba(239, 68, 68, 0.4),
                                            inset 0 -4px 8px rgba(0,0,0,0.3),
                                            inset 0 4px 8px rgba(255,255,255,0.2)
                                        `,
                                        textShadow: "0 2px 4px rgba(0,0,0,0.5)",
                                    }}
                                >
                                    <span className="relative z-10">
                                        B L E N D
                                    </span>
                                    
                                    {/* Glowing ring effect */}
                                    <div 
                                        className="absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                                        style={{
                                            boxShadow: "0 0 40px 10px rgba(239, 68, 68, 0.6)",
                                        }}
                                    />
                                </button>
                            </Form>
                        </div>
                        
                        {/* Small indicator lights */}
                        <div className="flex justify-center gap-4 mt-8">
                            <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" style={{ boxShadow: "0 0 10px #22c55e" }} />
                            <div className="w-3 h-3 rounded-full bg-yellow-500" style={{ boxShadow: "0 0 10px #eab308" }} />
                            <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" style={{ boxShadow: "0 0 10px #22c55e" }} />
                        </div>
                    </div>
                    
                    {/* Table edge/thickness */}
                    <div 
                        className="absolute left-0 right-0 h-8 bg-gradient-to-b from-zinc-800 to-zinc-950 rounded-b-xl"
                        style={{
                            transform: "rotateX(15deg) translateY(-4px)",
                            boxShadow: "0 10px 30px rgba(0,0,0,0.5)",
                        }}
                    />
                </div>
                
                {/* Warning text */}
                <p className="mt-12 text-zinc-500 text-sm text-center max-w-md">
                    AUTHORIZED PERSONNEL ONLY<br/>
                    <span className="text-xs">This action will immediately trigger THE DAILY BLEND.</span>
                </p>
            </div>
        </Shell>
    )
}