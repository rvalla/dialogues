import warnings
warnings.filterwarnings('ignore')

from levenscore import LevenScore

text = open("data/borges_chess.txt", "r").readlines()

l = LevenScore("chess", "Jorge Luis Borges", 0, "2/4", 2, "crayfish", [0], 0.25, 2, 72, -12)
for t in text:
    l.add_cycle(t)
l.save_score("examples/", "borges_chess", "xml")
