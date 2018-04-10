import random as r

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
	
	
# Guess =  [5, 0, 1, 2]
# Answer = [5, 5, 2, 3]
'''


'''
print("Welcome to my game of Mastermind! Guess a 4 digit number composed of only 0-5.")

while True:
    Answer = str(r.randint(0,5)) + str(r.randint(0,5)) + str(r.randint(0,5)) + str(r.randint(0,5))
    print("New Game:")
    for i in range(10):
        Guess = raw_input("What is your guess? ")
        Results = check(Guess, Answer)
        if Results[0] == 4:
            print("Congratz you guessed it exactly right!")
            Success = 1
            break
        print("You had " + str(Results[0]) + " which were exactly correct.")
        print("You had " + str(Results[1]) + " which were the right number, but in the wrong place.")
    if Success == 0:
        print("Sorry, you were unable to correctly guess the answer within the allowed 10 turns.")
        print("Correct answer was " + Answer + ".")
