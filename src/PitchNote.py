import re
class PitchNote:
    # -------------------------------------------------------------------------------------------------
    # PitchNote Class
    # Handles both standard (canonical) and non-standard musical picth notes such as "Fx4", "Cx5",
    # "Dx4", "Bbb3", "A#4", "Bx3" and their frequencies.
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
    # Version: 0.1.0
    # Date: 09 March 2025
    # -------------------------------------------------------------------------------------------------
    def __init__(self, A4_midi=69, A4_freq=440.0):
        """
        :param A4_midi: MIDI note number for A4 (default 69).
        :param A4_freq: Frequency of A4 in Hz (default 440.0).
        """
        self.version = "0.1.0"
        self.A4_midi = A4_midi
        self.A4_freq = A4_freq

        # Mapping from natural note letter to the “pitch class” (0..11)
        # measured as semitones above C.
        self.BASE_PITCH = {
            'C': 0,
            'D': 2,
            'E': 4,
            'F': 5,
            'G': 7,
            'A': 9,
            'B': 11
        }

        # For converting pitch class (0..11) back to a canonical name.
        # (All sharps, no flats.)
        # index 0 -> C, 1 -> C#, 2 -> D, etc.
        self.CANONICAL_NAMES_SHARP = [
            'C', 'C#', 'D', 'D#', 'E', 
            'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
        ]


    def parse_note(self, pitch_name: str) -> int:
        """
        Parses a note string like 'Cx4' (C double sharp 4), 'Db5', 'Bbb3', etc.
        Returns the corresponding MIDI note number.
        Raises ValueError if the format or note is invalid.
        """

        # Regex to capture: 
        #   Group 1: letter name (A–G, case-insensitive)
        #   Group 2: accidentals (any combination of #, b, x)
        #   Group 3: octave (digits)
        pattern = r'^([A-Ga-g])([#bx]+)?(\d+)$'
        match = re.match(pattern, pitch_name.strip())
        if not match:
            raise ValueError(f"Invalid note format: {pitch_name}")
        
        letter, accidentals, octave_str = match.groups()
        
        # Convert letter to uppercase
        letter = letter.upper()
        
        # Get base pitch class from the letter.
        if letter not in self.BASE_PITCH:
            raise ValueError(f"Unrecognized note letter: {letter}")
        base_pitch = self.BASE_PITCH[letter]
        
        # Convert the accidentals into a total semitone shift.
        semitone_shift = 0
        if accidentals:
            for symbol in accidentals:
                if symbol == '#':
                    semitone_shift += 1
                elif symbol == 'b':
                    semitone_shift -= 1
                elif symbol == 'x':
                    # double sharp = +2 semitones
                    semitone_shift += 2
                else:
                    raise ValueError(f"Unrecognized accidental: {symbol}")

        # Combine base pitch + shift, modulo 12 for safety
        pitch_class = (base_pitch + semitone_shift) % 12
        
        # Convert octave to integer
        octave = int(octave_str)

        # MIDI formula:
        #   Middle C (C4) is MIDI 60
        #   So for a note in octave `octave` with pitch class `pitch_class`,
        #   the MIDI is:
        #       (octave + 1) * 12 + pitch_class
        midi_num = (octave + 1) * 12 + pitch_class
        
        return midi_num


    def midi_to_freq(self, midi_num: int) -> float:
        """
        Convert a MIDI note number to its frequency in Hz
        using the standard 12-tone equal temperament (A4=440Hz).
        """
        return self.A4_freq * (2.0 ** ((midi_num - self.A4_midi) / 12.0))


    def midi_to_name(self, midi_num: int) -> str:
        """
        Convert a MIDI note number back to a canonical name (e.g. "C#4"),
        using sharps for accidentals.
        """

        # pitch_class in [0..11]
        pitch_class = midi_num % 12
        octave = (midi_num // 12) - 1  # ensures MIDI 60 -> "C4"

        pitch_name = self.CANONICAL_NAMES_SHARP[pitch_class]
        
        return f"{pitch_name}{octave}"

    def normalize_pitch_name(self, base_note: str, octave: int) -> str:
        """
        Takes something like base_note='Cx' and octave=4
        and returns a standard spelling like 'D4' if we
        only store D4 in our dictionary.
        """
        # 1) Convert the possibly exotic note (e.g. "Cx4") to a MIDI number
        full_input = f"{base_note}{octave}"
        midi_num = self.parse_note(full_input)

        # 2) Convert that MIDI back to canonical name (e.g. "D4").
        return self.midi_to_name(midi_num)


    def note_freq_definition(self):
        """*
        return dictionary of canonical notes {MIDI: Frequency}
        MIDI is canonical note from A0 to C8. Frequency in Hz.
        """
        NOTE_FREQUENCIES = {}
        A4_MIDI = 69
        pitch_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        A4_FREQ = 440.0
        
        # Generate all MIDI notes from 21 (A0) to 127 (G9)
        for midi_num in range(21, 128):
            note_index = midi_num % 12
            octave = (midi_num // 12) - 1
            pitch_name = f"{pitch_names[note_index]}{octave}"
            freq = A4_FREQ * (2 ** ((midi_num - A4_MIDI) / 12.0))
            NOTE_FREQUENCIES[pitch_name] = freq

        NOTE_FREQUENCIES["rest"] = 0.0
        return NOTE_FREQUENCIES

if __name__ == "__main__":
    # Example usage:
    handler = PitchNote()

    test_notes = ["Fx4", "Cx5", "Dx4", "Cx4", "Bbb3", "F#4", "Eb5", "Fx3", "Bx3", "C4", "E#4"]
    for tn in test_notes:
        try:
            midi = handler.parse_note(tn)
            freq = handler.midi_to_freq(midi)
            canonical = handler.midi_to_name(midi)
            normalized = handler.normalize_pitch_name(tn[:-1], tn[-1])  # split base_note, octave
            print(f"Original: {tn:<5} -> MIDI: {midi:<3}  Freq: {freq:8.2f} Hz   "
                  f"Canonical: {canonical:<4}  Normalized: {normalized}")
        except ValueError as e:
            print(e)