from typing import List
import argparse

import numpy as np
from pypianoroll import Multitrack, StandardTrack
from pretty_midi import PrettyMIDI


MIDI_MAX_PITCHES = 128
DEFAULT_VELOCITY = 80


def ndarray_to_midi(
    array: np.ndarray,
    is_velocity_zero_one: bool,
    programs: List[int],
    is_drums: List[bool],
    track_names: List[str],
    tempo: int,
    beat_resolution: int,
    lowest_pitch: int,
) -> PrettyMIDI:
    """convert pianoroll ndarray into PrettyMIDI

    Args:
        array (np.ndarray): pianoroll array.
            shape=(tracks, timesteps, pitches)
            smaller index means lower note.
        is_velocity_zero_one (bool): whether pianoroll array is zero_one array.
            if False, each elements is used as velocity(0-127)
        programs (List[int]): MIDI program numbers
        is_drums (List[bool]): whether each track is drums
        track_names (List[str]): track names
        tempo (int): tempo
        beat_resolution (int): timesteps per beat
        lowest_pitch (int): lowest pitch in MIDI note number

    Returns:
        PrettyMIDI: converted MIDI song as Pretty MIDI
    """
    if (array.ndim != 3):
        raise ValueError("Invalid shape of input array.")
    n_tracks, n_timesteps, n_pitches = array.shape
    # arguments validation
    if ((n_tracks != len(programs)) or
            (n_tracks != len(is_drums)) or
            (n_tracks != len(track_names))):
        raise ValueError(
            "tracks count is differ from each arguments.\n"
            f"array: {n_tracks}\n"
            f"programs: {len(programs)}\n"
            f"is_drums: {len(is_drums)}\n"
            f"trask_names: {len(track_names)}\n"
        )
    if (is_velocity_zero_one):
        array *= DEFAULT_VELOCITY

    tempo_array = np.full((n_timesteps, 1), tempo)

    tracks = []
    # create each track
    for i_track, (program, is_drum, track_name) in \
            enumerate(zip(programs, is_drums, track_names)):
        # pad so that pitches is 128
        pianoroll = np.pad(
            array[i_track],
            ((0, 0),
             (lowest_pitch, MIDI_MAX_PITCHES - lowest_pitch - n_pitches),),
            mode="constant",
            constant_values=0,

        )
        tracks.append(
            StandardTrack(
                name=track_name,
                program=program,
                is_drum=is_drum,
                pianoroll=pianoroll,))
    multitrack = Multitrack(
        tracks=tracks,
        tempo=tempo_array,
        resolution=beat_resolution,
    )
    return multitrack.to_pretty_midi()


def export_midi_from_lpd_npy():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_npy", type=str, required=True)
    parser.add_argument("-o", "--output_midi", type=str, required=True)
    args = parser.parse_args()

    pianoroll = np.load(args.input_npy).astype(np.int64)
    pianoroll = pianoroll.transpose(3, 0, 1, 2)
    pianoroll = pianoroll.reshape(pianoroll.shape[0], -1, pianoroll.shape[-1])

    mid = ndarray_to_midi(
        array=pianoroll,
        is_velocity_zero_one=True,
        programs=(0, 0, 25, 33, 48),
        is_drums=[True, False, False, False, False,],
        track_names=["Drums", "Piano", "Guitar", "Bass", "Strings",],
        tempo=100,
        beat_resolution=12,
        lowest_pitch=25,
    )
    mid.write(args.output_midi)


def debug():
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
    pianoroll[0, :, ::24, 15] = 1  # kick
    pianoroll[0, :, ::12, 21] = 1  # close hat
    pianoroll[1, :, :-6, 51] = 1  # piano
    pianoroll[1, :, :-6, 55] = 1  # piano
    pianoroll[1, :, :-6, 27] = 1  # piano
    pianoroll[2, :, :-6, 15] = 1  # bass

    pianoroll = pianoroll.reshape((
        n_tracks, n_measures * measure_resolution, n_pitches))

    mid = ndarray_to_midi(
        array=pianoroll,
        programs=programs,
        is_drums=is_drums,
        track_names=track_names,
        tempo=tempo,
        lowest_pitch=lowest_pitch,
        is_velocity_zero_one=is_zero_one,
        beat_resolution=measure_resolution / n_measures,
    )
    mid.write("test.mid")


if __name__ == '__main__':
    export_midi_from_lpd_npy()
