number_of_cards = int(input('Input the number of cards:\n'))
cards = []

for i in range(1, number_of_cards + 1):
    cards.append([input(f'The term for card #{i}:\n'),
                  input(f'The definition for card #{i}:\n')])

for i in cards:
    if input(f'Print the definition of "{i[0]}":\n') == i[1]:
        print('Correct!')
    else:
        print(f'Wrong. The right answer is "{i[1]}".')
