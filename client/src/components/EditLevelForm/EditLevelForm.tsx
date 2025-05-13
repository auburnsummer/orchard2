import { RDLevel } from "@cafe/types/rdLevelBase";
import { atom, useAtom } from "jotai";
import { useRef, useState } from "react";
import { withImmer } from "jotai-immer";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Shell } from "../Shell";

type EditLevelFormProps = {
    level: RDLevel;
    // form submit url
    // preamble html element to go before the form
}

export function EditLevelForm({level: initialLevel}: EditLevelFormProps) {
    const levelAtom = useRef(
        withImmer(
            atom(
                initialLevel
            )
        )
    );
    const csrfInput = useCSRFTokenInput();
    const [level, setLevel] = useAtom(levelAtom.current);
    const [bpmSync, setBpmSync] = useState(false);

    return (
        <Shell
        >
            <p>ayayaya</p>
        </Shell>
    )
}