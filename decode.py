from typing import List

import numpy as np
from pypianoroll import Multitrack, Track
import pretty_midi
from pretty_midi import Instrument, PrettyMIDI
import matplotlib.pyplot as plt


def ndarray_to_midi(
    array: np.ndarray,
    programs: List[int],
    is_drums: List[bool],
    track_names: List[str],
    tempo: int,
    lowest_pitch: int,
    is_zero_one: bool,
) -> PrettyMIDI:
    """convert pianoroll ndarray into PrettyMIDI

    Args:
        array (np.ndarray): pianoroll array.
            shape=(tracks, measures, measure_resolution, pitches)
        is_zero_one (bool): whether pianoroll array is zero_one array.
            if False, each elements is used as velocity(0-127)
        programs (List[int]): MIDI program numbers
        is_drums (List[bool]): whether each track is drums
        track_names (List[str]): track names
        tempo (int): tempo
        lowest_pitch (int): lowest pitch in MIDI note number

    Returns:
        PrettyMIDI: converted MIDI song as Pretty MIDI
    """
    # TODO: implement


if __name__ == '__main__':
    n_measures = 4
    measure_resolution = 24
    n_pitches = 88
    lowest_pitch = 21

    programs = [0, 0, 33,]
    is_drums = [True, False, False,]
    track_names = [
        "Drums",
        "Piano",
        "Bass",
    ]
    n_tracks = len(programs)

    tempo = 100
    is_zero_one = True

    pianoroll = np.zeros((
        n_tracks, n_measures, measure_resolution, n_pitches,
    ))

    # dummy song
    pianoroll[0, :, ::24, 3] = 1  # kick
    pianoroll[0, :, ::12, 9] = 1  # close hat
    pianoroll[1, :, :-6, 51] = 1  # piano
    pianoroll[1, :, :-6, 55] = 1  # piano
    pianoroll[2, :, :-6, 15] = 1  # bass

    mid = ndarray_to_midi(
        array=pianoroll,
        programs=programs,
        is_drums=is_drums,
        track_names=track_names,
        tempo=tempo,
        lowest_pitch=lowest_pitch,
        is_zero_one=is_zero_one,
    )
