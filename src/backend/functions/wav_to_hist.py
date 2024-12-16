import librosa
import numpy as np

def extract_features_from_wav(file_path, hop_length=512):
    y, sr = librosa.load(file_path, sr=None)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []
    for mag, pitch in zip(magnitudes.T, pitches.T):
        if mag.max() > 0.1:
            index = mag.argmax()
            pitch_values.append(pitch[index])
        else:
            pitch_values.append(0)
    smoothed_pitch = smooth_pitch(np.array(pitch_values))
    midi_notes = np.round(librosa.hz_to_midi(smoothed_pitch))
    return midi_notes

def smooth_pitch(pitch_array, window_size=5):
    if window_size == 0:
        return pitch_array
    return np.convolve(pitch_array, np.ones(window_size) / window_size, mode='same')

def pitches_per_beat(file_path, hop_length=512):
    y, sr = librosa.load(file_path, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    midi_notes = extract_features_from_wav(file_path, hop_length=hop_length)
    pitch_per_beat = []
    for i in range(len(beat_frames) - 1):
        start, end = beat_frames[i], beat_frames[i + 1]
        avg_pitch = np.mean(midi_notes[start:end])
        pitch_per_beat.append(np.round(avg_pitch) if avg_pitch > 0 else 0)
    
    return pitch_per_beat, tempo

def sliding_window(pitch_per_beat, window_size=20, hop_size=4):
    windows = []
    for i in range(0, len(pitch_per_beat) - window_size + 1, hop_size):
        window = pitch_per_beat[i:i + window_size]
        windows.append(window)
    return np.array(windows)

def normalize_window(window):
    window_mean = np.mean(window)
    window_std = np.std(window)
    if window_std == 0:
        return [0] * len(window)
    return [(note - window_mean) / window_std for note in window]

def compute_fuzzy_atb_histograms(windows, bins, range_min, range_max):
    histograms = []
    bin_edges = np.linspace(range_min, range_max, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    for window in windows:
        hist = np.zeros(bins)
        for value in window:
            if range_min <= value <= range_max:
                for i, center in enumerate(bin_centers):
                    distance = abs(value - center)
                    if distance < (bin_edges[1] - bin_edges[0]):
                        weight = 1 - (distance / (bin_edges[1] - bin_edges[0]))
                        hist[i] += weight
        histograms.append(hist)
    
    return histograms

def compute_fuzzy_rtb_histograms(windows, bins, range_min, range_max):
    histograms = []
    bin_edges = np.linspace(range_min, range_max, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    for window in windows:
        hist = np.zeros(bins)
        for i in range(1, len(window)):
            difference = window[i] - window[i-1]
            if range_min <= difference <= range_max:
                for j, center in enumerate(bin_centers):
                    distance = abs(difference - center)
                    if distance < (bin_edges[1] - bin_edges[0]):
                        weight = 1 - (distance / (bin_edges[1] - bin_edges[0]))
                        hist[j] += weight
        histograms.append(hist)
    
    return histograms

def compute_fuzzy_ftb_histograms(windows, bins, range_min, range_max):
    histograms = []
    bin_edges = np.linspace(range_min, range_max, bins + 1)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    for window in windows:
        hist = np.zeros(bins)
        first_note = window[0]
        for value in window:
            difference = value - first_note
            if range_min <= difference <= range_max:
                for i, center in enumerate(bin_centers):
                    distance = abs(difference - center)
                    if distance < (bin_edges[1] - bin_edges[0]):
                        weight = 1 - (distance / (bin_edges[1] - bin_edges[0]))
                        hist[i] += weight
        histograms.append(hist)
    
    return histograms


# def cosine_similarity(hist1, hist2):
#     if len(hist1) != len(hist2):
#         raise ValueError("Histograms must have the same length")

#     return 1 - cosine(hist1, hist2)

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


# def compare_wav_files(file1, file2):
#     arr1, tempo1 = pitches_per_beat(file1)
#     arr2, tempo2 = pitches_per_beat(file2)
#     print(len(arr1))
#     print(len(arr2))
#     windows1 = sliding_window(arr1, window_size=40, hop_size=8)
#     windows2 = sliding_window(arr2, window_size=40, hop_size=8)
#     normalized_windows1 = [normalize_window(window) for window in windows1]
#     normalized_windows2 = [normalize_window(window) for window in windows2]
#     atb_histograms1 = compute_fuzzy_atb_histograms(normalized_windows1, bins=128, range_min=-64, range_max=64)
#     atb_histograms2 = compute_fuzzy_atb_histograms(normalized_windows2, bins=128, range_min=-64, range_max=64)

#     rtb_histograms1 = compute_fuzzy_rtb_histograms(normalized_windows1, bins=256, range_min=-128, range_max=128)
#     rtb_histograms2 = compute_fuzzy_rtb_histograms(normalized_windows2, bins=256, range_min=-128, range_max=128)

#     ftb_histograms1 = compute_fuzzy_ftb_histograms(normalized_windows1, bins=256, range_min=-128, range_max=128)
#     ftb_histograms2 = compute_fuzzy_ftb_histograms(normalized_windows2, bins=256, range_min=-128, range_max=128)
#     similarity_atb = aggregate_similarity(atb_histograms1, atb_histograms2)
#     similarity_rtb = aggregate_similarity(rtb_histograms1, rtb_histograms2)
#     similarity_ftb = aggregate_similarity(ftb_histograms1, ftb_histograms2)
#     overall_similarity = 0.3 * similarity_atb + 0.5 * similarity_rtb + 0.2 * similarity_ftb
#     return {
#         "ATB": similarity_atb,
#         "RTB": similarity_rtb,
#         "FTB": similarity_ftb,
#         "Overall": overall_similarity
#     }
# file1 = "soj.wav"
# file2 = "dewi.wav"
# similarity = compare_wav_files(file1, file2)
# print("Similarity scores:", similarity)
