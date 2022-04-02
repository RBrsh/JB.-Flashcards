class TermDoesNotExist(Exception):
    pass


class CardsDeck:
    def __init__(self):
        self.cards_terms = []
        self.cards_definitions = []

    def add_card(self, term: str, definition: str):
        if self.exists_term(term) or self.exists_definition(definition):
            raise TermOrDefinitionExists
        else:
            self.cards_terms.append(term)
            self.cards_definitions.append(definition)

    def exists_term(self, term: str) -> bool:
        if term in self.cards_terms:
            return True
        return False

    def exists_definition(self, definition: str) -> bool:
        if definition in self.cards_definitions:
            return True
        return False

    def remove_term(self, term: str):
        if self.exists_term(term):
            del self.cards_definitions[self.cards_terms.index(term)]
            self.cards_terms.remove(term)
        else:
            raise TermDoesNotExist

    def study(self, ask_limit: int):
        counter = 0
        cards_available = len(self.cards_terms)

        if ask_limit <= cards_available:
            cards_limit = ask_limit
        else:
            cards_limit = cards_available

        while counter < ask_limit:
            for i in range(cards_limit):
                answer = input(f'Print the definition of "{self.cards_terms[i]}":\n')
                if answer == self.cards_definitions[i]:
                    print('Correct!')
                elif self.exists_definition(answer):
                    print(f'Wrong. The right answer is "{self.cards_definitions[i]}",'
                          f' but your definition is correct for '
                          f'"{self.cards_terms[self.cards_definitions.index(answer)]}".')
                else:
                    print(f'Wrong. The right answer is "{self.cards_definitions[i]}".')

                counter += 1
                if counter >= ask_limit:
                    break

    def update_card(self, term: str, definition: str):
        if self.exists_term(term):
            self.cards_definitions[self.cards_terms.index(term)] = definition
        else:
            self.add_card(term, definition)

    def export_cards(self) -> dict:
        return {t: self.cards_definitions[k] for k, t in enumerate(self.cards_terms)}


def main():
    cards_to_study = CardsDeck()

    while True:
        user_input = input('\nInput the action (add, remove, import, export, ask, exit):\n')
        if user_input == 'add':
            print("The card:")
            while True:
                term = input()
                if cards_to_study.exists_term(term):
                    print(f'The card "{term}" already exists. Try again:')
                else:
                    break

            print('The definition of the card:')
            while True:
                definition = input()

                if cards_to_study.exists_definition(definition):
                    print(f'The definition "{definition}" already exists. Try again:')
                else:
                    break

            cards_to_study.add_card(term, definition)
            print(f'The pair ("{term}":"{definition}") has been added.')
        elif user_input == "remove":
            term = input('Which card?\n')
            try:
                cards_to_study.remove_term(term)
                print('The card has been removed.\n')
            except TermDoesNotExist:
                print(f'Can\'t remove "{term}": there is no such card.\n')
        elif user_input == "import":
            filename = input('File name:\n')
            try:
                with open(filename) as fh:
                    counter = 0
                    for line in fh:
                        term_def = line.split(sep=';')
                        cards_to_study.update_card(term_def[0].strip(),
                                                   term_def[1].strip())
                        counter += 1

                    print(f'{counter} cards have been loaded.')
            except FileNotFoundError:
                print('File not found.')
        elif user_input == "export":
            cards_for_export = [f'{k};{v}\n' for k, v in cards_to_study.export_cards().items()]

            filename = input('File name:\n')
            with open(filename, 'w') as fh:
                fh.writelines(cards_for_export)
                print(f'{len(cards_for_export)} cards have been saved.')
        elif user_input == "ask":
            times_to_ask = int(input('How many times to ask?\n'))
            cards_to_study.study(times_to_ask)
        elif user_input == "exit":
            print("Bye bye!")
            break


if __name__ == '__main__':
    main()
