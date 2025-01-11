# uchchaaran

A text-to-speech (TTS) system using concatenative synthesis to generate speech for Devanagari-script (mainly Hindi and Bhojpuri) languages. It combines pre-recorded audio units for natural, clear speech output.

## Dataset

The dataset is contained in the `data` directory.

* `data/corpus`: Hindi text corpus
* `data/devanagari_syllable_dataset`: Speech dataset we created for each team member
* `data/devanagari_syllable_dataset_split`: Segmented speech samples dataset
* `data/frequency.json`: Frequency data of each segmented syllable like object
* `data/syllables.txt`: Top 300 syllable like objects sorted by frequency and then by dictionary order used for recording the dataset

## Instructions

#### Installing dependencies

```
# Initialize and activate a Python virtual environment (optional).
$ python -m venv .venv

# Activate the initialized virtual environment according to your shell (only if using virtual environment).
$ source ./.venv/bin/activate

# Run the following to install the dependencies.
# Or run your system specific command to install.
$ pip install -r requirements.txt
```

#### Generating speech

1. Write the text you want it to speak in `data/test.txt`.
2. Run `python stitch.py` to save the generate speeches to `data/1.wav`, `data/2.wav`, `data/3.wav`, and `data/4.wav` using all 4 techniques.

#### Syllable frequency analysis (already done, DO NOT do it as the new generated order may not match the saved speech samples)

```
# Generate the frequency.json and syllables.txt files in ./data
$ python main.py

# Generate the split audio units in ./data/devanagari_syllable_dataset_split
$ python audio.py

# Play the audio fragments inside `./data/devanagari_syllable_dataset_split`
```

## Dev Instructions

```
$ uv venv
$ source ./.venv/bin/activate
$ uv pip compile pyproject.toml -o requirements.txt
$ uv pip sync requirements.txt
```
