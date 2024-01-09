import random

specialchars = "&“”\"(),/—--:#;+"
punct = "!?" #replace w/ period
start = "<START>"
end = "<END>"
ctr = "<COUNT>"
word_limit = 300
# these vars are implicitly global somehow

class BioIterator():
    def __init__(self):
        self.idx = 0
        with open('bios.txt', 'r') as file:
            self.arr = list(file.readlines())

    def hasNext(self):
        return self.idx < len(self.arr)

    def getNext(self):
        output = ""
        while self.hasNext() and self.arr[self.idx].strip():
            temp = self.arr[self.idx].strip() + " "
            temp = temp.replace("Dr.", "Dr")
            temp = temp.replace("Mr.", "Mr")
            temp = temp.replace("Ms.", "Ms")
            for c in punct:
                temp = temp.replace(c, '.')
            for c in specialchars:
                temp = temp.replace(c, ' ')
            output += temp
            self.idx += 1
        self.idx += 1
        return output

class SentenceIterator():
    def __init__(self, text):
        self.sentence_list = text.split(".")
    
    def hasNext(self):
        return len(self.sentence_list) != 0
    
    def getNext(self):
        if self.hasNext():
            output = self.sentence_list.pop(0)
            return output.split()

class BigramCounter():
    def __init__(self):
        self.freqs = {start: {ctr: 0}}

    def add(self, prev, nxt):
        if prev in self.freqs:
            if nxt in self.freqs[prev]:
                self.freqs[prev][nxt] += 1
            else:
                self.freqs[prev][nxt] = 1
            self.freqs[prev][ctr] += 1
        else:
            self.freqs[prev] = {nxt: 1, ctr: 1}
    
    def get(self, word):
        return self.freqs[word]
    
    def printAll(self):
        print(self.freqs)

class SentenceGenerator():
    def __init__(self, bigram_freqs):
        self.curr = start # will always begin with start
        self.bigram_freqs = bigram_freqs

    def getNext(self):
        output = ""
        word_ct = 0
        while self.curr != end:
            output += self.getWord() + " "
            word_ct += 1
        output = output.strip()
        output += "."
        self.curr = start # re-initializes for the next sentence to be generated
        return output, (word_ct - 1) # account for "end"

    def getWord(self):
        possible_next = self.bigram_freqs.get(self.curr)
        total = possible_next[ctr]
        idx = random.randint(1, total)
        
        for i in possible_next:
            if i != ctr and possible_next[i] >= idx:
                self.curr = i
                return i if i != end else ""
            elif i != ctr:
                idx -= possible_next[i]
        print("well shit somethign went wrong")

    
# Initializing the line iterator + bigram counter
bio_iterator = BioIterator()
freqs = BigramCounter()

while bio_iterator.hasNext():
    curr = bio_iterator.getNext()
    sentence_iterator = SentenceIterator(curr)

    while sentence_iterator.hasNext():
        word_list = sentence_iterator.getNext()
        if word_list:
            for i in range(len(word_list)):
                if i == 0:
                    freqs.add(start, word_list[i])
                else:
                    freqs.add(word_list[i - 1], word_list[i])
            freqs.add(word_list[-1], end)

# freqs.printAll()
# Begin generating sentences until word cap is reached
generator = SentenceGenerator(freqs)
output = ""
total_word_ct = 0
while total_word_ct <= word_limit:
    sentence, word_ct = generator.getNext()
    total_word_ct += word_ct

    if total_word_ct <= word_limit:
        output += sentence + "\n"

# Returns output in "output.txt"
writer = open("output.txt", "w")
writer.write(output)
print("Generation complete; see 'output.txt' for your Physics Team")

