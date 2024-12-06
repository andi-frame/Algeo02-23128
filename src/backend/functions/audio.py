from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
def wav_to_midi(wav_path):
    _, midi_data, _ = predict(wav_path, ICASSP_2022_MODEL_PATH)
    return midi_data

def extract_channel_1(midi_data):
    melody = []
    for instrument in midi_data.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                melody.append((note.pitch, note.start, note.end))
            break
    return melody
    
def windowing(melody, window_size=40, step_size=8):
    windows = []
    melody_length = len(melody)
    for i in range(0, melody_length - window_size + 1, step_size):
        window = melody[i:i + window_size]
        windows.append(window)
    return windows

def get_mean(pitches):
    if not pitches:
        return 0  
    return sum(pitches) / len(pitches)


def get_std_dev(pitches):
    if not pitches:
        return 0
    mean = get_mean(pitches)
    variance = sum((pitch - mean) ** 2 for pitch in pitches) / len(pitches)
    return variance ** (1/2)

def normalize_pitch(segment):
    pitches = [note[0] for note in segment]
    mean = get_mean(pitches)
    std_dev = get_std_dev(pitches)
    normalized_pitches = [((pitch - mean) / std_dev) for pitch in pitches]
    normalized_segment = [(normalized_pitches[i], segment[i][1], segment[i][2]) for i in range(len(segment))]
    return normalized_segment

def normalize_tempo(segment, target_duration):
    total_duration = sum(note[2] - note[1] for note in segment)
    scale_factor = target_duration / total_duration
    normalized = [(note[0], note[1] * scale_factor, note[2] * scale_factor) for note in segment]
    return normalized

def normalize_melody(segment, target_duration):
    normalized_pitch_segment = normalize_pitch(segment)
    normalized_melody = normalize_tempo(normalized_pitch_segment, target_duration)
    return normalized_melody

def get_atb_histogram(melody):
    histogram = [0] * 128
    for note in melody:
        pitch = note[0]  # (pitch, start_time, end_time)
        if 0 <= pitch < 128:
            histogram[pitch] += 1

    total_notes = sum(histogram)
    if total_notes > 0:
        histogram = [count / total_notes for count in histogram]
    return histogram

def get_rtb_histogram(melody):
    histogram = [0] * 255
    for i in range(1, len(melody)):
        pitch_prev = melody[i-1][0]
        pitch_curr = melody[i][0]
        interval = pitch_curr - pitch_prev
        bin_index = interval + 127
        if 0 <= bin_index < 255: 
            histogram[bin_index] += 1

    total_intervals = sum(histogram)
    if total_intervals > 0:
        histogram = [count / total_intervals for count in histogram]
    return histogram

def get_ftb_histogram(melody):
    histogram = [0] * 255
    if len(melody) == 0:
        return histogram
    
    pitch_first = melody[0][0]
    for i in range(len(melody)):
        pitch_curr = melody[i][0]
        interval = pitch_curr - pitch_first  
        bin_index = interval + 127
        if 0 <= bin_index < 255:
            histogram[bin_index] += 1

    total_intervals = sum(histogram)
    if total_intervals > 0:
        histogram = [count / total_intervals for count in histogram]
    
    return histogram

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sum(a ** 2 for a in vector_a) ** 0.5
    magnitude_b = sum(b ** 2 for b in vector_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0  
    
    return dot_product / (magnitude_a * magnitude_b)

def aggregate_similarity(windows_a, windows_b):
    if not windows_a or not windows_b:
        return 0.0  
    
    total_similarity = 0
    count = 0
    
    for vector_a in windows_a:
        for vector_b in windows_b:
            total_similarity += cosine_similarity(vector_a, vector_b)
            count += 1
    
    return total_similarity / count if count > 0 else 0.0



# # fungsi proses
# midi_obj = wav_to_midi(r"E:\Syafiq\3rd Semester\Algeo\TUBES 2\doremi.wav")
# channel_1 = extract_channel_1(midi_obj)
# windows = windowing(channel_1, 40, 8)
# normalized_windows = [normalize_melody(window, 1) for window in windows]
# atb_vectors = [get_atb_histogram(window) for window in normalized_windows]
# rtb_vectors = [get_rtb_histogram(window) for window in normalized_windows]
# ftb_vectors = [get_ftb_histogram(window) for window in normalized_windows]

# # similarity
# atb_similarity = aggregate_similarity(atb_vectors, atb_vectors)
# rtb_similarity = aggregate_similarity(rtb_vectors, rtb_vectors)
# ftb_similarity = aggregate_similarity(ftb_vectors, ftb_vectors)


# total_similarity = atb_similarity*0.3 + rtb_similarity*0.5 + ftb_similarity*0.2


# print(midi_obj)  
# print("\n")
# print(channel_1)
# print("\n")

# for window in windows :
#     print(window)
#     print("\n")

# for window in normalized_windows :
#     print(window)
#     print("\n")

# print("TOTAL SIMILARITY : ")
# print(total_similarity)


# print(channel_1)