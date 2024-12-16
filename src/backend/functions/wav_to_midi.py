# from basic_pitch.inference import predict
# from basic_pitch import ICASSP_2022_MODEL_PATH
# import pretty_midi
# import numpy as np

# # def calculate_tempo(wav_path):
# #     # Get the predicted MIDI data as a PrettyMIDI object
# #     _, midi_data, _ = predict(wav_path, ICASSP_2022_MODEL_PATH)

# #     # Extract onsets from the PrettyMIDI object
# #     onsets = midi_data.get_onsets()

# #     # Calculate the inter-onset intervals (IOI) between successive onsets
# #     iois = np.diff(onsets)

# #     # Estimate the average IOI
# #     avg_ioi = np.mean(iois)  # average time between beats (in seconds)

# #     # Calculate tempo (BPM): tempo is the inverse of the average IOI, converted to minutes
# #     tempo = 60 / avg_ioi if avg_ioi != 0 else 0  # BPM = 60 / IOI (in seconds)

# #     return tempo

# def wav_to_midi(wav_blob):
#     """
#     Converts a WAV blob to a MIDI blob using a prediction model.

#     Args:
#         wav_blob (bytes): WAV data in a binary blob.

#     Returns:
#         bytes: MIDI data as a binary blob.
#     """
#     wav_path = "temp.wav"
#     midi_path = "temp.mid"
#     with open(wav_path, "wb") as f:
#         f.write(wav_blob)
#     _, midi_data, _ = predict(wav_path, ICASSP_2022_MODEL_PATH)
#     midi_file = pretty_midi.PrettyMIDI()
#     instrument = pretty_midi.Instrument(program=0)
#     midi_file.instruments.append(instrument)
#     for note in midi_data.instruments[0].notes:
#         pitch = note.pitch
#         start_time = note.start
#         end_time = note.end
#         instrument.notes.append(pretty_midi.Note(velocity=64, pitch=pitch, start=start_time, end=end_time))
#     midi_file.write(midi_path)
#     with open(midi_path, "rb") as f:
#         midi_blob = f.read()

#     return midi_blob