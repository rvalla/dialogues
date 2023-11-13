import warnings
warnings.filterwarnings('ignore')

from levenscore import LevenScore

#example code create music with LevenScore()...
print("Let's create a Levenshtein based musical piece...", end="\n")
print("After setting configuration you can send text. Remember these commands:", end="\n")
print("- _n to set a new notes set.", end="\n")
print("- _m to set a new mode.", end="\n")
print("- _s to save the score.", end="\n")
print("- _q to quit.", end="\n\n")

title = None
composer = None
key = None
t_sig = None
parts = None
mode = None #chords, melody, pulse, choral, crayfish
notes_set = None
t_unit = None
t_measure = None
offs = None
v_offs = None
filename = None

l = None #the score...

def set_configuration():
	#some configuration data...
	print("Please tell me a title for your piece:", end="\n")
	global title
	title = input()
	print("Now I need a your name:", end="\n")
	global composer
	composer = input()
	print("We need to decide a key... Tell me a number (0-11):", end="\n")
	global key
	key = int(input())
	print("Tell me your prefered time signature (3/4, 4/4, etc):", end="\n")
	global t_sig
	t_sig = input()
	print("Tell me the number of parts in this composition:", end="\n")
	global parts
	parts = int(input())
	print("Select working mode (chords, melody, pulse, choral, imitation, crayfish)", end="\n")
	global mode
	mode = input()
	print("I need a notes set now. Send me numbers separated with spaces.", end="\n")
	global notes_set
	notes_set = [int(a) for a in input().split(" ")]
	print("What is the minimun duration (using quarter note fractions):", end="\n")
	global t_unit
	t_unit = float(input())
	print("Tell me please the total quarter note duration of a measure:", end="\n")
	global t_measure
	t_measure = float(input())
	print("How many notes above 0 is the upper voice C?", end="\n")
	global offs
	offs = int(input())
	print("Please define each voice offset:", end="\n")
	global v_offs
	v_offs = int(input())
	print("Last thing I ask... Please send me a filename for the output:", end="\n")
	global filename
	filename = input()
	print("", end="\n\n")

def writing():
	while True:
		data = input()
		if data[0] == "_":
			if data == "_m":
				print("Select a new mode for the score:", end="\n")
				mode = input()
				l.set_mode(mode)
				print("I am working in " + l.mode + " mode now.", end="\n\n")
			elif data == "_n":
				print("Select a new notes set for the score:", end="\n")
				notes_set = [int(a) for a in input().split(" ")]
				l.new_notes_set(notes_set)
				print("I am working with " + l.notes_set_to_str() + "now.", end="\n\n")
			elif data == "_t":
				print("Select a new minumn duration:", end="\n")
				unit = float(input())
				l.set_t_unit(unit)
				print("I am working with " + str(l.t_unit) + "now.", end="\n\n")
			elif data == "_s":
				l.fill_last_measures()
				l.save_score("output/", filename, "xml")
			elif data == "_q":
				break
		else:
			l.add_cycle(data)

try:
	set_configuration()
except:
	print("\nSomething went wrong. Let's start over...", end="\n\n")
	set_configuration()

l = LevenScore(title, composer, key, t_sig, parts, mode, notes_set, t_unit, t_measure, offs, v_offs)

print("I am ready to work with you. Waiting for text...", end="\n\n")
try:
	writing()
except:
	print("\nYour last input destroyed my flow. I discarded that.", end="\n\n")
	writing()