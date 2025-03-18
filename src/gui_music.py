import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
# from tkinter import filedialog
import Music

import tkinter as tk

class MusicGUI:
    def __init__(self, initial_title="Default Title", initial_size="1200x800"):
        # Save initial values
        self.initial_title = initial_title
        self.initial_size = initial_size
        
        # Initialize tkinter root
        self.root = tk.Tk()
        self._setup_root()
        self._setup_constants()
        self._setup_gui()
        
        # initalize Music Object
        self.muz = Music.Music()

    def _setup_root(self):
        # Apply initial values to the tkinter root
        self.root.title(self.initial_title)
        self.root.geometry(self.initial_size)

    def _setup_constants(self):
        # # CONSTANTS
        self.INSTRUMENTS = ["Piano", "Guitar", "Organ", "Drum", "Bass", "Bell", "Angklung", "Harmonica", "Flute"]
        self.EFFECTS = ["None", "Reverb", "Echo", "Distortion"]
        self.SAMPLE =["None", "Doremi", "Mozart", "kakatua"]
        self.signature_numerator_list=[1,2,3,4,5,6,7,8,9,16,32]
        self.signature_denomerator_list=[1,2,3,4,5,6,7,8,9,16,32,64]

    def _on_sample_selected(self, event):
        # Clear the text widget
        self.note_text.delete("1.0", tk.END)

        # Insert text based on sample selection
        selected_sample = self.sample_var.get()
        if selected_sample == "Doremi":
            music = self.doremi()
        elif selected_sample == "Mozart":
            music = self.mozart()
        elif selected_sample == "kakatua":
            music = self.kakatua()
        elif selected_sample == "None":
            music = {'name': "None",
            'notes':"",
            'signature': "4/4",
            'tempo': 60,
            }
        signature = music["signature"]
        music_notes = music["notes"]
        tempo = music["tempo"]
        self.note_text.insert("1.0", music_notes)
        self.tempo_var = tk.IntVar(value=tempo)
        numerator, denominator = map(int, signature.split('/'))
        self.signature_numerator_var = tk.IntVar(value=numerator)
        self.signature_denomerator_var = tk.IntVar(value=denominator)
        self.signature_nominator_menu.set(numerator)
        self.signature_denominator_menu.set(denominator)
        self.tempo_slider.set(tempo)
        
        
    
    def doremi(self):
        music = {'name': "doremi",
        'notes':"""rest/4 C4/4 D4/4 E4/4 | 
F4/4 G4/4 A4/4 B4/4 | 
C5/4 C5/4 B4/4 A4/4 | 
G4/4 F4/4 E4/4 D4/4 | 
C4/4 rest/2 rest/4
""",
        'signature': "4/4",
        'tempo': 60,
        }
        return music
    
    def mozart(self):
        music = {'name': "mozart",
        'notes': """rest/4 B4/16 A4/16 G#4/16 A4/16|
C5/8 rest/8 D5/16 C5/16 B4/16 C5/16|
E5/8 rest/8 F5/16 E5/16 D#5/16 E5/16|
B5/16 A5/16 G#5/16 A5/16 B5/16 A5/16 G#5/16 A5/16|
C6/4 A5/8 C6/8|
B5/8 A5/8 G5/8 A5/8|
B5/8 A5/8 G5/8 A5/8|
B5/8 A5/8 G5/8 F#5/8|
E5/2
        """,
        'signature': "2/4",
        'tempo': 128,
        }
        return music         
    
    def kakatua(self):
        music = {'name': "kakatua",
        'notes':"""G4/2 E4/4 |
C5/2 E4/4 |
D4/2. | 
D4/4 rest/4 E4/4|
F4/2 A4/4|
G4/2 F4/4 |
E4/2. |
E4/4 rest/4 G4/4 |
G4/2 E4/4 |
C5/2 E4/4 |
D4/4 rest/2 |
D4/4 rest/4 B4/8 A4/8 |
G4/2 F4/4|
E4/2 D4/4|
C4/4 rest/2|
C4/4 rest/4 G4/4|
E4/2 G4/4|
E4/2 G4/4|
A4/4 A4/4 A4/4|
A4/2 F4/4|
D4/2 F4/4|
D4/2 F4/4|
G4/4 G4/4 G4/4|
G4/2 G4/4|
E4/2 G4/4|
E4/2 G4/4|
A4/4 A4/4 A4/4|
D5/2 C5/4|
B4/2 G4/4|
A4/2 B4/4|
C5/4 rest/2|
C5/2 rest/4
    """,
        'signature': "3/4",
        'tempo': 128,
        }
        return music
            

    # Bind the slider to ensure integer values
    def update_tempo_var(self,value):
        self.tempo_var.set(int(float(value)))  # Convert the slider's value to integer
            
    def _setup_gui(self):
        # Instrument Selection
        ttk.Label(self.root, text="Select Instrument: ").grid(row=0, column=0, sticky="e")
        self.instrument_var = tk.StringVar(value="Piano")
        instrument_container = ttk.Frame(self.root)  # Create a frame to group slider and text box
        instrument_container.grid(row=0, column=1, sticky="w")
        instrument_menu = ttk.Combobox(instrument_container, textvariable=self.instrument_var, values=self.INSTRUMENTS)
        instrument_menu.grid(row=0, column=0, sticky="w")
        ttk.Label(instrument_container, text="            ").grid(row=0, column=2, sticky="e", pady=15)
        # Play buttons
        self.play_button = ttk.Button(instrument_container, text="🎵 Play", command=self.play_music)
        self.play_button.grid(row=0, column=3, sticky="e", pady=15)
        ttk.Label(instrument_container, text=" ").grid(row=0, column=4, sticky="e", pady=3)
        ttk.Label(instrument_container, text="press ESC to stop playing").grid(row=0, column=5, sticky="w")


        # Effect Selection
        ttk.Label(self.root, text="Select Effect: ").grid(row=1, column=0, sticky="e")
        self.effect_var = tk.StringVar(value="None")
        self.effect_menu = ttk.Combobox(self.root, textvariable=self.effect_var, values=self.EFFECTS)
        self.effect_menu.grid(row=1, column=1, sticky="w")

        # Sample Music Selection
        ttk.Label(self.root, text="Select Sample Music:").grid(row=2, column=0, sticky="e")
        sample_container = ttk.Frame(self.root)  # Create a frame to group slider and text box
        sample_container.grid(row=2, column=1, sticky="w") 
        self.sample_var = tk.StringVar(value="")
        self.sample_menu = ttk.Combobox(sample_container, textvariable=self.sample_var, values=self.SAMPLE)
        self.sample_menu.grid(row=0, column=0, sticky="w")        
        self.sample_menu.bind("<<ComboboxSelected>>", self._on_sample_selected) # callback for selection
        ttk.Label(sample_container, text="            ").grid(row=0, column=1, sticky="e", pady=15)
        self.canonize_button = ttk.Button(sample_container, text="Canonize", command=self.canonize_music)
        self.canonize_button.grid(row=0, column=2, sticky="e", pady=15)

        # Tempo Selection (slider and text synchronization)
        ttk.Label(self.root, text="Tempo (Speed): ").grid(row=3, column=0, sticky="e")
        tempo_container = ttk.Frame(self.root)  # Create a frame to group slider and text box
        tempo_container.grid(row=3, column=1, sticky="w")  # Place the frame in the same row/column as needed
        self.tempo_var = tk.IntVar(value=128)
        self.tempo_slider = ttk.Scale(tempo_container, from_=8, to=512, orient=tk.HORIZONTAL, variable=self.tempo_var)
        self.tempo_slider.grid(row=0, column=0, sticky="w", pady=15)  # Add slider to the frame
        self.tempo_entry = ttk.Entry(tempo_container, textvariable=self.tempo_var, width=12)
        self.tempo_entry.grid(row=0, column=1, sticky="w", pady=15)  # Add entry to the frame, below slider
        self.tempo_slider.configure(command=self.update_tempo_var)  # Bind the callback to slider movement
        # Time Signature
        ttk.Label(tempo_container, text="            ").grid(row=0, column=2, sticky="e", pady=15)
        ttk.Label(tempo_container, text="Time Signature: ").grid(row=0, column=3, sticky="e")
        self.signature_numerator_var = tk.IntVar(value=4)
        self.signature_denomerator_var = tk.IntVar(value=4)
        self.signature_nominator_menu=ttk.Combobox(tempo_container, textvariable=self.signature_numerator_var, values=self.signature_numerator_list, width=3)
        self.signature_nominator_menu.grid(row=0, column=4, sticky="w")
        self.signature_nominator_menu.bind("<<ComboboxSelected>>", self._on_sample_selected)
        ttk.Label(tempo_container, text="/").grid(row=0, column=5, sticky="e")
        self.signature_denominator_menu=ttk.Combobox(tempo_container, textvariable=self.signature_denomerator_var, values=self.signature_denomerator_list, width=3)
        self.signature_denominator_menu.grid(row=0, column=6, sticky="w")
        self.signature_denominator_menu.bind("<<ComboboxSelected>>", self._on_sample_selected)

        # Text Box for Notes Input (left: label and button, right: text box)
        ttk.Label(self.root, text="Enter Music Notes: ").grid(row=4, column=0, sticky="ne")
        # self.import_button = ttk.Button(self.root, text="Import File", command=self.import_music_file)
        # self.import_button.grid(row=5, column=0, sticky="n", pady=5)
        self.note_text = tk.Text(self.root, height=10, width=50)
        self.note_text.insert("1.0", self.default_sample_music_note()) # Set default music notes
        self.note_text.grid(row=4, column=1, rowspan=2)
        
        # Save Button
        save_music_container = ttk.Frame(self.root)  # Create a frame to group slider and text box
        save_music_container.grid(row=6, column=1, sticky="w")
        ttk.Label(save_music_container, text="File Name: ").grid(row=0, column=0, sticky="w")
        self.file_name_var = tk.StringVar(value="Composition.wav")
        self.file_name_entry = ttk.Entry(save_music_container, textvariable=self.file_name_var)
        self.file_name_entry.grid(row=0, column=1, sticky="w")
        self.save_button = ttk.Button(save_music_container, text="Save Music as File", command=self.export_music_file)
        self.save_button.grid(row=0, column=2, sticky="e", pady=5)
        
    def default_sample_music_note(self):
        self.muz = Music.Music()
        name = "mary has a little lamb"
        music = self.muz.manager.get_music_by_name(name)
        if music:            
            # instrument = music.instruments[0]
            # tempo = music.tempo
            signature = music.signature
            self.muz.set_time_signature(signature)  
            return music.notes
        
    def import_music_file(self):
        pass
    
    def export_music_file(self):
        instrument = self.instrument_var.get().lower()
        filename = self.file_name_var.get()
        tempo = self.tempo_var.get()
        music_notes = self.note_text.get("1.0", tk.END).strip()
        waves = self.muz.music_note_to_waves(music_notes, tempo=tempo, instrument=instrument)
        self.muz.save_audio(filename, waves)
        # Show a messagebox to inform the user
        messagebox.showinfo("Success", f"The music file '{filename}' has been saved successfully!")

    def canonize_music(self):
        numerator = str(self.signature_numerator_var.get())
        denomerator = str(self.signature_denomerator_var.get())
        signature =  numerator + "/" + denomerator 
        tempo = self.tempo_var.get()
        music_notes = self.note_text.get("1.0", tk.END).strip()
        canonize_notes = self.muz.canonize_music(music_notes, tempo, signature)
        # Clear the existing text
        self.note_text.delete("1.0", tk.END)
        # Insert the new text
        self.note_text.insert("1.0", canonize_notes)
        
    def play_music(self):
        instrument = self.instrument_var.get().lower()
        effect = self.effect_var.get()
        tempo = self.tempo_var.get()
        music_notes = self.note_text.get("1.0", tk.END).strip()
        if music_notes!="" and tempo>0:
            waves = self.muz.music_notes_to_waves(music_notes, tempo=tempo, instrument=instrument, volume=0.5) # creating signal
            if effect == "Reverb":
                print("wave with reverb")
                new_waves = self.muz.apply_reverb(waves)
            elif effect == "Echo":
                print("wave with echo")
                new_waves = self.muz.apply_echo(waves)
            elif effect == "Distortion":
                print("wave with distortion")
                new_waves = self.muz.apply_distortion(waves)
            else:
                # effect == "None":
                new_waves = waves
            self.muz.play_wave(new_waves)
            # self.muz.play_music_notes(music_notes=music_notes, tempo=tempo, instrument=instrument, volume=0.5)
        
    def run(self):
        # Start the tkinter main event loop
        self.root.mainloop()

# Example of using the MyTkApp class
if __name__ == "__main__":
    # Set initial values
    app = MusicGUI(initial_title="Interactive Music Synthesizer", initial_size="920x510")
    # Run the app
    app.run()











# # # Function to play music
# # def play_music():
# #     pass
#     # instrument = instrument_var.get().lower()
#     # effect = effect_var.get().lower()
#     # tempo = tempo_var.get()
#     # music_notes = note_text.get("1.0", tk.END).strip()

#     # # Convert string to sound and play
#     # wave_data = process_music(music_notes, instrument, effect, tempo)
#     # play_wave(wave_data)

# 



# # Run GUI
# root.mainloop()

# # # File Import Button

# # def import_music_file():
# #     file_path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid"), ("Audio Files", "*.mp3;*.wav")])
# #     if file_path.endswith(".mid"):
# #         music_string = convert_midi_to_string(file_path)
# #     else:
# #         music_string = convert_audio_to_string(file_path)

# #     note_text.delete("1.0", tk.END)
# #     note_text.insert(tk.END, music_string)


# # def process_music(music_string, instrument="piano", effect="none", tempo=120):
# #     quarter_note_duration = 60 / tempo

# #     wave_data = np.array([])
    
# #     for measure in music_string.split(", "):
# #         for note in measure.split(" "):
# #             note_parts = note.split("/")
# #             pitch = note_parts[0]
# #             duration = 4 / int(note_parts[1])

# #             frequency = NOTE_FREQUENCIES.get(pitch, 0)
# #             wave = generate_wave(frequency, quarter_note_duration * duration, instrument=instrument)

# #             if effect == "reverb":
# #                 wave = apply_reverb(wave)
# #             elif effect == "echo":
# #                 wave = apply_echo(wave)
# #             elif effect == "distortion":
# #                 wave = apply_distortion(wave)

# #             wave_data = np.concatenate((wave_data, wave))

# #     return wave_data

