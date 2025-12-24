import { Shell } from "@cafe/components/Shell/Shell";
import { ProfileNavbar } from "./ProfileNavbar";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";

export function ProfileIndexView() {
  return (
    <Shell navbar={<ProfileNavbar />}>
      <Surface className="m-3 p-6 flex-grow">
        <Words as="p">This is your profile page! There isn't anything here yet.</Words>
        <Words as="p" className="mt-4">
          I'm thinking in the future, you could have a little bio here and your
          favourite levels!
        </Words>
        <Words as="p">...please be patient 🙏</Words>
      </Surface>
    </Shell>
  );
}
