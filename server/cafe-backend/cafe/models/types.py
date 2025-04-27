from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from cafe.models.user import User as User
    from cafe.models.clubs.club import Club as Club

if TYPE_CHECKING:
    UserType: TypeAlias = "User"
    ClubType: TypeAlias = "Club"
else:
    UserType: TypeAlias = "cafe.User"
    ClubType: TypeAlias = "cafe.Club"
