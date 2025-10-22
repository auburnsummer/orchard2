import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "./ProfileNavbar";
import { Surface } from "@cafe/components/ui/Surface";

export function ProfileIndexView() {
  return (
    <Shell navbar={<ProfileNavbar />}>
      <Surface className="m-3 p-6 flex-grow">
        <p>This is your profile page! There isn't anything here yet.</p>
        <p>
          I'm thinking in the future, you could have a little bio here and your
          favourite levels!
        </p>
        <p>...please be patient 🙏</p>
      </Surface>
    </Shell>
  );
}
