import './404.css';
import edegaBudgetCuts from './edegabudgetcuts.webp';

export function NotFound() {
	return (
		<div class='nf'>
			<div class='nf_content'>
				<img src={edegaBudgetCuts} class='nf_:edegabudgetcuts:' />
				<h1 class='nf_title'>page not found :(</h1>
			</div>
		</div>
	);
}
