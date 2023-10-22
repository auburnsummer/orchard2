import { WithClass } from "@orchard/utils/withClass";
import { IconButton, Input, Tag } from "..";

import cc from "clsx";
import { useCallback, useEffect, useMemo, useRef, useState } from "preact/hooks";

import "./TagInput.css";
import { type SlInput } from "@shoelace-style/shoelace";


type TagInputProps = WithClass & {
    items: string[],
    onItems: (items: string[]) => void,
    commaSubmits: boolean,
    validationMessage?: string,
    inputProps?: Parameters<typeof Input>[0]
}

export function TagInput({
    "class": _class,
    items, onItems,
    commaSubmits,
    validationMessage = '',
    inputProps = {}
}: TagInputProps) {
    const [value, setValue] = useState("");

    const prefix = useMemo(() => {
        return (
            <span slot="prefix" class="ti_tags">
                {
                    items.map((item, i) => (
                        <Tag
                            variant="primary"
                            size={"medium" as any}
                            removable
                            class="ti_tag"
                            onSlRemove={() => {
                                const itemsCopy = items.slice();
                                itemsCopy.splice(i, 1);
                                onItems(itemsCopy);
                            }}
                        >
                            {item}
                        </Tag>
                    ))
                }
            </span>
        )
    }, [items]);

    const newTagCut = useCallback(() => {
        if (value !== "") {
            onItems([...items, value]);
            setValue("");
        }
    }, [items, onItems, value, setValue]);

    const onKeyDown = useCallback((e: KeyboardEvent) => {
        if (e.key === "Enter" || (commaSubmits && e.key === ",")) {
            newTagCut();
            e.preventDefault();
        }
        if (e.key === "Backspace" && value === "") {
            onItems(items.slice(0, -1));
        }
    }, [items, onItems, value, newTagCut]);

    const inputRef = useRef<SlInput>(null);

    useEffect(() => {
        if (inputRef.current) {
            inputRef.current.setCustomValidity(validationMessage);
        }
    }, [validationMessage])

    return (
        <Input
            {...inputProps}
            class={cc(_class, inputProps.class, inputProps.className, "ti")} 
            size={inputProps.size || 'medium' as any}
            value={value}
            onSlInput={e => setValue(e.target.value)}
            onKeyDown={onKeyDown}
            ref={inputRef}
        >
            {prefix}
            <IconButton
                slot="suffix"
                name="plus-circle-dotted"
                label="add tag"
                onClick={newTagCut}
                class="ti_add-button"
            />
        </Input>
    )
}