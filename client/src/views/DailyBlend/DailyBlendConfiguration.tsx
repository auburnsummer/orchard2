import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { Form } from "@cafe/minibridge/components/Form";
import Textarea from "@cafe/components/ui/Textarea";
import { Button } from "@cafe/components/ui/Button";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

import jsonata from "jsonata";
import { useEffect, useMemo, useState } from "react";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Alert } from "@cafe/components/ui/Alert";

function unicodeToBase64(str: string): string {
  const utf8Bytes = new TextEncoder().encode(str);
  const binaryString = String.fromCharCode(...utf8Bytes);
  return btoa(binaryString);
}

type DailyBlendConfigurationProps = {
  config: {
    webhook_urls: string;
    jsonata_script: string;
  };
};

type JsonataResult = {
    state: "error",
    error: any
} | {
    state: "success",
    result: any
} | {
    state: "idle"
}

const EXAMPLE_LEVEL: RDLevel = {
  id: "r2JqHpm3",
  artist: "auburnsummer",
  artist_tokens: ["auburnsummer"],
  artist_raw: "auburnsummer",
  song: "test level 2",
  song_alt: "Bossa Fight",
  song_raw: "test level 2",
  seizure_warning: false,
  description: "This is another test level for the peer review system.",
  hue: 0.63,
  authors: ["auburnsummer"],
  authors_raw: "auburnsummer",
  max_bpm: 133,
  min_bpm: 133,
  difficulty: 0,
  single_player: true,
  two_player: false,
  last_updated: "2025-12-20T00:57:24+00:00",
  tags: ["test"],
  sha1: "0787968a624e21e7c2703a2f897b6ff46bcc5f09",
  rdlevel_sha1: "1648472309ee6d1cd098ef1508eb54d386185279",
  rd_md5: "9e74b3a1cad0aec6b2706289de4ec80d",
  is_animated: false,
  rdzip_url:
    "https://c2.rhythm.cafe/rdzips/ginseng/78/7968a624e21e7c2703a2f897b6ff46bcc5f09.rdzip",
  image_url:
    "https://c2.rhythm.cafe/images/chai/13/e1456232d6a06aa60ead1c1389861bf60e132.png",
  thumb_url:
    "https://c2.rhythm.cafe/thumbs/oolong/4a/312cf5c59710a354b700cd70aaeb803b635f3.webp",
  icon_url:
    "https://c2.rhythm.cafe/icons/jasmine/01/21c0ad376aea7bafc39e45fff0476bc38fdc4.png",
  submitter: {
    id: "uH5kdCcc",
    displayName: "auburn",
    avatarURL:
      "https://cdn.discordapp.com/avatars/297727909609603083/a8bcbcca3023d96ecdfa68be0f5a3d75.png",
  },
  club: { id: "cpharmacy", name: "Peer Reviewers" },
  approval: 0,
  is_private: false,
};

export function DailyBlendConfiguration({
  config,
}: DailyBlendConfigurationProps) {
  const csrfInput = useCSRFTokenInput();

  const [jsonataScript, setJsonataScript] = useState(config.jsonata_script);

  const [jsonataResult, setJsonataResult] = useState<JsonataResult>({state: "idle"});

  useEffect(() => {
    (async () => {
        try {
        const exec = jsonata(jsonataScript);
        const result = await exec.evaluate(EXAMPLE_LEVEL);
            setJsonataResult({state: "success", result});
        } catch (e) {
            setJsonataResult({state: "error", error: e});
        }
    })();
  }, [jsonataScript]);

  const previewData = useMemo(() => {
    if (jsonataResult.state !== "success") {
        return null;
    }
    const preview = {
        "version": "d2",
        "messages": [
            {
                "id": "1",
                "data": jsonataResult.result
            }
        ]
    }
    return unicodeToBase64(JSON.stringify(preview));
  }, [jsonataResult]);

  return (
    <Shell navbar={<DailyBlendNavbar />}>
      <Surface className="m-3 p-4">
        <Words variant="header" className="mb-4">
          Daily Blend Configuration
        </Words>
        <Form method="POST">
          {csrfInput}
          <Textarea
            name="webhook_urls"
            label="Webhook URLs (one per line)"
            rows={5}
            defaultValue={config.webhook_urls}
          />
          <Textarea
            className="font-mono"
            value={jsonataScript}
            onChange={(e) => setJsonataScript(e.target.value)}
            name="jsonata_script"
            label="JSONata Script"
            rows={15}
          />
          <Button
            type="button"
            onClick={() => {
                navigator.clipboard.writeText(JSON.stringify(EXAMPLE_LEVEL, null, 2));
            }}
          >
            Copy example JSON to Clipboard
          </Button>
          {
            jsonataResult.state === "idle" ? null : jsonataResult.state === "error" ? (
              <Alert variant="error" className="mt-4">
                <strong>Error:</strong> {JSON.stringify({...jsonataResult.error, "stack": undefined}, null, 2)}
              </Alert>
            ) : (
              <iframe
                src={`https://discohook.app/viewer?header=false&data=${previewData}`}
              >

              </iframe>
            )
          }

          <Button type="submit" className="mt-4">
            Save Configuration
          </Button>
        </Form>
      </Surface>
    </Shell>
  );
}
