import mido
from collections import defaultdict

def detect_melody_channel(midi_file):
    """
    Detects the main melody channel in a MIDI file based on the most active channel.

    Args:
        midi_file (str): Path to the MIDI file.

    Returns:
        int: Channel number of the main melody.
    """
    midi = mido.MidiFile(midi_file)
    channel_note_count = defaultdict(int)
    for track in midi.tracks:
        for msg in track:
            if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
                channel_note_count[msg.channel] += 1
    melody_channel = max(channel_note_count, key=channel_note_count.get, default=0)
    return melody_channel

import mido

def midi_to_pitch_array_with_tempo(midi_file):
    """
    Converts a MIDI file to an array of pitches per quarter note and retrieves tempo in BPM.
    Automatically detects the melody channel.

    Args:
        midi_file (str): Path to the MIDI file.

    Returns:
        tuple:
            - list: Array of pitches where arr[i] is the pitch at quarter beat i.
            - float: Tempo in BPM.
            - int: ticks_per_beat for the MIDI file.
    """
    midi = mido.MidiFile(midi_file)
    melody_channel = detect_melody_channel(midi_file)
    print(f"Detected melody channel: {melody_channel}")
    default_tempo = 500000
    tempo = default_tempo
    current_beat = 0
    quarter_pitches = []

    for track in midi.tracks:
        for msg in track:
            if msg.is_meta and msg.type == 'set_tempo':
                tempo = msg.tempo
            if not msg.is_meta and hasattr(msg, 'time'):
                delta_seconds = mido.tick2second(msg.time, midi.ticks_per_beat, tempo)
                current_beat += delta_seconds * (8 / (60 / (60 * 1_000_000 / tempo)))
                if msg.type == 'note_on' and msg.velocity > 0 and msg.channel == melody_channel:
                    quarter_pitches.append((current_beat, msg.note))
    
    if not quarter_pitches:
        print("No pitches detected in the MIDI file.")
        return [], 60 * 1_000_000 / tempo, midi.ticks_per_beat
    
    # Find the max quarter note
    max_quarter_beat = int(round(max(quarter for quarter, _ in quarter_pitches)))
    pitch_array = [-1] * (max_quarter_beat + 1)

    # Populate pitch array for each quarter note
    for quarter, pitch in quarter_pitches:
        idx = int(round(quarter))
        if idx < len(pitch_array):
            pitch_array[idx] = pitch
    
    bpm = 60 * 1_000_000 / tempo
    return pitch_array, bpm, midi.ticks_per_beat

def normalize_pitches(pitch_array, min_pitch=21, max_pitch=108):
    """
    Normalize pitch values to a specified range.
    
    Args:
        pitch_array (list): List of pitch values (e.g., MIDI notes).
        min_pitch (int): The minimum pitch value (e.g., MIDI note A0).
        max_pitch (int): The maximum pitch value (e.g., MIDI note C8).
        
    Returns:
        list: Normalized pitch values.
    """
    min_input_pitch = min(p for p in pitch_array if p != -1) 
    max_input_pitch = max(p for p in pitch_array if p != -1)
    if min_input_pitch == max_input_pitch:
        return []
    normalized_pitches = []
    for pitch in pitch_array:
        if pitch != -1:
            normalized_pitch = min_pitch + (pitch - min_input_pitch) * (max_pitch - min_pitch) / (max_input_pitch - min_input_pitch)
            normalized_pitches.append(int(round(normalized_pitch)))
        else:
            normalized_pitches.append(-1)

    return normalized_pitches

def filter_pitch_array(array):
    result = []
    for x in array:
        if x != -1:
            result.append(x)
    return result

def sliding_window(pitch_per_beat, window_size=20, hop_size=4):
    windows = []
    for i in range(0, len(pitch_per_beat) - window_size + 1, hop_size):
        window = pitch_per_beat[i:i + window_size]
        windows.append(window)
    return windows

def window_to_atb_fuzzy(window, n_semitones=1, fuzziness=0.5):
    """
    Convert a window of pitches to an ATB fuzzy histogram.

    Args:
        window (list of int): Array of pitch values.
        n_semitones (int): Number of semitones for fuzziness.
        fuzziness (float): Fraction of contribution to adjacent bins.

    Returns:
        list: ATB fuzzy histogram with 128 bins.
    """
    atb_hist = [0] * 128
    for pitch in window:
        if 0 <= pitch < 128:
            atb_hist[pitch] += 1
    fuzzy_hist = [0] * len(atb_hist)
    for i in range(len(atb_hist)):
        if atb_hist[i] > 0:
            for offset in range(-n_semitones, n_semitones + 1):
                if 0 <= i + offset < len(atb_hist):
                    contribution = atb_hist[i] * (1 - abs(offset) * fuzziness / n_semitones)
                    fuzzy_hist[i + offset] += contribution

    return fuzzy_hist

def window_to_rtb_fuzzy(window, n_semitones=1, fuzziness=0.5):
    """
    Convert a window of pitches to an RTB fuzzy histogram.

    Args:
        window (list of int): Array of pitch values.
        n_semitones (int): Number of semitones for fuzziness.
        fuzziness (float): Fraction of contribution to adjacent bins.

    Returns:
        list: RTB fuzzy histogram with 255 bins (differences from -127 to 127).
    """
    rtb_hist = [0] * 255
    for i in range(len(window) - 1):
        diff = window[i + 1] - window[i]
        if -127 <= diff <= 127:
            rtb_hist[diff + 127] += 1
    fuzzy_hist = [0] * len(rtb_hist)
    for i in range(len(rtb_hist)):
        if rtb_hist[i] > 0:
            for offset in range(-n_semitones, n_semitones + 1):
                if 0 <= i + offset < len(rtb_hist):
                    contribution = rtb_hist[i] * (1 - abs(offset) * fuzziness / n_semitones)
                    fuzzy_hist[i + offset] += contribution

    return fuzzy_hist


def window_to_ftb_fuzzy(window, n_semitones=1, fuzziness=0.5):
    """
    Convert a window of pitches to an FTB fuzzy histogram.

    Args:
        window (list of int): Array of pitch values.
        n_semitones (int): Number of semitones for fuzziness.
        fuzziness (float): Fraction of contribution to adjacent bins.

    Returns:
        list: FTB fuzzy histogram with 255 bins (differences from -127 to 127).
    """
    if len(window) == 0:
        return [0] * 255

    ftb_hist = [0] * 255
    first_pitch = window[0]
    for pitch in window:
        diff = pitch - first_pitch
        if -127 <= diff <= 127:
            ftb_hist[diff + 127] += 1
    fuzzy_hist = [0] * len(ftb_hist)
    for i in range(len(ftb_hist)):
        if ftb_hist[i] > 0:
            for offset in range(-n_semitones, n_semitones + 1):
                if 0 <= i + offset < len(ftb_hist):
                    contribution = ftb_hist[i] * (1 - abs(offset) * fuzziness / n_semitones)
                    fuzzy_hist[i + offset] += contribution

    return fuzzy_hist

def convert_window_to_histograms(window, n_semitones=1, fuzziness=0.5):
    """
    Convert a window of pitches into ATB, RTB, and FTB fuzzy histograms.

    Args:
        window (list of int): Array of pitch values.
        n_semitones (int): Number of semitones for fuzziness.
        fuzziness (float): Fraction of contribution to adjacent bins.

    Returns:
        dict: A dictionary containing 'ATB', 'RTB', and 'FTB' histograms.
    """
    atb_hist = window_to_atb_fuzzy(window, n_semitones, fuzziness)
    rtb_hist = window_to_rtb_fuzzy(window, n_semitones, fuzziness)
    ftb_hist = window_to_ftb_fuzzy(window, n_semitones, fuzziness)

    return {'ATB': atb_hist, 'RTB': rtb_hist, 'FTB': ftb_hist}

def shrink_atb_histogram(histogram, left=12, right=12):
    """
    Shrinks an ATB histogram to a smaller range based on the mean note.

    Args:
        histogram (list of float): The ATB histogram with 128 bins.
        left (int): The number of semitones to the left of the mean note to keep.
        right (int): The number of semitones to the right of the mean note to keep.

    Returns:
        list of float: The shrunk ATB histogram.
    """
    n_bins = len(histogram)
    total_weight = sum(histogram)
    if total_weight == 0:
        return [0] * (left + 1 + right)
    mean_note = sum(i * histogram[i] for i in range(n_bins)) / total_weight
    center = int(round(mean_note))
    start = max(0, center - left)
    end = min(n_bins, center + right + 1)
    shrunk_hist = [0] * (left + 1 + right)
    for i in range(start, end):
        shrunk_idx = i - (center - left)
        shrunk_hist[shrunk_idx] += histogram[i]
    if start > 0:
        shrunk_hist[0] += sum(histogram[:start])
    if end < n_bins:
        shrunk_hist[-1] += sum(histogram[end:])

    return shrunk_hist


def shrink_rtb_or_ftb_histogram(histogram, left=12, right=12):
    """
    Shrinks an RTB or FTB histogram to a smaller range and discards out-of-range values.

    Args:
        histogram (list of float): The RTB or FTB histogram with 255 bins.
        left (int): The number of semitones to the left of 0 to keep.
        right (int): The number of semitones to the right of 0 to keep.

    Returns:
        list of float: The shrunk RTB or FTB histogram.
    """
    n_bins = len(histogram)
    center = n_bins // 2
    start = max(0, center - left)
    end = min(n_bins, center + right + 1)
    shrunk_hist = histogram[start:end]
    return shrunk_hist


def shrink_histograms(histograms, atb_left=12, atb_right=12, rtb_left=24, rtb_right=24):
    """
    Shrinks ATB, RTB, and FTB histograms.

    Args:
        histograms (dict): Dictionary containing 'ATB', 'RTB', and 'FTB' histograms.
        atb_left (int): Left range for ATB histogram.
        atb_right (int): Right range for ATB histogram.
        rtb_left (int): Left range for RTB and FTB histograms.
        rtb_right (int): Right range for RTB and FTB histograms.

    Returns:
        dict: Dictionary containing shrunk 'ATB', 'RTB', and 'FTB' histograms.
    """
    shrunk_atb = shrink_atb_histogram(histograms['ATB'], left=atb_left, right=atb_right)
    shrunk_rtb = shrink_rtb_or_ftb_histogram(histograms['RTB'], left=rtb_left, right=rtb_right)
    shrunk_ftb = shrink_rtb_or_ftb_histogram(histograms['FTB'], left=rtb_left, right=rtb_right)

    return {'ATB': shrunk_atb, 'RTB': shrunk_rtb, 'FTB': shrunk_ftb}


def cosine_similarity(vec1, vec2):
    """
    Compute the cosine similarity between two vectors.

    Args:
        vec1 (list): First vector.
        vec2 (list): Second vector.

    Returns:
        float: Cosine similarity between the two vectors.
    """
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
    magnitude2 = sum(b ** 2 for b in vec2) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0 

    return dot_product / (magnitude1 * magnitude2)

def calculate_similarity(array1, array2, atb_weight=0.6,rtb_weight=0.2, ftb_weight=0.2):
    """
    Calculate the similarity between two arrays of sets of 3 vectors using weighted cosine similarity.

    Args:
        array1 (list): First array of sets of 3 vectors (ATB, RTB, FTB).
        array2 (list): Second array of sets of 3 vectors (ATB, RTB, FTB).
        atb_weight (float): Weight for ATB similarity.
        rtb_weight (float): Weight for RTB similarity.
        ftb_weight (float): Weight for FTB similarity.

    Returns:
        float: The highest similarity score between the two arrays.
    """
    highest_similarity = 0.0

    for set1 in array1:
        for set2 in array2:
            # Calculate cosine similarity for each histogram type
            atb_similarity = cosine_similarity(set1['ATB'], set2['ATB'])
            rtb_similarity = cosine_similarity(set1['RTB'], set2['RTB'])
            ftb_similarity = cosine_similarity(set1['FTB'], set2['FTB'])
            total_similarity = (
                atb_weight * atb_similarity +
                rtb_weight * rtb_similarity +
                ftb_weight * ftb_similarity
            )
            if total_similarity > highest_similarity:
                highest_similarity = total_similarity

    return highest_similarity

# Example usage:
# similarity_score = calculate_similarity(shrink_vector_1, shrink_vector_2)
# print("Highest similarity score:", similarity_score)
def process(path):
    pitch_array, bpm, ticks_per_beat = midi_to_pitch_array_with_tempo(path)
    filtered = filter_pitch_array(pitch_array)
    print(len(filtered))
    
    window_size = 40
    hop_size = 8
    windows = sliding_window(filtered, window_size=window_size, hop_size=hop_size)
    normalized_windows = [normalize_pitches(window) for window in windows] 
    hists = [convert_window_to_histograms(window) for window in normalized_windows]
    shrink_vector = [shrink_histograms(hist) for hist in hists]
    return shrink_vector

# v1 = process("naruto.mid")
# v2 = process("dewicut10.mid")
# similarity_score = calculate_similarity(v1, v2)
# print("Highest similarity score:", similarity_score)



