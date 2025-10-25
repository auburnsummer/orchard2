import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter";
import { Button } from "@cafe/components/ui/Button";
import { Words } from "@cafe/components/ui/Words";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";
import { ClubMembership } from "@cafe/types/clubMembership";
import { ReactNode } from "react";

type ClubSettingsRedeemInviteProps = {
  invite: {
    club: Club;
  } | null;
  code: string;
  expiry: string;
  role: "owner" | "admin";
  membership: ClubMembership | null;
};

function isPointless(
  membership: ClubMembership | null,
  role: "owner" | "admin",
) {
  if (membership === null) return false;
  if (membership.role === "owner") {
    return true;
  }
  if (role === "admin" && membership.role === "admin") {
    return true;
  }
  return false;
}

export function ClubSettingsRedeemInvite(props: ClubSettingsRedeemInviteProps) {
  const input = useCSRFTokenInput();

  let content: ReactNode;
  if (props.invite === null) {
    content = (
      <div>
        <Words as="p">The invite is invalid or has expired.</Words>
        <Words as="p">Please ask the person who invited you to send a new invite.</Words>
        <Words as="p">If it keeps happening, please ping Auburn for help.</Words>
      </div>
    );
  } else if (isPointless(props.membership, props.role)) {
    content = (
      <div className="flex flex-col gap-2">
        <Words variant="header" as="h2">Cannot Redeem Invite</Words>
        <Words>
          You already have{" "}
          {props.membership?.role === "owner" ? "owner" : "admin"} access to{" "}
          <b>{props.invite.club.name}</b>.
        </Words>
        <Words>
          This invite is valid, but redeeming it would not change your current
          permissions in the group.
        </Words>
      </div>
    );
  } else {
    content = (
      <Form method="post">
        {input}
        <div className="flex flex-col gap-2">
          <Words as="h2" variant="header">Redeem Invite</Words>
          <Words>
            You are being invited to the group <b>{props.invite.club.name}</b>
          </Words>
          <Button type="submit" variant="primary">Join {props.invite.club.name}</Button>
        </div>
      </Form>
    );
  }
  return (
    <ShellDramaticCenter>
      {content}
    </ShellDramaticCenter>
  );
}
