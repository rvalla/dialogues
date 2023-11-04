import json as js
import random as rd
from levenshtein import Levenshtein
from score import m21Score

class LevenScore(m21Score):
	"A machine to make music from text"

	#building an instance of a Counterpoint()..
	def __init__(self, title, composer, key, t_sig, parts, mode, notes_set, t_unit, t_measure, offs, v_offs):
		m21Score.__init__(self, title, composer, key, t_sig, parts)
		self.lv = Levenshtein()
		self.total_duration = 0
		self.mode = mode
		self.last_note = 0
		self.notes_set = notes_set
		self.t_unit = t_unit
		self.t_measure = t_measure
		self.midi_offset = offs
		self.voice_offset = v_offs

	#adding cycle from text...
	def add_cycle(self, text):
		if self.mode == "chords":
			self.add_chords(text)
		elif self.mode == "melody":
			self.add_melody(text)
		elif self.mode == "pulse":
			self.add_pulse(text)
		elif self.mode == "choral":
			self.add_choral(text)
		elif self.mode == "imitation":
			self.add_imitation(text)

	#functions to create with chords mode...
	def add_chords(self, text):
		words = text.split(" ")
		self.add_chord(words[0])
		for w in range(1, len(words)):
			d = self.lv.distance(words[w-1], words[w])
			if d > 0:
				duration = self.t_unit * d
				self.add_rest_chord(duration)
			self.add_chord(words[w])

	def add_chord(self, word):
		self.total_duration += self.t_unit
		for p in range(self.parts_count):
			pitch = self.notes_set[p%len(self.notes_set)] + self.midi_offset + self.voice_offset * p
			note = self.create_note(pitch, self.t_unit)
			if p == 0:
				note.addLyric(word)
			self.parts[p].append(note)
	
	def add_rest_chord(self, duration):
		self.total_duration += duration
		for p in range(self.parts_count):
			self.parts[p].append(self.create_note(-1, duration))
	
	#functions to create with melody mode...
	def add_melody(self, text):
		words = text.split(" ")
		for p in range(self.parts_count):
			self.last_note = rd.choice(self.notes_set)
			self.add_melody_note(p, words[0], 0, 1)
			for w in range(1, len(words)):
				d = self.lv.distance(words[w-1], words[w])
				self.add_melody_note(p, words[w], d, self.melody_direction(words[w-1], words[w]))
		self.fill_last_measure()
	
	def add_melody_note(self, part, word, d, direction):
		duration = len(word) * self.t_unit
		self.last_note = self.last_note + d * direction
		pitch = self.last_note + self.midi_offset + self.voice_offset * part
		note = self.create_note(pitch, duration)
		if part == 0:
			self.total_duration += duration
			note.addLyric(word)
		self.parts[part].append(note)

	def melody_direction(self, word_a, word_b):
		direction = 1
		if len(word_b) < len(word_a):
			direction = -1
		elif len(word_b) == len(word_a):
			direction = rd.choice([-1,1])
		return direction
	
	#functions to create with pulse mode...
	def add_pulse(self, text):
		words = text.split(" ")
		for p in range(self.parts_count):
			self.last_note = rd.choice(self.notes_set)
			self.add_pulse_note(p, words[0], 0, self.melody_direction(words[0], words[1]))
			for w in range(1, len(words)):
				d = self.lv.distance(words[w-1], words[w])
				self.add_pulse_note(p, words[w], d, self.pulse_direction(words[w-1], words[w]))
		self.fill_last_measure()
	
	def add_pulse_note(self, part, word, d, direction):
		self.last_note = self.last_note + d * direction
		pitch = self.last_note + self.midi_offset + self.voice_offset * part
		note = self.create_note(pitch, self.t_unit)
		if part == 0:
			self.total_duration += self.t_unit
			note.addLyric(word)
		self.parts[part].append(note)

	def pulse_direction(self, word_a, word_b):
		direction = 1
		if len(word_b) < len(word_a):
			direction = -1
		elif len(word_b) == len(word_a):
			direction = rd.choice([-1,1])
		return direction
	
	#functions to create with choral mode...
	def add_choral(self, text):
		words = text.split(" ")
		for w in range(len(words)):
			c_words = []
			c_distances = [0]
			for p in range(self.parts_count):
				c_words.append(words[(w + p)%len(words)])
			for c_w in range(1, len(c_words)):
				c_distances.append(self.lv.distance(c_words[0], c_words[c_w]))
			self.add_choral_chord(c_words, c_distances, self.get_upper_voice(w))

	def add_choral_chord(self, words, distances, n):
		self.total_duration += self.t_unit
		for p in range(self.parts_count):
			pitch = n - distances[p] + self.midi_offset + self.voice_offset * p
			note = self.create_note(pitch, self.t_unit)
			note.addLyric(words[p])
			self.parts[p].append(note)
	
	def get_upper_voice(self, position):
		return self.notes_set[position%len(self.notes_set)]

	#functions to create with imitation mode...
	def add_imitation(self, text):
		words = text.split(" ")
		offsets = self.get_offsets(self.parts_count, len(words))
		for p in range(self.parts_count):
			self.last_note = rd.choice(self.notes_set)
			self.add_melody_note(p, words[offsets[p]%len(words)], 0, 1)
			for w in range(1, len(words)):
				d = self.lv.distance(words[(w + offsets[p] - 1)%len(words)], words[(w + offsets[p])%len(words)])
				self.add_melody_note(p, words[(w + offsets[p])%len(words)], d, self.melody_direction(words[(w + offsets[p] - 1)%len(words)], words[(w + offsets[p])%len(words)]))
		self.fill_last_measure()
	
	def get_offsets(self, parts, size):
		offsets = [0]
		for p in range(1,parts):
			offsets.append(rd.choice(range(size)))
		return offsets

	#setting mode...
	def set_mode(self, mode):
		self.mode = mode
	
	#setting t_unit...
	def set_mode(self, unit):
		self.t_unit = unit

	#changing notes...
	def new_notes_set(self, notes):
		self.notes_set = notes
	
	def notes_set_to_str(self):
		s = ""
		for n in self.notes_set:
			s += str(n)
			s += " "
		return s

	#filling last measures...
	def fill_last_measure(self):
		f = 1
		if self.t_unit < 1:
			f = 1 / self.t_unit
		m = self.t_measure * f
		r = (self.total_duration * f)%m
		if r > 0:
			self.add_rest_chord((m-r)/f)

	#printing information...
	def __str__(self):
		return "-- Hi, I am a tool to create music from text..." + "\n" \
				+ "-- I have " + str(self.parts_count) + " parts" + "\n" \
				+ "-- And " + self.get_notes_count() + " notes" + "\n" \
				+ "-- I think there is a chance you like me..."

	
