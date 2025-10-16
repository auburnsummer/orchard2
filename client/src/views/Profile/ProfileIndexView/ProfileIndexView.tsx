import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "../ProfileNavbar/ProfileNavbar";

export function ProfileIndexView() {
  return (
    <Shell navbar={<ProfileNavbar />}>
      <div>
        <p>This is your profile page! There isn't anything here yet.</p>
        <p>
          I'm thinking in the future, you could have a little bio here and your
          favourite levels!
        </p>
        <p>...please be patient 🙏</p>
      </div>
    </Shell>
  );
}
