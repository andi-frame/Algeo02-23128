from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import pretty_midi
from io import BytesIO
import numpy as np


def calculate_tempo(wav_blob):
    """
    Calculate the tempo of a WAV audio file represented as a blob.
    """
    # Load WAV data from blob
    wav_blob.seek(0)  # Ensure the blob is at the start
    wav_path = BytesIO(wav_blob.read())

    # Get the predicted MIDI data as a PrettyMIDI object
    _, midi_data, _ = predict(wav_path, ICASSP_2022_MODEL_PATH)

    # Extract onsets from the PrettyMIDI object
    onsets = midi_data.get_onsets()

    # Calculate inter-onset intervals (IOI) and tempo
    iois = np.diff(onsets)
    avg_ioi = np.mean(iois) if len(iois) > 0 else 0
    tempo = 60 / avg_ioi if avg_ioi != 0 else 0  # BPM

    return tempo


def wav_to_midi(wav_blob):
    """
    Converts a WAV audio blob to a MIDI blob.
    """
    # Calculate the tempo from the audio blob
    tempo = calculate_tempo(wav_blob)
    print(f"Estimated tempo: {tempo} BPM")

    # Reload the WAV blob for conversion
    wav_blob.seek(0)  # Reset to the beginning
    wav_path = BytesIO(wav_blob.read())

    # Get the predicted MIDI data as a PrettyMIDI object
    _, midi_data, _ = predict(wav_path, ICASSP_2022_MODEL_PATH)

    # Create a new PrettyMIDI object
    midi_file = pretty_midi.PrettyMIDI()

    # Create an Instrument instance (Program 0 is usually piano)
    instrument = pretty_midi.Instrument(program=0)
    midi_file.instruments.append(instrument)

    # Add notes to the MIDI track
    for note in midi_data.instruments[0].notes:
        pitch = note.pitch
        start_time = note.start
        end_time = note.end
        instrument.notes.append(pretty_midi.Note(velocity=64, pitch=pitch, start=start_time, end=end_time))

    # Save the MIDI data to a blob
    midi_blob = BytesIO()
    midi_file.write(midi_blob)
    midi_blob.seek(0)  # Reset the blob to the beginning

    return midi_blob
