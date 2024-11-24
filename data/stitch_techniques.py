from pathlib import Path
import numpy as np
import librosa

FADE_DURATION = 0.05
PAUSE_DURATION = 0.2


def add_pause(audio, sr, duration=PAUSE_DURATION):
    """Add a silent pause of the given duration."""
    pause = np.zeros(int(sr * duration))
    return np.concatenate([audio, pause])


def direct_concatenation(syllables_per_word: list[list[Path]]):
    output = []

    for word in syllables_per_word:
        word_audio = []
        for syllable in word:
            audio, sr = librosa.load(syllable, sr=None)
            word_audio.append(audio)
        # Concatenate syllables of the word and add a pause
        word_audio = np.concatenate(word_audio)
        output.append(add_pause(word_audio, sr))

    # Combine words to form the final sentence
    sentence_audio = np.concatenate(output)
    return sentence_audio, sr


def crossfade(s1, s2, fade_duration, sr):
    fade_samples = int(fade_duration * sr)
    fade_in = np.hanning(2 * fade_samples)[fade_samples:]
    fade_out = np.hanning(2 * fade_samples)[:fade_samples]
    s1[-fade_samples:] *= fade_out
    s2[:fade_samples] *= fade_in
    return np.concatenate(
        (s1[:-fade_samples], s1[-fade_samples:] + s2[:fade_samples], s2[fade_samples:])
    )


def crossfade_transition(syllables_per_word: list[list[Path]]):
    output = []

    for word in syllables_per_word:
        word_audio = []
        for i, syllable in enumerate(word):
            audio, sr = librosa.load(syllable, sr=None)
            if i > 0:
                word_audio = crossfade(
                    word_audio, audio, fade_duration=FADE_DURATION, sr=sr
                )
            else:
                word_audio = audio
        # Add a pause after the word
        output.append(add_pause(word_audio, sr))

    sentence_audio = np.concatenate(output)
    return sentence_audio, sr


def adjust_syllable(audio, sr, pitch_shift=0, stretch_factor=1, emphasis=1):
    audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=pitch_shift)
    audio = librosa.effects.time_stretch(audio, rate=stretch_factor)
    return audio * emphasis


def prosody_adjustment(syllables_per_word: list[list[Path]]):
    output = []

    for word in syllables_per_word:
        word_audio = []
        for syllable in word:
            audio, sr = librosa.load(syllable, sr=None)
            # Example parameters: pitch_shift, stretch_factor, emphasis
            adjusted_audio = adjust_syllable(
                audio, sr, pitch_shift=0, stretch_factor=1, emphasis=1
            )
            word_audio.append(adjusted_audio)
        word_audio = np.concatenate(word_audio)
        output.append(add_pause(word_audio, sr))

    sentence_audio = np.concatenate(output)
    return sentence_audio, sr


def crossfade_transition_prosody_adjustment(syllables_per_word: list[list[Path]]):
    output = []

    for word in syllables_per_word:
        word_audio = []
        for i, syllable in enumerate(word):
            audio, sr = librosa.load(syllable, sr=None)
            # Apply prosody adjustment (example parameters)
            adjusted_audio = adjust_syllable(
                audio, sr, pitch_shift=0, stretch_factor=1, emphasis=1.2
            )
            if i > 0:  # Apply crossfade between consecutive syllables
                word_audio = crossfade(
                    word_audio, adjusted_audio, fade_duration=0.05, sr=sr
                )
            else:
                word_audio = adjusted_audio
        # Add a pause after the word
        output.append(add_pause(word_audio, sr))

    # Combine words to form the final sentence
    sentence_audio = np.concatenate(output)
    return sentence_audio, sr
