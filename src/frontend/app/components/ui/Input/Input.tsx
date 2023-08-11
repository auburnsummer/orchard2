import { forwardRef } from "react";
import cc from "clsx";

import "./Input.css";

type InputProps = React.ComponentPropsWithoutRef<"input"> 

export const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
    return (
        <input ref={ref} {...props} className={cc("ui", props.className)}/>
    )
})