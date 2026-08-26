import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "./ProfileNavbar";

import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { useUser } from "@cafe/hooks/useUser";
import { Form } from "@cafe/minibridge/components/Form";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { TextInput } from "@cafe/components/ui/TextInput";
import Select from "@cafe/components/ui/Select";
import { Button } from "@cafe/components/ui/Button";
import { Checkbox } from "@cafe/components/ui/Checkbox";
import { useState } from "react";
import { Link } from "@cafe/minibridge/components/Link";
import { useAsync, AsyncState } from "@cafe/hooks/useAsync";
import { CAFE_LINK_STATUS_URL } from "@cafe/utils/rddirect";

const CAFE_MOD_INSTALLATION_INSTRUCTIONS_URL = "https://github.com/auburnsummer/orchard2/wiki/CafeLink-Installation-Instructions";

type ConnectionTestResponse = {
  status: "ok" | "starting" | "busy";
}

async function doConnectionTest(): Promise<ConnectionTestResponse> {
  const response = await fetch(CAFE_LINK_STATUS_URL);
  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
  }
  console.log(response);
  return await response.json();
}

function connectionTestDisplay(testResult: AsyncState<ConnectionTestResponse>) {
  if (testResult.status === "idle") {
    return null;
  }
  if (testResult.status === "pending") {
    return <Words variant="muted" className="text-sm">PENDING</Words>;
  }
  if (testResult.status === "success") {
    if (testResult.data.status === "ok") {
      return <Words variant="muted" className="text-sm">SUCCESS</Words>;
    }
    if (testResult.data.status === "starting") {
      return <Words variant="muted" className="text-sm">STARTING</Words>;
    }
    if (testResult.data.status === "busy") {
      return <Words variant="muted" className="text-sm">BUSY</Words>;
    }
  }
  if (testResult.status === "error") {
    return <Words variant="muted" className="text-sm">ERROR: {testResult.error.message}</Words>;
  }
  return null;
}

export function ProfileSettingsView() {
  const user = useUser();
  const input = useCSRFTokenInput();

  const [showRdDirect, setShowRdDirect] = useState(user.show_rddirect);

  const [testResult, startTest] = useAsync(doConnectionTest);

  return (
    <Shell navbar={user.authenticated && <ProfileNavbar />}>
      <title>Settings | Rhythm Café</title>
      <Surface className="m-3 p-6 flex-grow">
        <Words as="h2" variant="header">Settings</Words>
        <Form className="pt-2" method="post">
          {input}
          <div className="flex flex-col gap-2">
            {
              user.authenticated && (
                <TextInput
                  name="display_name"
                  label="Display name"
                  maxLength={150}
                  defaultValue={user.displayName}
                  className="max-w-64"
                />
              )
            }
            <Select
              label="Theme"
              className="max-w-64"
              allowDeselect={false}
              defaultValue={user.theme_preference}
              name="theme_preference"
              data={[
                {
                  label: "Light",
                  value: "light",
                },
                {
                  label: "Dark",
                  value: "dark",
                },
                {
                  label: "Use system default",
                  value: "system",
                }
              ]}
            />
            <Select
              label="Default peer review search filter"
              className="max-w-64"
              allowDeselect={false}
              defaultValue={user.default_pr_preference}
              name="default_pr_preference"
              data={[
                {
                  label: "Approved levels only",
                  value: "approved",
                },
                {
                  label: "Pending levels only",
                  value: "pending",
                },
                {
                  label: "Rejected levels only",
                  value: "rejected",
                },
                {
                  label: "All levels",
                  value: "all",
                }
              ]}
            />
            <div className="flex flex-row items-end gap-2">
            <Checkbox
              className="mt-4"
              name="show_rddirect"
              label="Show direct play links"
              description={
                <>
                  <Words variant="muted">
                    For the links to work you need to install a Rhythm Doctor mod. See <Link href={CAFE_MOD_INSTALLATION_INSTRUCTIONS_URL} target="_blank" rel="noopener noreferrer" className="underline">installation instructions</Link>.
                  </Words>
                </>
              }
              checked={showRdDirect}
              onChange={(e) => setShowRdDirect(e.target.checked)}
              showDescriptionAsTooltip={false}
            />

            {
              showRdDirect && (
                <Button className="max-w-48 ml-1" variant="default" onClick={startTest} type="button">Test Connection</Button>
              )
            }

            {
              showRdDirect && connectionTestDisplay(testResult)
            }

            </div>

            <Button type="submit" variant="primary" className="max-w-48 py-2 mt-4">Save</Button>
          </div>
        </Form>
        {
          !user.authenticated && (
            <div className="mt-8">
              <Words variant="muted" className="text-sm">
                Note: when you are not logged in, settings are saved in a cookie.
              </Words>
            </div>
          )
        }
      </Surface>
    </Shell>
  );
}
