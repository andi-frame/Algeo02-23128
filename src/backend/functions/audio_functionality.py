import os
import shutil
import audio
import backend.functions.wav_to_midi as wav_to_midi
from io import BytesIO
from tempfile import TemporaryDirectory


def build_audio_database(folderpath):
    """
    1. Get folder of .mid files from folderpath
    2. Use process() on each .mid file and append the result with its name to a result array
    3. Return result array
    """
    database = []
    for filename in os.listdir(folderpath):
        if filename.endswith('.mid'):
            filepath = os.path.join(folderpath, filename)
            print(f"Processing MIDI file: {filename}")
            processed_data = audio.process(filepath)
            database.append({'name': filename, 'data': processed_data})

    return database



def audio_query(database, query_path):
    """
    1. Use process() on query_path (.mid)
    2. Iterate through database to get each element's similarity with query, then append the result with its name to a result array
    3. Sort the result
    4. Return the sorted result
    """
    print(f"Processing query MIDI file: {query_path}")
    query_data = audio.process(query_path)
    results = []
    for entry in database:
        similarity_score = audio.calculate_similarity(query_data, entry['data'])
        results.append({'name': entry['name'], 'similarity': similarity_score})
    sorted_results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    return sorted_results

def path_to_blob(midi_path):
    """
    Converts a MIDI file path to a binary blob.

    Args:
        midi_path (str): Path to the MIDI file.

    Returns:
        bytes: Binary data of the MIDI file.
    """
    with open(midi_path, 'rb') as f:
        return f.read()

def process_wav_blob(blob):
    midi_blob = wav_to_midi.wav_to_midi(blob)
    return audio.process(midi_blob)

# print(process_wav_blob(path_to_blob("src/backend/functions/tes01.wav")))

# audio.process(path_to_blob("src/backend/functions/dewicut10.mid"))
#print(audio.process("src/backend/functions/dewicut10.mid"))

# def build_audio_database_from_wav(folder_path):
#     """
#     1. Get folder of .wav files from folderpath
#     2. Convert each .wav to .mid and save all in a folder
#     3. Use build_audio_database on that newly created folder
#     """
#     midi_folder = os.path.join(folder_path, 'converted_midis')
#     os.makedirs(midi_folder, exist_ok=True)
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.wav'):
#             wav_path = os.path.join(folder_path, filename)
#             midi_path = os.path.join(midi_folder, f"{os.path.splitext(filename)[0]}.mid")
#             print(f"Converting WAV file to MIDI: {filename}")
#             wav_to_midi.wav_to_midi(wav_path, midi_path)
#     database = build_audio_database(midi_folder)
#     shutil.rmtree(midi_folder)

#     return database

# if __name__ == "__main__":
#     audioDB = build_audio_database_from_wav("test/TestAudio")
#     print(audioDB)
#     wav_to_midi.wav_to_midi("test/tes01.wav", "test/tes01.mid")
#     queryResult = audio_query(audioDB, "test/tes01.mid")
#     print("Query Results:")
#     for result in queryResult:
#         print(f"File: {result['name']}, Similarity: {result['similarity']:.4f}")
