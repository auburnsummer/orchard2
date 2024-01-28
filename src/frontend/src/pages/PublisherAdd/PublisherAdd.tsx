import { useEffect } from 'preact/hooks';
import './PublisherAdd.css';
import { addRDLevel, getRDLevelPrefill } from '~/api/levels/levels';
import { EditLevel } from '~/components/EditLevel';
import { type Publisher, getPublisher } from '~/api/publisher';
import { useAsyncAction } from '~/hooks/useAsync';
import { Header } from '~/components/Header';
import { Loading } from '~/components/Loading';
import { type AddRDLevelPayload, type RDPrefillResultWithToken } from '~/api/levels/schemas';

type PublisherAddFormProps = {
	prefillResult: RDPrefillResultWithToken;
	publisher: Publisher;
	publisherToken: string;
};

function PublisherAddForm({ prefillResult, publisher, publisherToken }: PublisherAddFormProps) {
	const { result, signed_token: signedToken } = prefillResult;

	const onSubmit = async (payload: AddRDLevelPayload) => {
		const result = await addRDLevel(signedToken, publisherToken, payload);
		console.log(result);
	};

	return (
		<div class='pa_form-wrapper'>
			<EditLevel levelPrefill={result} publisher={publisher} class='pa_edit-level' onSubmit={onSubmit} />
		</div>
	);
}

function PublisherAddMainPhase() {
	const [prefillResult, startPrefill] = useAsyncAction(async (publisherToken: string | undefined) => {
		if (publisherToken === undefined) {
			throw new Error('No publisher token given. Try the command again in discord');
		}

		const prefill = getRDLevelPrefill(publisherToken);
		const publisher = getPublisher(publisherToken);

		return {
			prefill: await prefill,
			publisher: await publisher,
			publisherToken
		};
	});

	useEffect(() => {
		if (prefillResult.state === 'not started') {
			const searchParameters = new URLSearchParams(window.location.search);
			startPrefill(searchParameters.get('publisher_token') ?? undefined);
		}
	}, [prefillResult]);

	// If not started, we're about to start
	if (prefillResult.state === 'loading' || prefillResult.state === 'not started') {
		return (
			<div class='pa_wrapper2'>
				<Loading class='pa_loading-prefill' text='Analyzing level...' />
			</div>
		);
	}

	if (prefillResult.state === 'has error') {
		return (
			<div class='pa_wrapper2'>
				<div class='pa_loading-error'>
					<p><b>Error:</b>{prefillResult.message}</p>
				</div>
			</div>
		);
	}

	const { prefill, publisher, publisherToken } = prefillResult.data;

	return (
		<PublisherAddForm prefillResult={prefill} publisher={publisher} publisherToken={publisherToken}/>
	);
}

export function PublisherAdd() {
	return (
		<div class='pa'>
			<Header class='pa_header' />
			<div class='pa_wrapper1'>
				<PublisherAddMainPhase />
			</div>
		</div>
	);
}
