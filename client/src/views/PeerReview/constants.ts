export const BAD_THING_CATS = ['level', 'rows', 'metadata'] as const;

export const BAD_THINGS = [
    {
        name: "(did not play completely, might have other problems)",
        description: "A pharmacist did not review the entirety of the level. This often happens when pharmacists have a lot of levels to get through. Levels CANNOT be PRd if this is selected.",
        category: "level"
    } as const,
    {
        name: "Bad Audio",
        description: "A portion of the level's audio is imbalanced, making gameplay difficult.",
        category: "level"
    } as const,
    {
        name: "Harmful Audio",
        description: "A portion of the level's audio is harmful to headphone users.",
        category: "level",
        hidden: true
    } as const,
    {
        name: "No Volume Warning",
        description: "No clear volume warning is present before loud audio plays.",
        category: "level",
        hidden: true
    } as const,
    {
        name: "Did Not Meet Jam Criteria",
        description: "(of a level with a competition/jam's tag) if a level breaks a unique rule, or does not follow the theme of the Jam(s) it's for. THIS IS NOT A REASON TO NR.",
        category: "level",
        hidden: true
    } as const,
    {
        name: "Endless Level",
        description: "The level is a gameplay loop that will never reach an official end to the level (At least 1 of 3 End Level action events).",
        category: "level"
    } as const,
    {
        name: "Incorrect BPM/Offset",
        description: "Any part of the level's gameplay has the wrong BPM or offset (except double/half time).",
        category: "level"
    } as const,
    {
        name: "Reupload of Peer-Reviewed Level",
        description: "The level by the same author of the exact same song is Peer Reviewed again without removing the first version. THIS IS NOT A REASON TO NR.",
        category: "level"
    } as const,
    {
        name: "Rhythm Game Clone",
        description: "The majority of the level is a remake of charts, tracks, or gameplay from a music game, rhythm game, or official Rhythm Doctor/ADOFAI levels, collabs, or minigames.",
        category: "level"
    } as const,
    {
        name: "Unperfectable",
        description: "It is not possible to get an S rank by a human player.",
        category: "level"
    } as const,
    {
        name: "Unreadable VFX",
        description: "Crazy and unnecessary visuals OR no visuals for an extended period of time.",
        category: "level"
    } as const,
    {
        name: "Bad Burnshots",
        description: "A Burnshot is incorrectly used, such as incorrect intervals, neglect of the cue, or otherwise.",
        category: "rows"
    } as const,
    {
        name: "Bad Freezeshots",
        description: "A Freezeshot is incorrectly used, such as incorrect intervals, neglect of the cue, or otherwise.",
        category: "rows"
    } as const,
    {
        name: "Bad Skipshots",
        description: "A Skipshot is incorrectly used, such as incorrect intervals, neglect of the cue, or otherwise.",
        category: "rows"
    } as const,
    {
        name: "Bad Triangleshots",
        description: "A Triangleshot is incorrectly used, such as incorrect intervals, neglect of the cue, or otherwise.",
        category: "rows"
    } as const,
    {
        name: "Bad Change Player Rows Timing",
        description: "A \"Change Player Rows\" action event is mistimed, causing a miss or unreactable gameplay.",
        category: "rows"
    } as const,
    {
        name: "Bad Holds",
        description: "A hold that starts while the player is already holding another beat.",
        category: "rows"
    } as const,
    {
        name: "Bad Syncopation",
        description: "An automatic syncopation is made inaudible OR a manual syncopation is cued poorly.",
        category: "rows"
    } as const,
    {
        name: "Bad X Rows",
        description: "A row is played where there are X's on the first beat of a row (unless a count is audible) or there are more than 4 X's on the row.",
        category: "rows"
    } as const,
    {
        name: "Heck Swing",
        description: "A swing beat is set at the maximum swing number, causing beats to be skipped. ",
        category: "rows"
    } as const,
    {
        name: "Incorrect Ticks that Negatively Affect Gameplay",
        description: "Ticks or row beats are weirdly offbeat against the fluidity of the level.",
        category: "rows"
    } as const,
    {
        name: "Incorrectly Cued Gimmicks",
        description: "Either a community or custom gimmick does not follow its own rules correctly OR gimmick cues are not demonstrated clearly.",
        category: "rows"
    } as const,
    {
        name: "Miscued Oneshots",
        description: "A Oneshot's cue is incorrect either at the wrong placement or at the wrong tick.",
        category: "rows"
    } as const,
    {
        name: "No Beat Sound",
        description: "A row is played and does not have a sound or a cue.",
        category: "rows"
    } as const,
    {
        name: "Pseudos",
        description: "A series of hits that are so close together as to be near impossible to hit with one button.",
        category: "rows"
    } as const,
    {
        name: "Shakeritis",
        description: "2 or more rows or beats have indiscernible beat/hold sounds that play separately at the same time.",
        category: "rows"
    } as const,
    {
        name: "Uncued Freetimes",
        description: "Any freetime that is not cued and does not follow a standard row pattern.",
        category: "rows"
    } as const,
    {
        name: "Uncued Oneshots",
        description: "A Oneshot, or a change in a Oneshot pattern, is not cued at all.",
        category: "rows"
    } as const,
    {
        name: "Unreactable Gameplay",
        description: "A series of ticks so fast that the player is unable to fairly respond to.",
        category: "rows"
    } as const,
    {
        name: "Unreactable Triangleshots",
        description: "A triangleshot is not fairly reactable, typically if the amount is too high, the tick is too fast, or the cue is too sudden.",
        category: "rows"
    } as const,
    {
        name: "Blacklisted",
        description: "The artist or song used is blacklisted. In this case, the level is deleted.",
        category: "metadata",
        hidden: true
    } as const,
    {
        name: "No Seizure Warning",
        description: "If the Seizure Warning button is \"off\" and the level contains 3 high contrast changes within 1 second.",
        category: "metadata"
    } as const,
    {
        name: "Uncredited Custom Assets",
        description: "If the level includes any custom Rhythm Doctor assets that the creator has required crediting to use.",
        category: "metadata",
        hidden: true
    } as const,
    {
        name: "Incorrect Metadata",
        description: "If the level breaks any metadata rules.",
        category: "metadata"
    } as const,
].sort((a, b) => a.name.localeCompare(b.name));

export type BadThing = typeof BAD_THINGS[number];

export type BadThingCategory = typeof BAD_THING_CATS[number];

export type BadThingNames = BadThing['name'];

export const JAM_TAGS = [
    "RDRPG",
    "Internet Jam",
    "smol Jam",
    "Two-Handed Jam",
    "Workshop Jam",
    "Vanilla Jam",
    "Creepypasta Jam",
    "Old Jam",
    "Odd Jam",
    "RDSRT",
    "RDSRT1",
    "RDSRT2",
    "RDSRT3",
    "Animal Jam",
    "Square Jam",
    "Tasty Jam",
    "Spicy Jam",
    "Street Life Jam"
];

export const BLOCKED_ARTISTS = [
    "ICE",
    "Project Grimoire",
    "KIVA",
    "Æsir",
    "AEsir",
    "KillerBlood",
    "Lesitia",
    "Sound Souler",
    "litmus*",
    "Zekk",
    "Team ArcStar",
    "antiPLUR",
    "Paul Bazooka",
    "Sound piercer",
    "Cosmograph",
    "a_hisa",
    "xi",
    "Tuyu",
    "ツユ"
];