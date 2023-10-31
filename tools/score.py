from music21 import *

class m21Score():
	"An object to build a score of some unknown music"

	def __init__(self, title, composer, key_signature, time_signature, parts_count):
		self.score = stream.Score() #The score object...
		self.score.insert(0, metadata.Metadata())
		self.score.metadata.title = title #Some metadata...
		self.score.metadata.composer = composer
		self.parts_count = parts_count
		self.parts = []
		for p in range(parts_count):
			self.parts.append(stream.Part()) #Here we create the parts...
			self.parts[p].append(key.KeySignature(key_signature))
			self.parts[p].append(meter.TimeSignature(time_signature))
			self.score.append(self.parts[p])

	#function to create a note...
	def create_note(self, midi_v, duration_v):
		try:
			if midi_v >= 0:
				n = note.Note(midi_v)
			else:
				n = note.Rest()
			n.duration = duration.Duration(duration_v)
			return n
		except:
			print("-- Explotion. Something went wrong...")

	#function to add one note
	def create_note_in_part(self, midi_v, duration_v, part):
		try:
			n = self.create_note(midi_v, duration_v)
			self.parts[part].append(n)
		except:
			print("-- Explotion. Something went wrong...")

	#function to add a list of notes
	def create_notes_in_part(self, midi_vs, duration_vs, part):
		for m, d in zip(midi_vs, duration_vs):
			self.create_note_in_part(m, d, part)

	#function to add a list of pitches with the same duration
	def create_pitches_in_part(self, midi_vs, duration_v, part):
		for m in midi_vs:
			self.create_note_in_part(m, duration_v, part)

	#adding notes to part...
	def add_notes_to_part(self, notes, part):
		for n in notes:
			self.add_note_to_part(n, part)

	#adding one note to part...
	def add_note_to_part(self, note, part):
		try:
			self.parts[part].append(note)
		except:
			print("-- Explotion. Something went wrong...")

	#show me my score!
	def show_score(self):
		self.score.show()

	#saving the score!
	def save_score(self, output_p, output_n, f):
		self.score.write(f, output_p + output_n + "." + f)
		print("-- Score saved as " + output_n)

	#number of notes in score...
	def get_notes_count(self):
		notes = 0
		for p in self.parts:
			notes += len(p) - 2
		return str(notes)

	#printing m21Score information...
	def __str__(self):
		return "-- Hi, I am a score of unknown music" + "\n" \
				+ "-- I have " + str(len(self.parts)) + " parts" + "\n" \
				+ "-- And " + self.get_notes_count() + " notes" + "\n" \
				+ "-- I think I sound perfectly."