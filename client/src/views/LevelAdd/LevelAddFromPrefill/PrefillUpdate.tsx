import { LevelCard } from "@cafe/components/LevelCard/LevelCard";
import { Shell } from "@cafe/components/Shell";
import { Alert } from "@cafe/components/ui/Alert";
import { Button } from "@cafe/components/ui/Button";
import { Surface } from "@cafe/components/ui/Surface";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Words } from "@cafe/components/ui/Words";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { RDLevelPrefillUpdateReady } from "@cafe/types/rdLevelPrefill";
import { useState } from "react";

type PrefillUpdateProps = {
  prefill: RDLevelPrefillUpdateReady;
  potentialMatches: RDLevel[];
};

export function PrefillUpdate({ potentialMatches }: PrefillUpdateProps) {
  const [levelId, setLevelId] = useState<string>("");
  const csrfInput = useCSRFTokenInput();
  return (
    <Shell>
      <div className="p-4 flex flex-col gap-4">
        <Alert variant="info">
          <Words as="p" className="mb-2">Select the level this rdzip is updating.</Words>
          <Words as="p" className="mb-2">There are two ways you can do this.</Words>
          <ul className="list-disc list-inside space-y-1 mb-2">
            <li>
              <Words>
                If you know the level ID of the old level, enter it into the
                "Level ID" input field and Submit.
              </Words>
            </li>
            <li>
              <Words>
                We have also guessed potential levels for your rdzip in the
                "Potential Matches" section below. If your level is there, you
                can click it, then click Submit.
              </Words>
            </li>
          </ul>
          <Words as="p">
            If the level does not appear in Potential Matches, please search for
            the level to find the level ID to update.
          </Words>
        </Alert>
        <Surface className="self-start px-4 pb-4">    
          <Form method="POST" className="mt-4">
            {csrfInput}
            <div className="flex items-end gap-2">
              <TextInput
                label="Level ID"
                placeholder="Enter level ID"
                value={levelId}
                onChange={(e) => setLevelId(e.currentTarget.value)}
                name="prefill"
              />
              <Button disabled={!levelId} type="submit" variant="primary">
                Submit
              </Button>
            </div>
          </Form>
        </Surface>
        <Words as="h3" variant="subheader" className="mt-4 mb-2">
          Potential Matches
        </Words>
        {potentialMatches.length === 0 && (
          <Words>No potential matches found.</Words>
        )}
        {potentialMatches.length > 0 && (
          <ul className="space-y-2">
            {potentialMatches.map((match) => (
              <LevelCard
                key={match.id}
                level={match}
                showId={true}
                onClick={() => setLevelId(match.id)}
              />
            ))}
          </ul>
        )}
      </div>
    </Shell>
  );
}
