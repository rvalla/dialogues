class Levenshtein():
    
    #Measuring Levenshtein distance dinamically...
    #https://en.wikipedia.org/wiki/Levenshtein_distance#Iterative_with_full_matrix
    def distance(self, word_a, word_b):
       m = self.compute_matrix(word_a, word_b, len(word_a), len(word_b))
       return m[len(m)-1][len(m[0])-1]

    #Getting details from a distance computation...
    def detailed_distance(self, word_a, word_b):
        m = self.compute_matrix(word_a, word_b, len(word_a), len(word_b))
        s = "Computing distance between " + word_a + " and " + word_b + ":\n\n"
        s += self.get_matrix_string(word_a, word_b, m)
        s += "\n\n"
        s += "Distance = " + str(m[len(m)-1][len(m[0])-1])
        return s

    #Building the matrix to compute Levenshtein distance between two words...
    def compute_matrix(self, word_a, word_b, a, b):
        #We create the matrix of len(word_a) + 1 rows and len(word_b) + 1 columns
        m = self.build_empty_matrix(a, b)
        
        #Now we compute Levenshtein distance between all prefixes...
        for r in range(a):
            for c in range(b):
                #We check if both characters are equal...
                x = 1
                if word_a[r] == word_b[c]:
                    x = 0
                m[r+1][c+1] = min([
                                m[r+1][c] + 1, #insertion vs deletion vs replacement
                                m[r][c+1] + 1,
                                m[r][c] + x
                            ])
        return m
    
    #Building an empty matrix to work with...
    def build_empty_matrix(self, a, b):
        m = [[n for n in range(b + 1)]]        
        for i in range (1, a + 1):
            m.append([0 for n in range(b+1)])
        for i in range(1,len(m)):
            m[i][0] = i
        return m
    
    def get_matrix_string(self, word_a, word_b, matrix):
        s = ""
        a = " " + word_a
        b = "  " + word_b
        for l in b:
            s += "  "
            s += l
            s += " "
        s += "\n"
        for r in range(len(matrix)):
            s += "  "
            s += a[r]
            s += " "
            for c in range(len(matrix[0])):
                s += " "
                if matrix[r][c] < 10:
                    s += " "
                s += str(matrix[r][c])
                s += " "
            s += "\n"
        return s   

    #Printing class information...
    def __str__(self):
        return "I am a class with the power of computing the Levenshtein distance between words!\n" + \
                "Because of that I know that the distance between 'matrix' and 'mattress' is 4."