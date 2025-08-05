import { Link } from '@cafe/minibridge/components/Link';
import { Shell } from '../components/Shell';

export function HomeView() {
    return (
        <Shell>
            <p>This is the home page</p>
            <p>nothing here yet, so...</p>
            <p>...click <Link href="/levels">here</Link> to go to the main levels view</p>
        </Shell>
    );
}
  