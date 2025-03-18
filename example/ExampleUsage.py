from Music import Music 

# Example usage

# example 1
muz = Music(isPrint = True)
music = muz.manager.get_music_by_name("doremi") # get sample music object
if music:        
    muz.play_music(music) # play music object
    name = music.name
    music_notes = music.notes
    tempo = music.tempo
    signature = music.signature
    muz.set_time_signature(signature)
    print(f"music_notes of {name}: {music_notes}") 
    waves = muz.music_notes_to_waves(music_notes, tempo=tempo, instrument="violin",volume=0.5) 
    print("saving to file")
    muz.save_audio("doremi.wav", waves)
    print("original wave")
    muz.play_wave(waves)
    print("wave with echo")
    new_waves = muz.apply_echo(waves)
    muz.play_wave(new_waves)
    print("wave with distortion")
    new_waves = muz.apply_distortion(waves)
    muz.play_wave(new_waves)
    print("wave with reverb")
    new_waves = muz.apply_reverb(waves)
    muz.play_wave(new_waves)
    
# example 2
muz = Music(isPrint = True)
music = muz.manager.get_music_by_name("mozart")
if music:
    name = music.name    
    music_notes = music.notes
    instrument = music.instruments[0]
    print(f"Playing {name} using {instrument}")
    tempo = music.tempo
    signature = music.signature
    muz.set_time_signature(signature)
    waves = muz.music_notes_to_waves(music_notes, tempo=tempo, instrument=instrument)
    muz.play_wave(waves)
    muz.save_audio("mozart.wav", waves)
    
# example 3
muz = Music(isPrint = False)
music = muz.manager.get_music_by_name("kakatua")
if music:
    name = music.name           
    music_notes = music.notes
    instruments = music.instruments
    print("available instruments:",instruments)
    tempo = music.tempo
    signature = music.signature
    muz.set_time_signature(signature)
    for instrument in instruments[:-5]:
        # playing a few of the intruments
        print(f"Playing {name} using {instrument}")
        muz.play_music_notes(music_notes, tempo=tempo, instrument=instrument)
    waves = muz.music_notes_to_waves(music_notes,instrument="harmonica")
    muz.save_audio("kakatua.wav", waves)
        
    