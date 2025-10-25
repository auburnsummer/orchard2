import { Checkbox } from "@cafe/components/ui/Checkbox";
import { NumberInput } from "@cafe/components/ui/NumberInput";
import { Words } from "@cafe/components/ui/Words";

import { useState } from "react";
import { useSearchParams } from "@cafe/minibridge/hooks";
import { Button } from "@cafe/components/ui/Button";

export function BPMSelect() {
  const [searchParams, navigateViaSearchParams] = useSearchParams();

  const minBpmS = searchParams.get("min_bpm");
  const maxBpmS = searchParams.get("max_bpm");
  const minBpm = minBpmS ? parseInt(minBpmS, 10) : 20;
  const maxBpm = maxBpmS ? parseInt(maxBpmS, 10) : 400;

  const [minBpmValue, setMinBpmValue] = useState(minBpm);
  const [maxBpmValue, setMaxBpmValue] = useState(maxBpm);

  const [isEnabled, setIsEnabled] = useState(
    minBpmS !== null || maxBpmS !== null,
  );

  return (
    <div>
      <div className="flex items-center gap-2 mb-2">
        <Words variant="label">
          BPM
        </Words>
        <Checkbox
          onChange={(event) => {
            const checked = event.currentTarget.checked;
            setIsEnabled(checked);
            if (!checked) {
              navigateViaSearchParams((params) => {
                params.delete("min_bpm");
                params.delete("max_bpm");
              });
            }
          }}
          checked={isEnabled}
          label={<Words variant="xs">Enable filter</Words>}
        />
      </div>

      <div className="flex gap-2 pr-8 mt-2 items-end">
        <NumberInput
          label="Min"
          value={minBpmValue}
          min={20}
          max={400}
          step={1}
          disabled={!isEnabled}
          onChange={v => v && setMinBpmValue(v)}
          className="flex-1"
        />
        <NumberInput
          label="Max"
          value={maxBpmValue}
          min={20}
          max={400}
          step={1}
          disabled={!isEnabled}
          onChange={v => v && setMaxBpmValue(v)}
          className="flex-1"
        />
        <Button 
          className="h-9"
          onClick={() => {
            navigateViaSearchParams(params => {
              params.set("min_bpm", `${minBpmValue}`);
              params.set("max_bpm", `${maxBpmValue}`);
            })
          }}
        >
          Go
        </Button>
      </div>
    </div>
  );
}
