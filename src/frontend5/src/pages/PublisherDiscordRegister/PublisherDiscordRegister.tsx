import { Header } from "@orchard/components/Header";

import "./PublisherDiscordRegister.css";
import { Button, Input } from "@orchard/ui";
import { useAsyncAction2 as useAsyncAction } from "@orchard/hooks/useAsync";

import { createNewDiscordPublisher } from "@orchard/api/publisher";
import { useForm } from "@orchard/hooks/useForm";

import * as tg from "generic-type-guard";
import { Loading } from "@orchard/components/Loading";

type FormContents = {
    name: string
}

const isFormContents: tg.TypeGuard<FormContents> = tg.isLikeObject({
    name: tg.isString
})

function PublisherDiscordRegisterContents() {
    const [publisher, startRegister] = useAsyncAction(async (name: string) => {
        const urlParams = new URLSearchParams(window.location.search);
        const guildToken = urlParams.get("guild_token");
        if (!guildToken) {
            throw new Error("No guild token, try restarting the command");
        }
        if (name === "") {
            throw new Error("Publisher name cannot be blank.");
        }
        const pub = await createNewDiscordPublisher(name, guildToken);
        return pub;
    });

    const formProps = useForm(isFormContents, (data) => {
        startRegister(data.name);
    });

    if (publisher.state === 'not started') {
        return (
            <form
                class="pd_form"
                {...formProps}
            >
                <Input
                    name="name"
                    required
                    label="Name the publisher"
                    helpText="This is typically the name of the Discord server. You can change this later."
                />
                <Button variant="primary" type="submit">Submit</Button>
            </form>
        )
    }

    if (publisher.state === 'loading') {
        return (
            <Loading class="pd_loading" text="Loading..." />
        )
    }

    if (publisher.state === 'has data') {
        return (
            <div class="pd_success">
                <h1 class="pd_success-success">Success!</h1>
                <p>Your publisher called "{publisher.data.name}" has been created.</p>
                <p>You may now close this window.</p>
                <p class="pd_success-techinfo">id: {publisher.data.id}</p>
            </div>
        )
    }

    // only remaining state is error
    return (
        <div class="pd_error">
            <p class="pd_error-1"><b>Error:</b> {publisher.message}</p>
            <p class="pd_error-2">Try again from the start. If it happens again, ping auburn!</p>
        </div>
    )
}

export function PublisherDiscordRegister() {
    return (
        <div class="pd">
            <Header />
            <main class="pd_main">
                <PublisherDiscordRegisterContents />
            </main>
        </div>
    )
}