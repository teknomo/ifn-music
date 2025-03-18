import numpy as np
import pyaudio
import soundfile as sf
import re
import scipy
import os
from PitchNote import PitchNote
from fractions import Fraction
import keyboard
import threading
from MusicManager import MusicManager

class Music():
    # -------------------------------------------------------------------------------------------------
    # Music Class
    # Play Musical Notes and Save it to Wave File.
    #
    # Copyright (c) 2025 Kardi Teknomo/Revoledu.com
    # All rights reserved.
    #
    # This software is provided "as is," without warranty of any kind, express or implied, including
    # but not limited to the warranties of merchantability, fitness for a particular purpose, and
    # non-infringement. In no event shall the authors or copyright holders be liable for any claim,
    # damages, or other liability, whether in an action of contract, tort, or otherwise, arising
    # from, out of, or in connection with the software or the use or other dealings in the software.
    #
    # Version: 0.1.3
    # Date: 09 March 2025
    # -------------------------------------------------------------------------------------------------
    def __init__(self, time_signature="4/4", isPrint = True):        
        self.is_print = isPrint
        self.set_time_signature(time_signature)
        self.version = "0.1.3"
        
        self.stop_playback = False
        self.note_handle = PitchNote()
        self.manager = MusicManager("music_data.json")
        self.manager.load_data()
        
        
    def _parse_time_signature(self):
        """Convert time signature to beats per measure"""
        numerator, denominator = map(int, self.time_signature.split('/'))
        return Fraction(numerator, denominator)
    
    
    def set_time_signature(self, time_signature):
        '''
        set time signature and beats per measure
        '''
        self.time_signature = time_signature
        self.beats_per_measure = self._parse_time_signature()
    
    
    """
    #
    #    musical pitch note and its frequency
    
    #    note = pitch / duration
    #    pitch = MIDI + [Chromatic] + Octave
    #    higher tenmpo is faster music
    #    
    """
    

    def pitch_to_freq(self, pitch):
        '''
        Convert the note pitch to its frequency in Hz.
        return the frequency of MIDI note (e.g. note = `C4` or `E#4`, `Ab3` )
        For example, A4 -> 440Hz, etc.
        '''
        if pitch.lower() == "rest":
            return 0.0
        midi = self.note_handle.parse_note(pitch)
        freq = self.note_handle.midi_to_freq(midi)
        return freq
    
    
    def canonize_pitch(self, pitch):
        '''
        return the canonical name of MIDI pitch note
        example: Bbb3 -> A3, Bx3 -> C#3, E#4 -> F4
        '''
        if pitch.lower() == "rest":
            return pitch
        midi = self.note_handle.parse_note(pitch)
        return self.note_handle.midi_to_name(midi)


    def canonize_music(self, music_notes, tempo, time_signature):
        self.set_time_signature(time_signature)       
        measures = self.parse_music(music_notes)
        canonize_notes=""
        for measure in measures:
            for event in self.notes_to_events([measure], tempo):
                if event['type'] == 'note':
                    note=f"{event['pitch']}/{event['note_duration']}"
                elif event['type'] == 'rest':
                    note=f"rest/{event['note_duration']}"
                canonize_notes += note + " "
            canonize_notes +=  " | \n"
        return canonize_notes
    
    
    """
    #
    #    musical waves
    #       waveform determines the instruments
    #       wave <-- frequency + duration + volume
    #    
    """

    def generate_wave(self, frequency, duration, instrument="piano", volume=0.5):
        """
        Generate a waveform (sine or whichever wave for a musical instrument) for the given
        frequency, duration, instrument, volume
        """
        sample_rate=44100
        num_samples = int(sample_rate * duration)
        if num_samples == 0:
            return np.zeros(0, dtype=np.float32)
        
        t = np.linspace(0, duration, num_samples, endpoint=False)
        
        if frequency <= 0:
            return np.zeros(num_samples, dtype=np.float32)

        wave = np.zeros(num_samples)
        
        # Instrument-specific synthesis
        if instrument == "guitar":
            # Physical modeling of plucked string
            noise = np.random.uniform(-1, 1, int(sample_rate*0.01))  # Initial pluck noise
            wave = np.append(noise, np.zeros(num_samples - len(noise)))
            delay = int(sample_rate / frequency)
            
            # Karplus-Strong algorithm approximation
            for i in range(len(noise), num_samples):
                if i - delay >= 0:
                    wave[i] = (wave[i - delay] + wave[i - delay - 1]) * 0.49
            
            # Resonance filter and envelope
            b, a = scipy.signal.butter(2, frequency/(sample_rate/2), btype='low')
            wave = scipy.signal.lfilter(b, a, wave)
            env = np.exp(-t * 8)

        elif instrument == "organ":
            # Additive synthesis with multiple harmonics
            harmonics = [
                (1, 0.6),  # Fundamental
                (2, 0.4),  # Octave
                (3, 0.3),  # Twelfth
                (4, 0.2)   # Double octave
            ]
            for mult, amp in harmonics:
                wave += amp * np.sin(2 * np.pi * frequency * mult * t)
            env = np.ones_like(t)

        elif instrument == "drum":
            # Kick drum synthesis
            freq_sweep = np.linspace(200, 50, num_samples)  # Pitch drop
            wave = np.sin(2 * np.pi * freq_sweep * t)
            wave += 0.5 * np.random.normal(0, 1, num_samples)  # Noise component
            env = np.exp(-t * 25)  # Fast decay

        elif instrument == "bass":
            # FM synthesis for electric bass
            modulator = 0.5 * np.sin(2 * np.pi * 2 * frequency * t)
            carrier = np.sin(2 * np.pi * frequency * t + modulator)
            wave = carrier
            env = np.exp(-t * 4)

        elif instrument == "bell":
            # Inharmonic partials with exponential decay
            partials = [(1, 0.6), (2.76, 0.4), (5.43, 0.3), (8.12, 0.2)]
            for mult, amp in partials:
                wave += amp * np.sin(2 * np.pi * frequency * mult * t) * np.exp(-t * 0.5)
            env = np.exp(-t * 8)

        elif instrument == "angklung":
            # Metallic percussion model
            main = np.sin(2 * np.pi * frequency * t)
            noise = np.random.normal(0, 0.3, num_samples)
            wave = main + noise
            env = np.exp(-t * 20) * (1 - np.cos(2 * np.pi * t * 10))  # Tremolo effect

        elif instrument == "harmonica":
            # Reed vibration with breath noise
            wave = scipy.signal.sawtooth(2 * np.pi * frequency * t * 1.005, 0.5)
            wave += 0.1 * np.random.normal(0, 1, num_samples) * np.exp(-t * 10)
            env = 1 - np.exp(-t * 10)  # Slow attack
        
        elif instrument == "violin":
            wave = (2 * (t * frequency % 1) - 1)
            env = 1 - np.exp(-t * 2)  # Slow attack
        
        elif instrument == "flute":
            # Breath-controlled sine with vibrato
            vibrato = 0.005 * np.sin(2 * np.pi * 6 * t)  # 6Hz vibrato
            wave = np.sin(2 * np.pi * frequency * t * (1 + vibrato))
            breath_noise = 0.05 * np.random.normal(0, 1, num_samples)
            wave += breath_noise * np.exp(-t * 5)
            env = 1 - np.exp(-t * 2)  # Slow attack

        elif instrument == "piano":        
            wave = np.sign(np.sin(2 * np.pi * frequency * t)) # Square wave
            env = np.exp(-t * 8)
        
        else:  # Default to sine wave
            wave = np.sin(2 * np.pi * frequency * t)
            env = np.ones_like(t)

        # Apply amplitude envelope and volume
        wave = np.clip(wave * env * volume, -1.0, 1.0)
        return wave.astype(np.float32)


    def play_wave(self, wave):
        sample_rate=44100
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, output=True)
        stream.write(wave.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()
        p.terminate()


    def music_notes_to_waves(self, music_notes, tempo=120, instrument="piano", volume=0.5):
        """Convert music sequence to audio waves with proper measure validation"""
        self.beats_per_measure = self._parse_time_signature()
        full_wave = np.array([], dtype=np.float32)
        measures = self.parse_music(music_notes)
        
        for event in self.notes_to_events(measures, tempo):
            if event['type'] == 'note':
                wave = self.generate_wave(
                    event['frequency'],
                    event['duration'],
                    instrument=instrument,
                    volume=volume
                )
            else:
                wave = np.zeros(int(44100 * event['duration']), dtype=np.float32)
                
            full_wave = np.append(full_wave, wave)
            
        return full_wave
   
    
    """
    #
    #    musical notes handler
    #
    #       music_notes <-- measures
    #       measures <-- notes
    #       total beats per measure <-- time signature 
    #       note = pitch/duration
    #       duration = number of beats. One beat = 1/4 duration 
    #       pitch = MIDI + [Chromatic] + Octave
    #
    """   
    
    def parse_music(self, music_notes: str):
        """
        Parse standard music notation with measure validation        
        
        Convert a music string of the form:

            "C4/4 E4/4 G4/4 C5/4 | F4/4 F4/4 F4/4 F4/4"

        into a list of measures, each measure is a list of (pitch, duration_in_beats).

        Then check if each measure sums up to the specified beats_per_measure:
          - If less, add a rest to fill the measure.
          - If more, either carry over or warn the user.

        This function returns something like:
        [
          [('C4', 1), ('E4', 1), ('G4', 1), ('C5', 1)],    # measure 1
          [('F4', 1), ('F4', 1), ('F4', 1), ('F4', 1)]     # measure 2
        ]
        # Standard format: "C4/4 D4/4 E4/4 | F4/2 G4/2 | r/4 ..."
        """
        beats_per_measure = self.beats_per_measure # local copy
        
        # Normalize whitespace
        music_notes = music_notes.replace("\n", "").strip()
        music_notes = re.sub(r'\s+', ' ', music_notes.strip())
        # Split by measure bars (assumed separated by '|')
        raw_measures = [m.strip() for m in music_notes.split('|') if m.strip()]
        # pattern = r'([A-Ga-g][#b]?\d+|r|R|rest)/?((?:\d+/?)+)'
        pattern = r'([A-Ga-g][#b]?\d+|[Rr]|rest)/([\d\.]+)'
        
        measures = []
        # for measure in music_notes.split('|'):
        for m_index, measure in enumerate(raw_measures):
            measure = measure.strip()
            if not measure:
                continue
                
            total_duration = Fraction(0)
            notes = []
            
            for note in re.findall(pattern, measure):
                pitch, duration = note
                pitch = pitch.upper()
                
                # Parse duration with support for dotted notes
                dur_parts = sum(Fraction(s) for s in duration.split('+'))
                total_duration += 1/dur_parts.numerator
                
                notes.append({
                    'pitch': pitch,
                    'duration': dur_parts
                })
            
            # # Validate measure duration
            # # Compare measure length to the expected beats_per_measure
            # if total_duration < beats_per_measure:
            #     # Fill in the difference with a rest
            #     needed = beats_per_measure - total_duration
            #     # measures.append((f"rest/{1/needed}"))
            #     notes.append({
            #         'pitch': "rest",
            #         'duration': Fraction(1/needed)
            #     })
            #     print(f"Warning: measure {m_index+1} has {total_duration} below {beats_per_measure} beats. rest/{int(1/needed)} was added")
            #     total_duration += needed
            # elif total_duration > beats_per_measure:
            #     # For a simple approach, just warn user. 
            #     # Or do a partial measure or carry remainder to the next measure, etc.
            #     print(f"Warning: measure {m_index+1} has {total_duration} exceeds {beats_per_measure} beats.")
            
            # if total_duration != beats_per_measure:
            #     raise ValueError(f"Invalid measure: Expected {beats_per_measure}, got {total_duration}")
            
            measures.append(notes)
        return measures
    
    
    def validate_measure(self, measure, beats_per_measure, validation_type='strict'):
        """Validate measure duration against beats per measure."""
        total_duration = Fraction(0)
        for note in measure:
            total_duration += note['duration']

        if validation_type == 'strict':
            # Strict validation, return False if total duration doesn't match beats_per_measure
            if total_duration != beats_per_measure:
                return False
        elif validation_type == 'solve':
            # Solve validation, adjust to fit
            if total_duration < beats_per_measure:
                needed = beats_per_measure - total_duration
                measure.append({
                    'pitch': 'rest',
                    'duration': needed
                })
            elif total_duration > beats_per_measure:
                # Carry overflow to the next measure
                overflow = total_duration - beats_per_measure
                measure.append({
                    'pitch': 'rest',
                    'duration': overflow
                })
                print(f"Warning: measure exceeds {beats_per_measure} beats. Overflow of {overflow} added as rest.")
            return True
        return True

    def align_measures(self, music_notes: str, new_time_signature: str) -> list:
        """
        Resize musical measures according to a new time signature. This method reads the music notes string, 
        and adjusts the measure bars to fit the new beats per measure based on the new time signature. 

        Parameters:
        music_notes (str): A string containing the music notes in the format of pitch/duration sequences. 
                           E.g., "C4/4 E4/4 G4/4 | F4/4 F4/4"
        new_time_signature (str): The new time signature in the format "numerator/denominator". 
                                  E.g., "4/4" or "3/4"

        Returns:
        list: A list of measures where each measure is represented as a list of dictionaries with 'pitch' and 'duration'.
              The measures will be adjusted to align with the new time signature's beats per measure.
              
        Example:
        If the original time signature is "4/4" and the new time signature is "3/4", the function will 
        adjust the measures accordingly, adding rests or modifying notes if needed.
        """
        self.set_time_signature(new_time_signature)
        measures = self.parse_music(music_notes)

        # Adjust each measure for the new time signature
        adjusted_measures = []
        for measure in measures:
            while True:
                is_valid = self.validate_measure(measure, self.beats_per_measure, validation_type='solve')
                if is_valid:
                    adjusted_measures.append(measure)
                    break
                else:
                    print(f"Invalid measure duration, attempting to fix: {measure}")
        return adjusted_measures
    
                
    def notes_to_events(self, measures, tempo):
        """Convert to timeline events with proper timing"""
        quarter_duration = 60.0 / tempo
        for measure in measures:
            for note in measure:        
                try:
                    if note['pitch'] in ('R', 'r', 'rest', 'Rest', 'REST'):
                        event_type = 'rest'
                        freq = 0.0
                    else:
                        event_type = 'note'
                        freq = self.pitch_to_freq(note['pitch'])  # From previous implementation
                    
                    # Calculate actual duration in seconds
                    duration = max(float(1 / note['duration'] * 4 * quarter_duration), 0.01)
                    
                    yield {
                        'type': event_type,
                        'pitch': note['pitch'],
                        'duration': duration,
                        'frequency': freq,
                        'note_duration': note['duration'].numerator
                    }
                
                except Exception as e:
                    print(f"Skipping invalid note {note}: {str(e)}")
    
    
    """
    #
    #    play music / music_notes handler
    #    
    """
    
    
    def play_music(self, music: "MusicManager.SampleMusic"):        
        if music:
            name = music.name
            music_notes = music.notes
            tempo = music.tempo
            signature = music.signature
            
            if not hasattr(music, "instruments") or music.instruments == "":
                instrument = "organ"  # default instrument if it doesn't exist or is empty
            else:
                instrument = music.instruments[0]

            if not hasattr(music, "volume") or music.volume == "" or music.volume <= 0:
                volume = 0.5  # default volume if it doesn't exist, is empty, or is invalid
            else:
                volume = music.volume

            print(f"playing {name}")
            self.set_time_signature(signature)        
            self.play_music_notes(music_notes, tempo=tempo, instrument=instrument, volume=volume)
        
        
    # def play_music(self, music, tempo=128, instrument="organ", volume=0.5, chunk_size=1024):
        # try: 
        #     p = pyaudio.PyAudio()
        #     stream = p.open(format=pyaudio.paFloat32,
        #                     channels=1,
        #                     rate=44100,
        #                     output=True)
        #     measures = self.parse_music(music)
        #     for event in self.notes_to_events(measures, float(tempo)):
                
        #         # Preliminary ESC check
        #         if keyboard.is_pressed("esc"):
        #             print("ESC pressed! Stopping playback...")
        #             break
                
        #         # Print or debug info
        #         if self.is_print and event["type"] == "note":
        #             os.system('cls' if os.name == 'nt' else 'clear')
        #             print(f"Playing {instrument}: {event['pitch']} "
        #                 f"({event['frequency']:.2f} Hz, {event['duration']:.2f}s)")
                
        #         # Generate the entire wave (or silence) for the note/rest
        #         total_samples = int(44100 * event["duration"])
                
        #         if event['type'] == 'note':                    
        #             wave = self.generate_wave(
        #                 event['frequency'],
        #                 event['duration'],
        #                 instrument=instrument,
        #                 volume=volume
        #             )                                        
        #         elif event['type'] == 'rest':
        #             # Handle silence between notes
        #             wave = np.zeros(total_samples, dtype=np.float32)
                
        #         # Now stream in smaller chunks
        #         start_idx = 0
        #         while start_idx < total_samples:
        #             # Check if ESC was pressed mid-note
        #             if keyboard.is_pressed("esc"):
        #                 print("ESC pressed mid-note! Stopping playback.")
        #                 break

        #             end_idx = min(start_idx + chunk_size, total_samples)
        #             stream.write(wave[start_idx:end_idx].tobytes())
        #             start_idx = end_idx

        #         # If we broke mid-note due to ESC, stop everything
        #         if keyboard.is_pressed("esc"):
        #             break    
            
        #     # Cleanup
        #     stream.stop_stream()
        #     stream.close()
        #     p.terminate()
        #     return True
        # except Exception as e:
        #     print(f"Playback error: {e}")
        #     return False  
    
    def play_music_notes(self, music_notes: str, tempo: int = 128, instrument: str = "organ", volume: float = 0.5):
        """
        Play the given music with the specified tempo, instrument, and volume.

        Args:
            music_notes (str): List of music notes/measures to play.
            tempo (int): Tempo in beats per minute. Default is 128 BPM.
            instrument (str): Instrument to simulate during playback. Default is "organ".
            volume (float): Volume level (0.0 to 1.0). Default is 0.5.

        Returns:
            bool: True if playback was successful, False if interrupted or failed.
        """
        # Flag to control playback interruption
        self.stop_playback = False
        # Flag to track playback success
        playback_successful = True
        self.beats_per_measure = self._parse_time_signature()
        def playback_thread():
            nonlocal playback_successful  # Allows modifying the outer variable
            try:
                p = pyaudio.PyAudio()
                stream = p.open(format=pyaudio.paFloat32,
                                channels=1,
                                rate=44100,
                                output=True)
            
                measures = self.parse_music(music_notes)
                for event in self.notes_to_events(measures, tempo):
                    if keyboard.is_pressed("esc"):
                        print("ESC pressed! Stopping playback...")
                        self.stop_playback=True
                        
                    if self.stop_playback:  # Check if the user requested to stop playback
                        break
                    if event['type'] == 'note':
                        # Handle note playback
                        if self.is_print:
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"Playing {instrument}: {event['pitch']}/{event['note_duration']} "
                                f"({event['frequency']:.2f} Hz for {event['duration']:.2f}s)")
                        
                        wave = self.generate_wave(
                            event['frequency'],
                            event['duration'],
                            instrument=instrument,
                            volume=volume
                        )
                        stream.write(wave.tobytes())
                        
                    elif event['type'] == 'rest':
                        # Handle silence between notes
                        silence = np.zeros(int(44100 * event['duration']), dtype=np.float32)
                        stream.write(silence.tobytes())
            
                stream.stop_stream()
                stream.close()
                p.terminate()
            except Exception as e:
                print(f"Playback error: {e}")
                playback_successful = False
                
        # Run playback in a separate thread to avoid blocking the main thread
        thread = threading.Thread(target=playback_thread)
        thread.start()
        thread.join()  # Wait for the thread to finish
        return playback_successful
    
    def stop_music(self):
        # Simulate pressing the Esc key
        keyboard.send('esc')


    """
    #
    #    audio file handler
    #    
    """

    def save_audio(self, filename, wave, sample_rate=44100):
        """Save waveform to WAV file with proper normalization"""
        # Normalize to prevent clipping
        peak = np.max(np.abs(wave))
        if peak > 1.0:
            wave /= peak * 1.05
            
        # Convert to proper WAV format
        wave_int16 = np.int16(wave * 32767)
        
        sf.write(filename, wave_int16, sample_rate, subtype='PCM_16')


    """
    #
    #    signal processing for musical effects
    #       signal =  wave
    #       wave <-- frequency + duration + volume
    #    
    """
    
    # Echo effect
    def apply_echo(self, signal, sample_rate=44100, delay=0.15, decay=0.5):
        """Applies echo effect by delaying and reducing amplitude."""
        delay_samples = int(sample_rate * delay)
        echo_signal = np.zeros(len(signal) + delay_samples)
        echo_signal[:len(signal)] = signal
        echo_signal[delay_samples:] += decay * signal
        return echo_signal[:len(signal)]

    # Reverb effect (simplified)
    def apply_reverb(self, signal, sample_rate=44100, decay=0.4):
        """Applies a reverb effect by simulating reflections."""
        reverb_signal = np.copy(signal)
        for i in range(1, 5):
            reverb_signal += decay * np.roll(signal, i * 1000)
        return reverb_signal / 2

    # Distortion effect
    def apply_distortion(self, signal, gain=5.0):
        """Applies simple distortion by clipping the waveform."""
        return np.clip(signal * gain, -1.0, 1.0)
    
if __name__ == "__main__":
    muz = Music()
    
        
        
    
    