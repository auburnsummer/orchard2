from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    discord_id: str = Field(primary_key=True)
    # should levels this user posts to #rd-showcase be automatically added?
    autoadd_preference: bool
    # a user can Star a level.
    # A user can only Star their own levels, and they can only star one level at a time.
    # starred_level = fields.ForeignKeyField('models.Status', related_name='starred_by', null=True)

class DiscordMessage(SQLModel, table=True):
    guild_id: str
    channel_id: str
    message_id: str = Field(primary_key=True)

class Level(SQLModel, table=True):
    rdlevel_sha1: str = Field(primary_key=True)

    artist: str
    artist_tokens = fields.JSONField()
    authors = fields.JSONField()
    authors_raw = fields.TextField()
    description = fields.TextField()
    description_ct = fields.JSONField()
    difficulty = fields.SmallIntField()

    # null if this level did not come from Discord.
    discord_source_message = fields.ForeignKeyField('models.DiscordMessage', related_name='levels_in_message', null=True)
    discord_attachment_id = fields.TextField(null=True)

    has_classics = fields.BooleanField()
    has_freetimes = fields.BooleanField()
    has_freezeshots = fields.BooleanField()
    has_holds = fields.BooleanField()
    has_oneshots = fields.BooleanField()
    has_squareshots = fields.BooleanField()
    has_skipshots = fields.BooleanField()
    has_window_dance = fields.BooleanField()
    hue = fields.FloatField()
    icon = fields.TextField()
    image = fields.TextField()
    last_updated = fields.DatetimeField()
    max_bpm = fields.FloatField()
    min_bpm = fields.FloatField()
    single_player = fields.BooleanField()
    sha1 = fields.TextField()
    song = fields.TextField() 
    song_ct = fields.JSONField()
    seizure_warning = fields.BooleanField()
    tags = fields.JSONField()
    thumb = fields.TextField()
    two_player = fields.BooleanField()

    # null if this level was not posted by a user.
    # a Level can be transferred to another User, so this can be different from the DiscordMessage's user id.
    user = fields.ForeignKeyField('models.User', related_name='levels_posted', null=True)
