import { Shell } from "@cafe/components/Shell";
import { DailyBlendNavbar } from "./DailyBlendNavbar";
import { Form } from "@cafe/minibridge/components/Form";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Surface } from "@cafe/components/ui/Surface";
import { Button } from "@cafe/components/ui/Button";
import { Words } from "@cafe/components/ui/Words";

export function DailyBlendBlendNow() {
    const csrfInput = useCSRFTokenInput();

    return (
        <Shell
            navbar={<DailyBlendNavbar />}
        >
            <Surface
                className="mt-3 p-40 mr-3"
            >
            <Words>Click the button to immediately trigger the blend.</Words>
            {/* The actual button */}
                <Form method="POST" className="relative">
                    {csrfInput}
                    <Button 
                        type="submit"
                        variant="primary"
                        className="mt-4 w-60 h-40 shadow-2xl"
                    >
                        【﻿ＢＬＥＮＤ　ＮＯＷ】
                    </Button>
                </Form>
            </Surface>
        </Shell>
    )
}