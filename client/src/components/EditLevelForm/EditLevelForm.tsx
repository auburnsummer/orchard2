import { RDLevel } from "@cafe/types/rdLevelBase";
import { atom, useAtom } from "jotai";
import { useRef, useState } from "react";
import { withImmer } from "jotai-immer";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Shell } from "../Shell";

import commonStyles from "@cafe/theme/commonPatterns.module.css";
import styles from "./EditLevelForm.module.css";

import cc from "clsx";

import { LevelCard } from "../LevelCard/LevelCard";
import { Form } from "@cafe/minibridge/components/Form";
import { Button } from "../ui/Button";
import { TextInput } from "../ui/TextInput";
import Fieldset from "../ui/Fieldset";
import { Surface } from "../ui/Surface";
import Textarea from "../ui/Textarea";
import { TagInput } from "../ui/TagInput";

const CHECKBOXES = [
  ["single_player", "Single Player"],
  ["two_player", "Two Player"],
  ["seizure_warning", "Seizure Warning"],
  ["has_classics", "Has classic beats"],
  ["has_oneshots", "Has Oneshots"],
  ["has_squareshots", "Has Squareshots"],
  ["has_freezeshots", "Has Freezeshots"],
  ["has_freetimes", "Has Freetimes"],
  ["has_holds", "Has Holds"],
  ["has_skipshots", "Skipshots"],
  ["has_window_dance", "Has Window Dance"],
] as const;

type EditLevelFormProps = {
  level: RDLevel;
  preamble: React.ReactNode;
  submitButtonText: string;
  // form submit url
  // preamble html element to go before the form
};

function PrefillPreview({ level }: { level: RDLevel }) {
  return (
    <div className={cc("flex items-center justify-center flex-grow p-2", commonStyles.paperBg)}>
      <LevelCard level={level} className={styles.preview} />
    </div>
  );
}

export function EditLevelForm({
  level: initialLevel,
  preamble,
  submitButtonText,
}: EditLevelFormProps) {
  const levelAtom = useRef(withImmer(atom(initialLevel)));
  const csrfInput = useCSRFTokenInput();
  const [level, setLevel] = useAtom(levelAtom.current);
  const [bpmSync, setBpmSync] = useState(false);

  return (
    <Shell aside={<PrefillPreview level={level} />}>
      <Surface className="flex flex-col gap-4 m-4">
        {preamble}
        <div className="mx-4">
          <div className="flex justify-between">
            <Button onClick={(_) => setLevel(initialLevel)} variant="default">Reset</Button>
            {/* the addlevel button is a secret form.
                because the level format is a bit complex,
                we have a hidden input with the edited prefill as json which is what gets submitted
            */}
            <Form method="POST">
              {csrfInput}
              <input type="hidden" name="prefill" value={JSON.stringify(level)} />
              <Button type="submit" variant="primary">{submitButtonText}</Button>
            </Form>
          </div>
          <div className="flex flex-row flex-wrap gap-4 pt-4">
            <TextInput
              label="Song Name"
              onChange={(e) =>
                setLevel((l) => {
                  l.song = e.target.value;
                })
              }
              value={level.song}
            ></TextInput>
            <TextInput
              label="Song Name (alternate)"
              value={level.song_alt}
              onChange={(e) =>
                setLevel((l) => {
                  l.song_alt = e.target.value;
                })
              }
              description="Alternate name of the song, such as a localised or romanized name."
            />
          </div>
          <Textarea
            label="Description"
            description="Note: <color> tags are not supported. Any <color> tags have been removed."
            value={level.description}
            onChange={(e) =>
              setLevel((l) => {
                l.description = e.target.value;
              })
            }
          />
          <TagInput
            legend="Artists"
            values={level.artist_tokens}
            onChange={(values) =>
              setLevel((l) => {
                if (values.length > 0) {
                  l.artist_tokens = values;
                }
              })
            }
            inputLabelFunc={(index) => `Artist ${index + 1}`}
          />
          {/* <TagsInput
            label="Artists"
            description="Press [Enter] after typing to add an artist."
            value={level.artist_tokens}
            splitChars={[]}
            onChange={(values) =>
              setLevel((l) => {
                if (values.length > 0) {
                  l.artist_tokens = values;
                }
              })
            }
          /> */}
          {/* <Fieldset legend="BPM">
            <Group align="end">
              <NumberInput
                label="Min BPM"
                value={level.min_bpm}
                min={0}
                max={bpmSync ? 1000 : level.max_bpm}
                onChange={(value) =>
                  setLevel((l) => {
                    if (typeof value === "number") {
                      l.min_bpm = value;
                      if (bpmSync) {
                        l.max_bpm = value;
                      }
                    }
                  })
                }
              />
              <NumberInput
                label="Max BPM"
                value={level.max_bpm}
                min={bpmSync ? 0 : level.min_bpm}
                max={1000}
                onChange={(value) =>
                  setLevel((l) => {
                    if (typeof value === "number") {
                      l.max_bpm = value;
                      if (bpmSync) {
                        l.min_bpm = value;
                      }
                    }
                  })
                }
              />
              <Switch
                checked={bpmSync}
                onChange={(event) => setBpmSync(event.currentTarget.checked)}
                label="Sync BPM inputs"
              ></Switch>
            </Group>
          </Fieldset>
          <Fieldset legend="Difficulty" pb="xl">
            <Slider
              label={null}
              step={0.001}
              w={300}
              min={0}
              max={3}
              value={level.difficulty}
              onChange={(value) =>
                setLevel((l) => {
                  l.difficulty = value;
                })
              }
              restrictToMarks={true}
              marks={[
                { value: 0, label: "Easy" },
                { value: 1, label: "Medium" },
                { value: 2, label: "Tough" },
                { value: 3, label: "Very Tough" },
              ]}
            />
          </Fieldset>
          <TagsInput
            label="Tags"
            description="Press [Enter] after typing to add an tag."
            value={level.tags}
            splitChars={[]}
            onChange={(values) =>
              setLevel((l) => {
                if (values.length > 0) {
                  l.tags = values;
                }
              })
            }
          />
          <Fieldset p="md">
            <Grid justify="flex-start" align="flex-start">
              {CHECKBOXES.map(([key, label]) => {
                return (
                  <Grid.Col span={4}>
                    <Checkbox
                      checked={level[key]}
                      label={label}
                      onChange={(e) =>
                        setLevel((l) => {
                          l[key] = e.target.checked;
                        })
                      }
                    />
                  </Grid.Col>
                );
              })}
            </Grid>
          </Fieldset> */}
        </div>
      </Surface>
    </Shell>
  );
}
