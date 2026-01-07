import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { Form } from "@cafe/minibridge/components/Form";
import Textarea from "@cafe/components/ui/Textarea";
import { Button } from "@cafe/components/ui/Button";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";

type DailyBlendConfigurationProps = {
    config: {
        webhook_urls: string;
        jsonata_script: string;
    }
}

export function DailyBlendConfiguration({ config }: DailyBlendConfigurationProps) {
    const csrfInput = useCSRFTokenInput();
    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <Surface className="m-3 p-4">
                <Words variant="header" className="mb-4">
                    Daily Blend Configuration
                </Words>
                <Form method="POST">
                    {csrfInput}
                    <Textarea name="webhook_urls" label="Webhook URLs (one per line)" rows={5} defaultValue={config.webhook_urls} />
                    <Textarea name="jsonata_script" label="JSONata Script" rows={15} defaultValue={config.jsonata_script} />
                    <Button type="submit" className="mt-4">
                        Save Configuration
                    </Button>
                </Form>
            </Surface>
        </Shell>
    )
}