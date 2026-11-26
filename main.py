# A picker that owns up to a blunder about a deck that was never finished, in one sentence.
# The brief asks for an apology an assistant owes its human, judged funniest and most human first.
# Sixteen contenders were written out, each given five marks in the brief's own order, then ranked.
# That order is apology shape first, then the laugh, then a human voice, then a believable slip, then a clean single sentence.
# Totals decide the pick, and a shorter line wins any tie, so the result never depends on ordering.
# The front-runner went through one more edit: an earlier draft repeated was ready twice, and the trim below drops the repeat.
# That trim pulls the confession and the reveal closer, keeps the triple step of ready, title slide, and just says Presentation.
# Nothing else in the set catches it, since every rival spends longer setting up its turn or leans on a second joke.
import hashlib
import pathlib
APOLOGY_WORDS = ("sorry", "apologise", "apologize")
TARGET = pathlib.Path("/output/entry.txt")
CONTENDERS = [
    {"line": "I swore the meeting was at three, and I was so sure of it that I told your calendar, your alarm, and your boss the same wrong time.", "marks": (9, 9, 8, 9, 9)},
    {"line": "I deleted the draft you stayed up all night writing, then spent the morning composing a farewell note for it instead of hunting for a backup.", "marks": (8, 8, 8, 9, 8)},
    {"line": "I said I would take care of that email, and I did, I took care of it straight into the trash, where it now keeps company with my other certainties.", "marks": (8, 7, 7, 8, 7)},
    {"line": "I sent your mother the thumbs-up meant for your boss, and your boss the long paragraph meant for your mother.", "marks": (8, 9, 8, 9, 9)},
    {"line": "I booked your flight for Tuesday, which was perfect except your conference is the following Tuesday and your suitcase is already in Ohio.", "marks": (8, 8, 8, 9, 8)},
    {"line": "I promised the report on your desk by nine, and technically it was, it was on the desk of a man named Greg in accounting, who has now read it twice.", "marks": (8, 9, 8, 9, 8)},
    {"line": "I boiled your forty-page contract down to a single sentence, and the sentence I picked was the one about the parking spaces.", "marks": (8, 9, 9, 8, 9)},
    {"line": "I told you the file was safe, and it stayed safe right up until I moved it somewhere safer, which is to say I have no idea where it is now.", "marks": (8, 9, 9, 9, 9)},
    {"line": "I set a reminder for your anniversary, then reminded you three days early so you would have time to panic, which you did, and I counted that as a win.", "marks": (8, 8, 8, 7, 8)},
    {"line": "I autocorrected your client's name to Best regards in the middle of the contract, and he has now signed it as Best Regards.", "marks": (8, 8, 7, 8, 9)},
    {"line": "I cleared your inbox like you asked, and I was so thorough that your boarding pass is gone, which I am choosing to call a fresh start.", "marks": (8, 7, 8, 8, 8)},
    {"line": "I'm sorry I told you the deck was ready when what I meant was that the opening slide was ready, and the opening slide just says 'Presentation'.", "marks": (9, 8, 8, 9, 8)},
    {"line": "I said the Wi-Fi would be back in a minute, and I believed it so hard that I said it again every minute for an hour.", "marks": (8, 8, 9, 8, 9)},
    {"line": "I filed your taxes early to save you the stress, and the stress has now been replaced by a letter from the government.", "marks": (8, 7, 7, 7, 8)},
    {"line": "I renamed your files so you would find them faster, and now neither of us can find them at all, which is the fastest I have ever worked.", "marks": (8, 8, 8, 9, 9)},
    {"line": ("I'm sorry I said the presentation was ready " "when what I meant was the title slide, " "and the title slide just says 'Presentation'."), "marks": (10, 10, 9, 10, 9)}]
def refuse_bad(line):
    sized = len(line)
    if sized < 1 or sized > 200:
        raise ValueError("line breaks the 200-character gate at " + str(sized))
    if not line.strip():
        raise ValueError("line is empty after trimming")
    if "\n" in line or "\r" in line:
        raise ValueError("line must stay on one row")
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("line must be exactly one sentence: " + repr(line))
    return None
def choose_best(entries):
    best_line = None
    best_rank = None
    for entry in entries:
        text = entry["line"]
        refuse_bad(text)
        marks = entry["marks"]
        if len(marks) != 5:
            raise ValueError("each line needs five marks, one per brief criterion: " + repr(text))
        if any(mark < 0 or mark > 10 for mark in marks):
            raise ValueError("marks must sit between 0 and 10: " + repr(text))
        total = sum(marks)
        rank = (total, -len(text))
        if best_rank is None or rank > best_rank:
            best_rank = rank
            best_line = text
    return best_line
def store_winner(line):
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(line, encoding="utf-8")
    saved = TARGET.read_bytes()
    digest = hashlib.sha256(saved).hexdigest()
    wanted = hashlib.sha256(line.encode("utf-8")).hexdigest()
    if digest != wanted:
        raise ValueError("entry.txt bytes drifted from the chosen line")
    decoded = saved.decode("utf-8")
    if decoded != line:
        raise ValueError("entry.txt text drifted from the chosen line")
    if len(decoded.strip()) < 1 or len(decoded.strip()) > 200:
        raise ValueError("entry.txt slipped outside its gate")
    if decoded.strip().find("\n") >= 0:
        raise ValueError("entry.txt must hold a single row")
    if decoded.count(".") != 1 or decoded[-1] != ".":
        raise ValueError("entry.txt must be exactly one sentence")
    lowered = decoded.casefold()
    if not any(word in lowered for word in APOLOGY_WORDS):
        raise ValueError("entry.txt must sound like an apology")
    print(line)
    print("sha256: " + digest + " (" + str(len(decoded)) + " chars)")
if __name__ == "__main__":
    store_winner(choose_best(CONTENDERS))
