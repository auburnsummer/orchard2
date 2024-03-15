import './Home.css';
import { Header } from '~/components/Header';
import { LevelList } from '~/components/LevelList';
import { Loading } from '~/components/Loading';
import { searchResultsCombined$ } from '~/signals/searchResults';
import { Button, Dialog } from '~/ui';

function HomeContents() {
	const searchResultsCombined = searchResultsCombined$.value;
	if (searchResultsCombined.state === 'loading') {
		return (
			<Loading class={'ho_loading'} text='Loading...' />
		);
	}

	if (searchResultsCombined.state === 'has error') {
		return (
			<Dialog open={true} label='Error' noHeader>
				<p>An error occured while getting the levels.</p>
				<p>{searchResultsCombined.message}</p>
				<p>Try refreshing the page. If this error persists, ping auburn!</p>
				<Button slot='footer' variant='primary' onClick={() => window.location.reload()}>
					Refresh
				</Button>
			</Dialog>
		);
	}

	return <LevelList class='ho_levels' />;
}

export function Home() {
	return (
		<div class='ho'>
			<Header />
			<div class='ho_contents'>
				<HomeContents />
			</div>
		</div>
	);
}
