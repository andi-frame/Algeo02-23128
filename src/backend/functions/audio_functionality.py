import audio
import wav_to_midi
from io import BytesIO
from tempfile import TemporaryDirectory


def build_audio_database_from_blobs(midi_blobs):
    """
    1. Accepts a list of blobs or file-like objects for MIDI files.
    2. Processes each file and appends the result with its name to a result array.
    3. Returns the result array.
    """
    database = []
    for midi_blob in midi_blobs:
        filename = midi_blob.filename
        print(f"Processing MIDI file: {filename}")
        with BytesIO(midi_blob.read()) as midi_data:
            processed_data = audio.process(midi_data)
            database.append({'name': filename, 'data': processed_data})

    return database


def build_audio_database_from_wav_blobs(wav_blobs):
    """
    1. Accepts a list of blobs or file-like objects for WAV files.
    2. Converts each WAV to MIDI using `wav_to_midi`.
    3. Processes the resulting MIDI files using `build_audio_database_from_blobs`.
    4. Returns the database array.
    """
    midi_blobs = []

    with TemporaryDirectory() as temp_dir:
        for wav_blob in wav_blobs:
            filename = wav_blob.filename
            print(f"Converting WAV file to MIDI: {filename}")
            midi_path = f"{temp_dir}/{filename.replace('.wav', '.mid')}"
            with BytesIO(wav_blob.read()) as wav_data:
                wav_to_midi.wav_to_midi(wav_data, midi_path)
            
            # Read back the converted MIDI file as a blob
            with open(midi_path, 'rb') as midi_file:
                midi_blobs.append(BytesIO(midi_file.read()))
                midi_blobs[-1].filename = filename.replace('.wav', '.mid')

    return build_audio_database_from_blobs(midi_blobs)


def audio_query(database, query_blob):
    """
    1. Accepts a database array and a query blob for a MIDI file.
    2. Processes the query MIDI file.
    3. Iterates through the database to calculate similarity with each entry.
    4. Sorts the results by similarity score.
    5. Returns the sorted result array.
    """
    filename = query_blob.filename
    print(f"Processing query MIDI file: {filename}")
    with BytesIO(query_blob.read()) as query_data:
        query_processed = audio.process(query_data)

    results = []
    for entry in database:
        similarity_score = audio.calculate_similarity(query_processed, entry['data'])
        results.append({'name': entry['name'], 'similarity': similarity_score})

    sorted_results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    return sorted_results

def wav_to_vector(wav_blob):
    midi_blob = wav_to_midi.wav_to_midi(wav_blob)
    return audio.process(midi_blob)


# if __name__ == "__main__":
#     audioDB = build_audio_database_from_wav("test/TestAudio")
#     print(audioDB)
#     wav_to_midi.wav_to_midi("test/tes01.wav", "test/tes01.mid")
#     queryResult = audio_query(audioDB, "test/tes01.mid")
#     print("Query Results:")
#     for result in queryResult:
#         print(f"File: {result['name']}, Similarity: {result['similarity']:.4f}")
