import { useMemo, useState } from 'preact/hooks';
import { getErrorMessage } from '~/utils/error';

type AsyncActionFunction<Args extends unknown[], Result> = (...args: Args) => Promise<Result>;

export type AsyncState<Result> = {
	state: 'not started';
} | {
	state: 'loading';
} | {
	state: 'has error';
	error: unknown;
	message: string;
} | {
	state: 'has data';
	data: Awaited<Result>;
};

export type AsyncResource<Result> = Exclude<AsyncState<Result>, { state: 'not started' }>;

/**
 * Hook to control the execution of an async function.
 * The first value is the state of the function.
 * The second value is a function to start the execution.
 * nb: The input function should be memoized to avoid rerenders.
 */
export function useAsyncAction<Args extends unknown[], Result>(func: AsyncActionFunction<Args, Result>) {
	const [value, setValue] = useState<AsyncState<Result>>({ state: 'not started' });

	const runFunc = useMemo(() => {
		const runner = async (...args: Args) => {
			setValue({ state: 'loading' });
			try {
				const data = await func(...args);
				setValue({
					state: 'has data',
					data,
				});
			} catch (error) {
				const errorMessage = await getErrorMessage(error);
				setValue({
					state: 'has error',
					message: errorMessage,
					error,
				});
			}
		};

		return (...args: Args) => {
			void runner(...args);
		};
	}, [func, setValue]);

	return [value, runFunc] as const;
}
