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
		self.notes_set = notes_set
		self.t_unit = t_unit
		self.t_measure = t_measure
		self.t_set = int(self.t_measure / self.t_unit)
		self.midi_offset = offs
		self.voice_offset = v_offs

	#adding cycle from text...
	def add_cycle(self, text):
		if self.mode == "chords":
			self.add_chords(text)

	#functions to create rwith chords mode...
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
		for p in range(len(self.parts)):
			pitch = self.notes_set[p%len(self.notes_set)] + self.midi_offset + self.voice_offset * p
			note = self.create_note(pitch, self.t_unit)
			if p == 0:
				note.addLyric(word)
			self.parts[p].append(note)
	
	def add_rest_chord(self, duration):
		self.total_duration += duration
		for p in range(len(self.parts)):
			self.parts[p].append(self.create_note(-1, duration))

	#setting mode...
	def set_mode(self, mode):
		self.mode = mode

	#changing notes...
	def new_notes_set(self, notes):
		self.notes_set = notes

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
				+ "-- I have " + str(len(self.parts)) + " parts" + "\n" \
				+ "-- And " + self.get_notes_count() + " notes" + "\n" \
				+ "-- I think there is a chance you like me..."

	
