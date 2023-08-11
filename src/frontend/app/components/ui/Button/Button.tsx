import { forwardRef } from "react";
import cc from "clsx";
import "./Button.css";

type ButtonProps = React.ComponentPropsWithoutRef<"button"> 

export const Button = forwardRef<HTMLButtonElement, ButtonProps>((props, ref) => {
    return (
        <button ref={ref} {...props} className={cc("ub", props.className)} />
    )
})