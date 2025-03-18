# unit-test-music.py
import unittest
import Music 

class TestMusic(unittest.TestCase):
    def setUp(self):
        self.muz = Music.Music()
    
    
    
    """
    #
    #    testing notes and its frequency
    #
    """
    
    def test_note_freq_definition(self):
        # standard dictionary of note and frequency has 108 notes
        self.assertEqual(len(self.muz.note_handle.note_freq_definition()),108)
    
    def test_pitch_to_frequencies(self): 
        # test the frequency of some notes manually              
        self.assertEqual(self.muz.pitch_to_freq("A0"),27.5)
        self.assertEqual(self.muz.pitch_to_freq("A1"),55.0)
        self.assertEqual(self.muz.pitch_to_freq("A2"),110.0)
        self.assertEqual(self.muz.pitch_to_freq("A3"),220.0)
        self.assertEqual(self.muz.pitch_to_freq("A4"),440.0)
        self.assertEqual(self.muz.pitch_to_freq("A5"),880.0)
        self.assertEqual(self.muz.pitch_to_freq("A6"),1760.0)
        self.assertEqual(self.muz.pitch_to_freq("A7"),3520.0)
        self.assertEqual(self.muz.pitch_to_freq("A8"),7040.0)
        self.assertEqual(self.muz.pitch_to_freq("C4"),261.6255653005986)
        self.assertEqual(self.muz.pitch_to_freq("G#5"),830.6093951598903)
        self.assertEqual(self.muz.pitch_to_freq("Bb3"),233.08188075904496)
        self.assertEqual(self.muz.pitch_to_freq("rest"),0.0)
        self.assertEqual(self.muz.pitch_to_freq("B4"),493.8833012561241)
        self.assertEqual(self.muz.pitch_to_freq("D5"),587.3295358348151)
        self.assertEqual(self.muz.pitch_to_freq("E3"),164.81377845643496)
        self.assertEqual(self.muz.pitch_to_freq("C8"),4186.009044809578)

    def test_all_notes_frequency_exhaustively(self):
        # test the frequency of all possible 108 notes exhaustively
        note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        A4_FREQ = 440.0
        A4_MIDI = 69
        for midi_num in range(21, 128):
            note_index = midi_num % 12
            octave = (midi_num // 12) - 1
            note_name = f"{note_names[note_index]}{octave}"
            self.assertEqual(self.muz.pitch_to_freq(note_name),A4_FREQ * (2 ** ((midi_num - A4_MIDI) / 12)))
    
    def test_non_standard_notes(self): 
        # test to normalize the non-standard notes
        examples = ["Fx4", "Cx5", "Dx4", "Bbb3", "A#4", "Bx3", "Cx4", "Bb3", "F#4", "Eb5", "Fx3", "B3", "Cb4", "G#4"]
        for note in examples:
            midi = self.muz.note_handle.parse_note(note)
            canonical = self.muz.note_handle.midi_to_name(midi)
            freq = self.muz.note_handle.midi_to_freq(midi)
            print(f"{note} -> MIDI {midi}, Canonical: {canonical:<4} freq ~ {freq:.2f} Hz")
            self.assertEqual(self.muz.pitch_to_freq(note),self.muz.pitch_to_freq(canonical))
    
    """
    #
    #    testing music
    #
    """
    
    def test_music_notes_are_string(self):
        # make sure all music notes are strings
        muz = Music.Music()
        music = muz.manager.get_music_by_name("doremi")
        music_notes = music.notes
        self.assertIsInstance(music_notes,str)
        
        music = muz.manager.get_music_by_name("mozart")
        music_notes = music.notes
        self.assertIsInstance(music_notes,str)
        
        music = muz.manager.get_music_by_name("kakatua")
        music_notes = music.notes
        self.assertIsInstance(music_notes,str)
    
    def test_play_doremi(self):
        muz = Music.Music(isPrint=False)
        music_object = muz.manager.get_music_by_name("doremi")
        music = music_object.get_music() # get dictionary of music data
        signature = music["signature"]
        music_notes = music["notes"]
        tempo = music["tempo"]        
        muz.set_time_signature(signature)
        self.assertTrue(self.muz.play_music_notes(music_notes, tempo=tempo))
        
if __name__ == "__main__":
    unittest.main()