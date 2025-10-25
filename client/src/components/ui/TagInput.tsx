import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Fieldset from "./Fieldset";
import { TextInput } from "./TextInput";
import { faPlus, faXmark } from "@fortawesome/free-solid-svg-icons";
import { Button } from "./Button";
import { useState, useEffect, useRef } from "react";

type TagInputProps = {
  legend: string;
  values: string[];
  onChange: (values: string[]) => void;
  allowBlank?: boolean;
};

export function TagInput({ legend, values, onChange, allowBlank = true }: TagInputProps) {
  // Internal state tracks all values including blanks
  const [internalValues, setInternalValues] = useState<string[]>(values);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);
  
  // Sync internal state when external values change (but don't overwrite if we have blanks)
  useEffect(() => {
    // Only sync if external values differ from our filtered output
    const filtered = allowBlank ? internalValues : internalValues.filter((v) => v.trim() !== "");
    if (JSON.stringify(filtered) !== JSON.stringify(values)) {
      setInternalValues(values);
    }
  }, [values, allowBlank, internalValues]);
  
  const hasBlankValues = !allowBlank && internalValues.some((v) => v.trim() === "");

  const emitChanges = (newValues: string[]) => {
    setInternalValues(newValues);
    const filtered = allowBlank ? newValues : newValues.filter((v) => v.trim() !== "");
    onChange(filtered);
  };

  return (
    <Fieldset legend={legend}>
      <div className="flex flex-row flex-wrap gap-3">
        {internalValues.map((value, index) => (
          <TextInput
            className="w-40"
            key={index}
            value={value}
            ref={(el) => {
              inputRefs.current[index] = el;
            }}
            onChange={(e) => {
              const newValues = [...internalValues];
              newValues[index] = e.target.value;
              emitChanges(newValues);
            }}
            onKeyDown={(e) => {
              if (e.key === "Backspace" && value === "") {
                if (internalValues.length > 1) {
                  const newValues = internalValues.filter((_, i) => i !== index);
                  emitChanges(newValues);
                  // Focus the previous input if it exists
                  if (index > 0) {
                    setTimeout(() => {
                      inputRefs.current[index - 1]?.focus();
                    }, 0);
                  }
                }
                e.preventDefault();
              }
            }}
            rightSlot={
              internalValues.length > 1 ? (
                <button
                  type="button"
                  className="text-slate-500 hover:text-slate-700 pr-2 pt-0.5 disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={() => {
                    const newValues = internalValues.filter((_, i) => i !== index);
                    emitChanges(newValues);
                  }}
                  disabled={
                    internalValues.filter((v) => v.trim() !== "").length === 1 &&
                    !allowBlank &&
                    value.trim() !== ""
                  }
                >
                  <FontAwesomeIcon icon={faXmark} />
                </button>
              ) : null
            }
          />
        ))}
        <Button
          type="button"
          variant="secondary"
          className="mt-2"
          onClick={() => {
            emitChanges([...internalValues, ""]);
          }}
          disabled={hasBlankValues}
        >
          <FontAwesomeIcon icon={faPlus} />
        </Button>
      </div>
    </Fieldset>
  );
}
