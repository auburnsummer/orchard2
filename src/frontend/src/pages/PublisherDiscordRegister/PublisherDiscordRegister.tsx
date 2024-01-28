import { object, string } from 'valibot';
import './PublisherDiscordRegister.css';
import { Header } from '~/components/Header';
import { Button, Input } from '~/ui';
import { useAsyncAction } from '~/hooks/useAsync';
import { createNewDiscordPublisher } from '~/api/publisher';
import { useForm } from '~/hooks/useForm';
import { Loading } from '~/components/Loading';

const formContentsSchema = object({
	name: string(),
});

function PublisherDiscordRegisterContents() {
	const [publisher, startRegister] = useAsyncAction(async (name: string) => {
		const urlParameters = new URLSearchParams(window.location.search);
		const guildToken = urlParameters.get('guild_token');
		if (!guildToken) {
			throw new Error('No guild token, try restarting the command');
		}

		if (name === '') {
			throw new Error('Publisher name cannot be blank.');
		}

		const pub = await createNewDiscordPublisher(name, guildToken);
		return pub;
	});

	const formProps = useForm(formContentsSchema, data => {
		startRegister(data.name);
	});

	if (publisher.state === 'not started') {
		return (
			<form
				class='pd_form'
				{...formProps}
			>
				<Input
					name='name'
					required
					label='Name the publisher'
					helpText='This is typically the name of the Discord server. You can change this later.'
				/>
				<Button variant='primary' type='submit'>Submit</Button>
			</form>
		);
	}

	if (publisher.state === 'loading') {
		return (
			<Loading class='pd_loading' text='Loading...' />
		);
	}

	if (publisher.state === 'has data') {
		return (
			<div class='pd_success'>
				<h1 class='pd_success-success'>Success!</h1>
				<p>Your publisher called "{publisher.data.name}" has been created.</p>
				<p>You may now close this window.</p>
				<p class='pd_success-techinfo'>id: {publisher.data.id}</p>
			</div>
		);
	}

	// Only remaining state is error
	return (
		<div class='pd_error'>
			<p class='pd_error-1'><b>Error:</b> {publisher.message}</p>
			<p class='pd_error-2'>Try again from the start. If it happens again, ping auburn!</p>
		</div>
	);
}

export function PublisherDiscordRegister() {
	return (
		<div class='pd'>
			<Header />
			<main class='pd_main'>
				<PublisherDiscordRegisterContents />
			</main>
		</div>
	);
}
