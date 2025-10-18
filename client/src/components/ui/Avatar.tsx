import { ImgHTMLAttributes } from "react";

import cc from "clsx";

type AvatarProps = ImgHTMLAttributes<HTMLImageElement> & {
    username?: string;
};

export function Avatar({ username, className, src, ...props }: AvatarProps) {
    return (
        <img
            src={
                src ||
            `https://www.gravatar.com/avatar/?d=initials&name=${encodeURIComponent(username || "Unknown User")}`
            }
            alt="User avatar"
            className={cc("m-1 h-10 w-10 rounded-full border-2 border-slate-50", className)}
            {...props}
        />
    )
}