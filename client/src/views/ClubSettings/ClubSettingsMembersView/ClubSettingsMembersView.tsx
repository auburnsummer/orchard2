import { Shell } from "@cafe/components/Shell";
import { Club } from "@cafe/types/club";
import { ClubSettingsNavbar } from "../ClubSettingsNavbar";
import { ClubMembership } from "@cafe/types/clubMembership";
import { useState } from "react";
import { AddMemberForm } from "./AddMemberForm";
import { EditMemberForm } from "./EditMemberForm";
import { useSearchParams } from "@cafe/minibridge/hooks";
import { CopyIconButton } from "@cafe/components/CopyIconButton";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Button } from "@cafe/components/ui/Button";
import { Alert } from "@cafe/components/ui/Alert";
import { Dialog } from "@cafe/components/ui/Dialog";
import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableHeaderCell,
  TableCell,
} from "@cafe/components/ui/Table";

type MembershipPermission = {
  can_change: boolean;
  can_delete: boolean;
};

type ClubSettingsMembersViewProps = {
  club: Club;
  memberships: {
    membership: ClubMembership;
    permissions: MembershipPermission;
  }[];
  can_add: boolean;
};

export function ClubSettingsMembersView({
  club,
  memberships,
  can_add,
}: ClubSettingsMembersViewProps) {
  const [editMemberFormOpen, setEditMemberFormOpen] = useState(false);
  const [membershipBeingEdited, setMembershipBeingEdited] =
    useState<ClubMembership | null>(null);
  const [addMemberFormOpen, setAddMemberFormOpen] = useState(false);
  const [searchParams] = useSearchParams();

  const inviteCode = searchParams.get("invite_code");
  const inviteUrl = new URL(
    `/groups/redeem_invite/${inviteCode}/`,
    window.location.origin,
  ).toString();

  const rows = memberships.map(({ membership, permissions }) => (
    <TableRow key={membership.user.id}>
      <TableCell firstColumn className="font-medium text-gray-900 dark:text-white">
        {membership.user.displayName}
      </TableCell>
      <TableCell className="text-xs text-gray-500 dark:text-gray-400 font-mono">
        {membership.user.id}
      </TableCell>
      <TableCell className="text-gray-500 dark:text-gray-400 capitalize">
        {membership.role}
      </TableCell>
      <TableCell lastColumn align="right" className="font-medium">
        <Button
          variant="secondary"
          onClick={() => {
            setMembershipBeingEdited(membership);
            setEditMemberFormOpen(true);
          }}
          disabled={!permissions.can_change && !permissions.can_delete}
          className="text-xs px-2 py-1"
        >
          Edit
        </Button>
      </TableCell>
    </TableRow>
  ));

  return (
    <Shell navbar={<ClubSettingsNavbar club={club} />}>
      <Dialog
        open={editMemberFormOpen}
        onClose={() => setEditMemberFormOpen(false)}
      >
        <EditMemberForm
          membership={membershipBeingEdited}
          canEdit={
            memberships.find(
              (m) => m.membership.user.id === membershipBeingEdited?.user.id,
            )?.permissions.can_change || false
          }
          club={club}
          onSubmit={() => setEditMemberFormOpen(false)}
        />
      </Dialog>
      <Dialog
        open={addMemberFormOpen}
        onClose={() => setAddMemberFormOpen(false)}
      >
        <AddMemberForm
          club={club}
          onSubmit={() => setAddMemberFormOpen(false)}
        />
      </Dialog>
      <Surface className="m-3 p-6 flex-grow">
        <div className="space-y-6">
          {inviteCode && (
            <Alert variant="info">
              <div className="flex flex-col gap-1">
                <Words className="font-semibold">Here is the invite link</Words>
                <Words className="text-sm">
                  Send this link to the person you want to invite.
                </Words>
                <div className="flex flex-row items-end gap-1">
                  <TextInput
                    onFocus={(e) => e.target.select()}
                    disabled={false}
                    value={inviteUrl}
                    readOnly
                    className="flex-grow"
                  />
                  <CopyIconButton value={inviteUrl} className="pb-0.5" />
                </div>
              </div>
            </Alert>
          )}

          <div className="sm:flex sm:items-center">
            <div className="sm:flex-auto">
              <Words as="h2" variant="header">Members of {club.name}</Words>
            </div>
            <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
              <Button 
                onClick={() => setAddMemberFormOpen(true)} 
                disabled={!can_add}
                variant="primary"
                className="px-3 py-2"
              >
                Add member
              </Button>
            </div>
          </div>

          <div className="mt-8">
            <Table>
              <TableHead>
                <TableRow>
                  <TableHeaderCell firstColumn>User</TableHeaderCell>
                  <TableHeaderCell>ID</TableHeaderCell>
                  <TableHeaderCell>Role</TableHeaderCell>
                  <TableHeaderCell lastColumn>
                    <span className="sr-only">Edit</span>
                  </TableHeaderCell>
                </TableRow>
              </TableHead>
              <TableBody>{rows}</TableBody>
            </Table>
          </div>
        </div>
      </Surface>
    </Shell>
  );
}
