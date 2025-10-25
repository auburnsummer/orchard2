import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Fieldset from "./Fieldset";
import { TextInput } from "./TextInput";
import { faPlus, faXmark } from "@fortawesome/free-solid-svg-icons";
import { Button } from "./Button";

type TagInputProps = {
  legend: string;
  values: string[];
  onChange: (values: string[]) => void;
};

export function TagInput({ legend, values, onChange }: TagInputProps) {
  return (
    <Fieldset legend={legend}>
      <div className="flex flex-row flex-wrap">
        {values.map((value, index) => (
          <TextInput
            className="w-32"
            key={index}
            value={value}
            onChange={(e) => {
              const newValues = [...values];
              newValues[index] = e.target.value;
              onChange(newValues);
            }}
            rightSlot={
              values.length > 1 ? (
                <button
                  type="button"
                  className="text-red-500 hover:text-red-700"
                  onClick={() => {
                    const newValues = values.filter((_, i) => i !== index);
                    onChange(newValues);
                  }}
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
            onChange([...values, ""]);
          }}
        >
          <FontAwesomeIcon icon={faPlus} />
        </Button>
      </div>
    </Fieldset>
  );
}
