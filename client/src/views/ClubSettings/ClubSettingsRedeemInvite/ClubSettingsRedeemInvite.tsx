import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter/ShellDramaticCenter";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { Club } from "@cafe/types/club";
import { ClubMembership } from "@cafe/types/clubMembership";
import { Button, Paper, Text, Title, Stack } from "@mantine/core";
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
      <>
        <Text>The invite is invalid or has expired.</Text>
        <Text>Please ask the person who invited you to send a new invite.</Text>
        <Text>If it keeps happening, please ping Auburn for help.</Text>
      </>
    );
  } else if (isPointless(props.membership, props.role)) {
    content = (
      <Stack gap="xs">
        <Title order={2}>Cannot Redeem Invite</Title>
        <Text>
          You already have{" "}
          {props.membership?.role === "owner" ? "owner" : "admin"} access to{" "}
          <b>{props.invite.club.name}</b>.
        </Text>
        <Text>
          This invite is valid, but redeeming it would not change your current
          permissions in the group.
        </Text>
      </Stack>
    );
  } else {
    content = (
      <Form method="post">
        {input}
        <Stack gap="xs">
          <Title order={2}>Redeem Invite</Title>
          <Text>
            You are being invited to the group <b>{props.invite.club.name}</b>
          </Text>
          <Button type="submit">Join {props.invite.club.name}</Button>
        </Stack>
      </Form>
    );
  }
  return (
    <ShellDramaticCenter>
      <Paper shadow="md" p="xl">
        {content}
      </Paper>
    </ShellDramaticCenter>
  );
}
