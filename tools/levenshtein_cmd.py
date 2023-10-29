from levenshtein import Levenshtein

lev = Levenshtein()
working = True
print(lev)
print("Waiting for a pair of words...", end="\n\n")

while working:
    data = input()
    if data == "q" or data == "Q":
        working = False
        break
    else:
        words = data.split(" ")
        print("\nI think the levenshtein's distance between " + words[0] + " and " + words[1] + " is", end=" ")
        d = lev.detailed_distance(words[0], words[1])
        print(str(d), end="\n\n")
        print("Waiting for a new pair of words...", end="\n\n")