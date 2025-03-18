import json
from pathlib import Path

class SampleMusic():
    # -------------------------------------------------------------------------------------------------
    # SampleMusic Class
    #
    # to keep music data structure as object
    #
    # Version: 0.0.1
    # Date: 10 March 2025
    # -------------------------------------------------------------------------------------------------
    def __init__(self, name, notes, signature, tempo, instruments=["piano"], volume = 0.5, **kwargs):
        self.name = name
        self.notes = notes
        self.signature = signature
        self.tempo = tempo
        self.instruments = instruments
        self.volume = volume
        self.optional_data = kwargs  # Store additional optional attributes

    def get_music(self):
        """
        return dictionary of music data
        """
        music_data = {
            "name": self.name,
            "notes": self.notes,
            "signature": self.signature,
            "tempo": self.tempo,
            "instruments": self.instruments,
            "volume": self.volume
        }
        music_data.update(self.optional_data)  # Merge optional data
        return music_data


class MusicManager:
    # -------------------------------------------------------------------------------------------------
    # MusicManager Class
    #
    # Manager class for loading and managing music
    # Version: 0.0.1
    # Date: 10 March 2025
    # -------------------------------------------------------------------------------------------------
    def __init__(self, data_file):
        # Get the directory of the current script
        script_dir = Path(__file__).parent
        # Construct the full path to the JSON file
        self.data_file = script_dir / data_file
        self.music_objects = []
        
    def load_data(self):
        """Load JSON data and create music objects."""
        with open(self.data_file, "r") as file:
            music_data_list = json.load(file)
        for music_data in music_data_list:
            music_object = self.create_music(music_data)
            self.music_objects.append(music_object)

    def create_music(self, music_data):
        """Factory method to create a SampleMusic object."""
        return SampleMusic(**music_data)
    
    def add_music(self, music):
        """Add a new SampleMusic object to the manager."""
        if isinstance(music, SampleMusic):
            self.music_objects.append(music)
        else:
            raise TypeError("Only SampleMusic objects can be added.")
    
    def save_data(self):
        """Save all music objects back to the JSON file."""
        data_to_save = [music.get_music() for music in self.music_objects]
        with open(self.data_file, "w") as file:
            json.dump(data_to_save, file, indent=4)

    def get_all_music(self):
        """Retrieve all SampleMusic objects."""
        return self.music_objects

    def get_music_by_name(self, name):
        """Retrieve a SampleMusic object by its name."""
        for music in self.music_objects:
            if music.name == name:
                return music
        return None
    
# Example usage
if __name__ == "__main__":
    # Instantiate the manager and load data
    manager = MusicManager("music_data.json")
    manager.load_data()

    # Retrieve music by name
    doremi = manager.get_music_by_name("doremi")
    if doremi:
        print(doremi.get_music())

    # List all music objects
    for music in manager.music_objects:
        print(music.get_music())
    
    # List all music name
    for music in manager.get_all_music():
        print(music.name)