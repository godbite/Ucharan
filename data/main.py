from collections import Counter
import json
from pathlib import Path
from syllable import load_text, normalize_text, syllables_from_words

file_paths = list((Path(__file__).parent / "./data/corpus").glob("*"))

count = 10
counter = Counter()

for start in range(0, len(file_paths), count):
    counter.update(
        syllables_from_words(normalize_text(load_text(start, count)).split())
    )

common_ones = sorted(counter.most_common(300), key=lambda kv: str(kv[0]))

json_raw = [
    {"syllable": syllable.__dict__(), "frequency": frequency}
    for syllable, frequency in common_ones
]

with open("data/frequency.json", "w") as f:
    json.dump(json_raw, f)

count = 20

with open("data/syllables.txt", "w") as f:
    for i in range(0, len(common_ones), count):
        reprs = [str(kv[0]) for kv in common_ones[i : i + count]]
        f.write("\n".join(reprs) + "\n\n\n")
