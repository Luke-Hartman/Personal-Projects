import random as r

Guesses = []

for a in range(6):
    for b in range(6):
        for c in range(6):
            for d in range(6):
                Guesses.append(str(a) + str(b) + str(c) + str(d))

def check(Guess, Answer):
    Results = [0,0]
    Refrenced1 = [0,0,0,0]
    Refrenced2 = [0,0,0,0]
    for a in range(4):
        if Guess[a] == Answer[a]:
            Results[0] += 1
            Refrenced1[a] = 1
            Refrenced2[a] = 1
    for a in range(4):
        if Refrenced1[a] == 0:
            for b in range(4):
                if Refrenced2[b] == 0:
                    if Guess[a] == Answer[b]:
                        Results[1] += 1
                        Refrenced1[a] = 1
                        Refrenced2[b] = 1
                        break
    return Results

for i in range(10):
    Guess = r.choice(Guesses)
    print Guess
    Results = [0,0]
    Results[0] = input("How many are exactly correct? ")
    if Results[0] == 4:
        print "Done"
        break
    Results[1] = input("How many are the right number, but in the wrong place? ")
    NewGuesses = []
    for a in Guesses:
        if check(a, Guess) == Results:
            NewGuesses.append(a)
    Guesses = NewGuesses
