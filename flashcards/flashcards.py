number_of_cards = int(input('Input the number of cards:\n'))
cards_terms = []
cards_definitions = []

for i in range(1, number_of_cards + 1):
    term = input(f'The term for card #{i}:\n')

    while term in cards_terms:
        term = input(f'The term "{term}" already exists. Try again:\n')

    cards_terms.append(term)

    definition = input(f'The definition for card #{i}:\n')

    while definition in cards_definitions:
        definition = input(f'The definition "{definition}" already exists. Try again:\n')

    cards_definitions.append(definition)


for i in enumerate(cards_terms):
    answer = input(f'Print the definition of "{i[1]}":\n')
    if answer == cards_definitions[i[0]]:
        print('Correct!')
    elif answer in cards_definitions:
        print(f'Wrong. The right answer is "{cards_definitions[i[0]]}", but your definition is correct for '
              f'"{cards_terms[cards_definitions.index(answer)]}".')
    else:
        print(f'Wrong. The right answer is "{cards_definitions[i[0]]}".')
