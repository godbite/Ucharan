import re
from pathlib import Path
import json
import soundfile as sf
from syllable import normalize_text, syllables_from_words, Syllable
from stitch_techniques import (
    direct_concatenation,
    crossfade_transition,
    prosody_adjustment,
    crossfade_transition_prosody_adjustment,
)

VOICE_ACTOR_NAME = "shubh"


def nth_syllable_sample_path(n: int) -> Path:
    return Path(
        f"data/devanagari_syllable_dataset_split/{
            VOICE_ACTOR_NAME}_{n // 20 + 1:02}_{n % 20 + 1:02}.wav"
    )


def load_samples_by_name():
    samples_by_name = {}

    for file_path in speech_file_paths:
        if (m := re.match(r"(\w+)_(\d+)_(\d+)", file_path.stem)) is None:
            continue
        name, major, minor = m.groups()
        major, minor = int(major), int(minor)
        if name not in samples_by_name:
            samples_by_name[name] = []
        samples_by_name[name].append(file_path)

    return samples_by_name


test_file = Path("data/test.txt")
syllables = [
    syllables_from_words([word])
    for word in normalize_text(test_file.read_text()).split()
]

file_paths = list((Path(__file__).parent / "./data/corpus").glob("*"))


speech_file_paths = sorted(
    (Path(__file__).parent / "./data/devanagari_syllable_dataset_split").glob("*.wav")
)
x

samples_by_name = load_samples_by_name()
speech_samples = samples_by_name[VOICE_ACTOR_NAME]


with open("data/frequency.json") as f:
    json_raw = json.load(f)

# print("\n".join(str(Syllable(*record["syllable"].values())) for record in json_raw)); exit()

# test_file = speech_file_paths[0]


print(syllables)

loaded_syllables = {
    Syllable(*record["syllable"].values()): i for i, record in enumerate(json_raw)
}
loaded_syllables[syllables_from_words(["\u091a\u094b"])[0]] = loaded_syllables[
    syllables_from_words(["\u091a\u094c"])[0]
]

speech_indices = [
    [loaded_syllables[s] for s in w if s in loaded_syllables] for w in syllables
]

print(f"{speech_indices=}")

syllable_paths = [
    [
        nth_syllable_sample_path(i)
        for i in word
        if not nth_syllable_sample_path(i).exists()
    ]
    for word in speech_indices
]
print(f"{syllable_paths=}")

syllable_paths = [
    [nth_syllable_sample_path(i)
     for i in word if nth_syllable_sample_path(i).exists()]
    for word in speech_indices
]
print(f"{syllable_paths=}")

sf.write("data/1.wav", *direct_concatenation(syllable_paths))
sf.write("data/2.wav", *crossfade_transition(syllable_paths))
sf.write("data/3.wav", *prosody_adjustment(syllable_paths))
sf.write("data/4.wav", *crossfade_transition_prosody_adjustment(syllable_paths))
