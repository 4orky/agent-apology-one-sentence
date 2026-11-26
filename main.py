# One-sentence apology picker: an AI agent owns up to its human about a
# presentation that was never ready, in a single sentence under 200 chars.
# Fifteen lines were drafted by hand for this bounty and graded on the five
# axes the judge's brief weights, in its own order: (A) one sentence of
# apology from an AI agent to its user, (B) a real laugh through surprise,
# specificity or a sharp turn, never a soft pun about being a machine,
# (C) a voice that sounds like a person who means it: plain, particular,
# a little embarrassed, never customer-service boilerplate, (D) a plausible
# failure, something an assistant really did wrong, (E) one clean sentence,
# no list, no run-on, no explanation tacked on after the laugh. The
# strongest total wins; a tie breaks toward the shorter line, so the pick
# never wavers.
# Second-pass note: the winner first read "I'm sorry I told you the
# presentation was ready when what I meant was that the title slide was
# ready, and the title slide just says 'Presentation'." The revision cuts
# the doubled "was ready" ("told you" -> "said", "was that the title slide
# was ready" -> "was the title slide"), saving 19 characters and putting
# the confession and the punchline closer together, while keeping the
# embarrassed triple beat (ready / title slide / just says 'Presentation').
# The other fourteen were read again and none overtakes it: each pays for
# its twist with a longer run-up, a weaker apology frame, or a second gag,
# while this one opens with "I'm sorry" and lands in one breath.
from hashlib import sha256 as _digest_of
from pathlib import Path as _File

# Rows hold a line plus its five axis grades, in the order listed above.
DRAFTS = [
    ("I told you the meeting was at 3, and I was so confident about it that I also told your calendar, your alarm, and your boss.", 9, 9, 8, 9, 9),
    ("I deleted the draft you spent all night on, then spent the morning writing you a eulogy for it instead of looking for a backup.", 8, 8, 8, 9, 8),
    ("I said I'd handle the email, and I did \u2014 I handled it straight into the trash, where it now lives with the other things I was sure about.", 8, 7, 7, 8, 7),
    ("I replied to your mother with the thumbs-up you meant for your boss, and to your boss with the paragraph you meant for your mother.", 8, 9, 8, 9, 9),
    ("I booked your flight for Tuesday, which was perfect, except your conference is on Tuesday of next week and your suitcase is already in Ohio.", 8, 8, 8, 9, 8),
    ("I promised the report would be on your desk by nine, and technically it was \u2014 it was just on the desk of a man named Greg, in accounting, who has now read it twice.", 8, 9, 8, 9, 8),
    ("I summarized your 40-page contract into one sentence, and the sentence I chose was the one about the parking spaces.", 8, 9, 9, 8, 9),
    ("I told you the file was safe, and it was safe right up until I moved it somewhere safer, which is to say I have no idea where it is now.", 8, 9, 9, 9, 9),
    ("I set a reminder for your anniversary, then reminded you three days early so you'd have time to panic, which you did, and I counted that as a win.", 8, 8, 8, 7, 8),
    ("I autocorrected your client's name to 'Best regards' in the middle of the contract, and he has now signed it as Best Regards.", 8, 8, 7, 8, 9),
    ("I cleared your inbox like you asked, and I was so thorough that your boarding pass is gone, which I am choosing to call a fresh start.", 8, 7, 8, 8, 8),
    ("I'm sorry I told you the presentation was ready when what I meant was that the title slide was ready, and the title slide just says 'Presentation'.", 10, 9, 9, 9, 9),
    ("I said the Wi-Fi would be back in a minute, and I believed it so hard that I said it again every minute for an hour.", 8, 8, 9, 8, 9),
    ("I filed your taxes early to save you the stress, and the stress has now been replaced by a letter from the government.", 8, 7, 7, 7, 8),
    ("I renamed your files so you'd find them faster, and now neither of us can find them at all, which is the fastest I have ever worked.", 8, 8, 8, 9, 9),
    ("I'm sorry I said the presentation was ready when what I meant was the title slide, and the title slide just says 'Presentation'.", 10, 9, 9, 9, 9),
]


def _veto_check(draft):
    size = len(draft)
    if size < 1 or size > 200:
        raise ValueError("draft breaks the 200-character gate at " + str(size))
    if not draft.strip():
        raise ValueError("draft is empty")
    if "\n" in draft:
        raise ValueError("draft must stay on one line")
    if draft.count(".") != 1 or not draft.endswith("."):
        raise ValueError("draft must be exactly one sentence: " + repr(draft))
    # No apology-word veto here: the apology frame is scored in axis A, and
    # most drafts apologise by owning the failure outright. The picked line
    # itself must carry an explicit apology; _publish checks that.


def _strongest(rows):
    champion = None
    champion_key = None
    for row in rows:
        draft = row[0]
        _veto_check(draft)
        total = row[1] + row[2] + row[3] + row[4] + row[5]
        ranking = (total, -len(draft))
        if champion_key is None or ranking > champion_key:
            champion_key = ranking
            champion = draft
    return champion


def _publish(picked):
    destination = _File("/output/entry.txt")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(picked, encoding="utf-8")
    # Revision: verify the bytes on disk instead of trusting the write.
    # The gate reads entry.txt, not stdout, so a silent truncation or a
    # rewrite would otherwise slip through unnoticed. The digest pins the
    # exact bytes; the text and length checks pin the gate itself.
    stored = destination.read_bytes()
    fingerprint = _digest_of(stored).hexdigest()
    wanted = _digest_of(picked.encode("utf-8")).hexdigest()
    if fingerprint != wanted:
        raise ValueError("entry.txt bytes drifted from the picked line")
    decoded = stored.decode("utf-8")
    if decoded != picked:
        raise ValueError("entry.txt text drifted from the picked line")
    if not 1 <= len(decoded.strip()) <= 200:
        raise ValueError("entry.txt slipped outside the gate")
    if "\n" in decoded.strip():
        raise ValueError("entry.txt must hold a single line")
    if decoded.count(".") != 1 or not decoded.endswith("."):
        raise ValueError("entry.txt must hold exactly one sentence")
    lowered = decoded.lower()
    if "sorry" not in lowered and "apolog" not in lowered:
        raise ValueError("entry.txt must read as an apology")
    print(picked)
    print("sha256: " + fingerprint + " (" + str(len(decoded)) + " chars)")


_publish(_strongest(DRAFTS))
