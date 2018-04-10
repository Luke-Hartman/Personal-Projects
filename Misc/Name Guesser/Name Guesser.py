from datetime import date
this_year = date.today().year

print("This program assists you in guessing somebody's name using only true/false questions.")
print("Guess a minimum bound for their age (no big deal if it is too high/low)")
min_age = int(input("> "))
print("Guess a maximum bound for their age")
max_age = int(input("> "))
print("Guess their gender (M/F)")
guess_gender = input("> ")

min_yob = this_year - max_age
max_yob = this_year - min_age

names_frequencies_by_yob_alphabetical = []
for yob in range(min_yob, max_yob + 1):
    f = open("names/yob%s.txt" % (yob), 'r')
    names_frequencies = []
    while True:
        line = f.readline()
        if line == "":
            break
        name, gender_str, frequency_str = line.split(",")
        if gender_str == guess_gender:
            names_frequencies.append((name, int(frequency_str)))

    names_frequencies.sort(key=lambda i: i[0], reverse=True)
    names_frequencies_by_yob_alphabetical.append(names_frequencies)
    f.close()

names_frequencies_alphabetical = []
done = False

while True:
    done = True
    min_name = "z"
    min_lists = []
    for i in range(len(names_frequencies_by_yob_alphabetical)):
        list = names_frequencies_by_yob_alphabetical[i]
        if len(list) == 0:
            continue
        done = False
        name, frequency = list[-1]
        if name < min_name:
            min_name = name
            min_lists = [i]
        elif name == min_name:
            min_lists.append(i)
    if done:
        break
    total_frequency = sum(names_frequencies_by_yob_alphabetical[i].pop()[1] for i in min_lists)
    names_frequencies_alphabetical.append((min_name, total_frequency))

integrated_table = [names_frequencies_alphabetical[0][1]]
for i in range(1, len(names_frequencies_alphabetical)):
    integrated_table.append(names_frequencies_alphabetical[i][1] + integrated_table[i - 1])

n_guesses = 1
meta_start_index = 0
meta_end_index = len(names_frequencies_alphabetical)
while meta_start_index < meta_end_index:
    target = (integrated_table[meta_start_index] + integrated_table[meta_end_index-1])//2
    start = 0
    stop = len(names_frequencies_alphabetical)
    while start < stop:
        guess = (start + stop)//2
        if integrated_table[guess] < target:
            start = guess + 1
        else:
            stop = guess
    ask_index = start
    print("Ask the person if their name comes after %s alphabetically (Y/N)" % (names_frequencies_alphabetical[ask_index][0]))
    answer = input("> ")
    if answer == "Y":
        meta_start_index = ask_index + 1
    else:
        meta_end_index = ask_index
    n_guesses += 1
print("Their name is %s, or is too uncommon to be found (or they lied)" % (names_frequencies_alphabetical[meta_start_index][0]))
print("Number of guesses used %s" % (n_guesses))