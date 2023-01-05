import collections
import glob
import random

import numpy as np
import pathlib
import pandas as pd
import pretty_midi
import tensorflow as tf

seed = 42
tf.random.set_seed(seed)
np.random.seed(seed)
temperature = 2.0
num_predictions = 100

# Sampling rate for audio playback
_SAMPLING_RATE = 16000

emotion_0 = "Q1_0vLPYiPN7qY_0.mid"
emotion_1 = "Q2_CxFXrYgdSSI_2.mid"
emotion_2 = "Q3_7JIdJLkJ0S4_1.mid"
emotion_3 = "Q4_3TYeU9idRGI_0.mid"

piano_data_dir = pathlib.Path('data/maestro-v2.0.0')
if not piano_data_dir.exists():
      tf.keras.utils.get_file(
          'maestro-v2.0.0-midi.zip',
          origin='https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0-midi.zip',
          extract=True,
          cache_dir='.', cache_subdir='data',
      )

piano_filenames = glob.glob(str(piano_data_dir/'**/*.mid*'))
piano_sample_file = piano_filenames[random.randint(0,20)]

#################



def mse_with_positive_pressure(y_true: tf.Tensor, y_pred: tf.Tensor):
  mse = (y_true - y_pred) ** 2
  positive_pressure = 10 * tf.maximum(-y_pred, 0.0)
  return tf.reduce_mean(mse + positive_pressure)


def predict_next_note(
        notes: np.ndarray,
        model: tf.keras.Model,
        temperature: float = 1.0) -> int:
    """Generates a note IDs using a trained sequence model."""

    assert temperature > 0

    # Add batch dimension
    inputs = tf.expand_dims(notes, 0)

    predictions = model.predict(inputs)
    pitch_logits = predictions['pitch']
    step = predictions['step']
    duration = predictions['duration']

    pitch_logits /= temperature
    pitch = tf.random.categorical(pitch_logits, num_samples=1)
    pitch = tf.squeeze(pitch, axis=-1)
    duration = tf.squeeze(duration, axis=-1)
    step = tf.squeeze(step, axis=-1)

    # `step` and `duration` values should be non-negative
    step = tf.maximum(0, step)
    duration = tf.maximum(0, duration)

    return int(pitch), float(step), float(duration)

def midi_to_notes(midi_file: str) -> pd.DataFrame:
  pm = pretty_midi.PrettyMIDI(midi_file)
  instrument = pm.instruments[0]
  notes = collections.defaultdict(list)

  # Sort the notes by start time
  sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
  prev_start = sorted_notes[0].start

  for note in sorted_notes:
    start = note.start
    end = note.end
    notes['pitch'].append(note.pitch)
    notes['start'].append(start)
    notes['end'].append(end)
    notes['step'].append(start - prev_start)
    notes['duration'].append(end - start)
    prev_start = start

  return pd.DataFrame({name: np.array(value) for name, value in notes.items()})


happy_model = tf.keras.models.load_model(r'0',
                                             custom_objects={'mse_with_positive_pressure':mse_with_positive_pressure})
angry_model = tf.keras.models.load_model(r'1',
                                             custom_objects={'mse_with_positive_pressure':mse_with_positive_pressure})
calm_model = tf.keras.models.load_model(r'2',
                                             custom_objects={'mse_with_positive_pressure':mse_with_positive_pressure})
sad_model = tf.keras.models.load_model(r'3',
                                             custom_objects={'mse_with_positive_pressure':mse_with_positive_pressure})

piano_raw_notes = midi_to_notes(piano_sample_file)

def notes_to_midi(
        notes: pd.DataFrame,
        out_file: str,
        instrument_name: str,
        velocity: int = 100,  # note loudness
) -> pretty_midi.PrettyMIDI:
    pm = pretty_midi.PrettyMIDI()
    if instrument_name == "Acoustic Grand Piano":

        instrument = pretty_midi.Instrument(
            program=pretty_midi.instrument_name_to_program(
                instrument_name))

    elif instrument_name == "Midi Drums":
        instrument = pretty_midi.Instrument(program=0, is_drum=True, name="Midi Drums")

    prev_start = 0
    for i, note in notes.iterrows():
        start = float(prev_start + note['step'])
        end = float(start + note['duration'])
        note = pretty_midi.Note(
            velocity=velocity,
            pitch=int(note['pitch']),
            start=start,
            end=end,
        )
        instrument.notes.append(note)
        prev_start = start

    pm.instruments.append(instrument)
    pm.write(out_file)
    return pm


def generate_emotion_music(type,length = 130,randomness = 2.0):

    key_order = ['pitch', 'step', 'duration']
    seq_length = 25
    vocab_size = 128


    if(type == "0"):
        model = happy_model
        raw_notes = midi_to_notes(emotion_0)
    elif (type == "1"):
        model = angry_model
        raw_notes = midi_to_notes(emotion_1)
    elif (type == "2"):
        model = calm_model
        raw_notes = midi_to_notes(emotion_2)
    else:
        model = sad_model
        raw_notes = midi_to_notes(emotion_3)


    sample_notes = np.stack([raw_notes[key] for key in key_order], axis=1)

    input_notes = (
        sample_notes[:seq_length] / np.array([vocab_size, 1, 1]))

    generated_notes = []
    prev_start = 0
    for _ in range(length):
      pitch, step, duration = predict_next_note(input_notes, model, randomness)
      start = prev_start + step
      end = start + duration
      input_note = (pitch, step, duration)
      generated_notes.append((*input_note, start, end))
      input_notes = np.delete(input_notes, 0, axis=0)
      input_notes = np.append(input_notes, np.expand_dims(input_note, 0), axis=0)
      prev_start = start

    generated_notes = pd.DataFrame(
        generated_notes, columns=(*key_order, 'start', 'end'))
    return generated_notes


def generate_emotional_music(filename,length = 130,randomness = 2.0,type='0'):
    out_file = filename
    generated_notes = generate_emotion_music(type,length,randomness)
    notes_to_midi(
        generated_notes, out_file=out_file, instrument_name="Acoustic Grand Piano")
    return True


