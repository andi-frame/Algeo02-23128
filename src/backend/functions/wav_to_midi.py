from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
import pretty_midi
import numpy as np

def calculate_tempo(wav_path):
    # Get the predicted MIDI data as a PrettyMIDI object
    _, midi_data, _ = predict(wav_path, ICASSP_2022_MODEL_PATH)

    # Extract onsets from the PrettyMIDI object
    onsets = midi_data.get_onsets()

    # Calculate the inter-onset intervals (IOI) between successive onsets
    iois = np.diff(onsets)

    # Estimate the average IOI
    avg_ioi = np.mean(iois)  # average time between beats (in seconds)

    # Calculate tempo (BPM): tempo is the inverse of the average IOI, converted to minutes
    tempo = 60 / avg_ioi if avg_ioi != 0 else 0  # BPM = 60 / IOI (in seconds)

    return tempo

def wav_to_midi(wav_path, midi_path):
    # Calculate the tempo from the audio
    tempo = calculate_tempo(wav_path)
    print(f"Estimated tempo: {tempo} BPM")

    # Get the predicted MIDI data as a PrettyMIDI object
    _, midi_data, _ = predict(wav_path, ICASSP_2022_MODEL_PATH)

    # Create a new PrettyMIDI object to hold the final result
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

    # Add a tempo change at time 0
    # midi_file.notes.append(pretty_midi('set_tempo', tempo=int(tempo * 1000)))# Set tempo at time 0 in the track

    # Save the MIDI file
    midi_file.write(midi_path)

# Example usage
# wav_to_midi('dewi.wav', 'dewi.mid')
