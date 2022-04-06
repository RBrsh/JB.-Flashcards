import io
import sys
import argparse


class TermOrDefinitionExists(Exception):
    pass


class TermDoesNotExist(Exception):
    pass


class InOutInterceptor:
    def __init__(self):
        self.io_log = io.StringIO('')
        self.term_out = sys.stdout
        self.term_in = sys.stdin

    def readline(self):
        line = self.term_in.readline()
        self.io_log.write(line)
        return line

    def write(self, text: str):
        self.io_log.write(text)
        self.term_out.write(text)

    def flush(self):
        return getattr(self.term_in, 'flush')

    def get_log(self):
        return self.io_log.getvalue()


class CardsDeck:
    def __init__(self):
        self.cards_terms = []
        self.cards_definitions = []
        self.cards_terms_mistakes = []

    def add_card(self, term: str, definition: str, mistakes=0):
        if self.exists_term(term) or self.exists_definition(definition):
            raise TermOrDefinitionExists
        else:
            self.cards_terms.append(term)
            self.cards_definitions.append(definition)
            self.cards_terms_mistakes.append(mistakes)

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
                    self.add_mistake(term_index=i)
                else:
                    print(f'Wrong. The right answer is "{self.cards_definitions[i]}".')
                    self.add_mistake(term_index=i)

                counter += 1
                if counter >= ask_limit:
                    break

    def update_card(self, term: str, definition: str, mistakes=0):
        """
        TODO: Decide if mistakes counter should be reset while updating the term.
        :param term:
        :param definition:
        :param mistakes:
        :return:
        """
        if self.exists_term(term):
            self.cards_definitions[self.cards_terms.index(term)] = definition
        else:
            self.add_card(term, definition, mistakes)

    def export_cards(self) -> dict:
        return {t: [self.cards_definitions[k], self.cards_terms_mistakes[k]]
                for k, t in enumerate(self.cards_terms)}

    def add_mistake(self, term_index=None):
        """
        TODO: Implement accepting term itself in the future.
        :param term_index:
        :return:
        """
        if term_index is not None:
            self.cards_terms_mistakes[term_index] += 1

    def get_hardest_cards(self) -> list:
        if self.cards_terms_mistakes:
            max_mistakes = max(self.cards_terms_mistakes)
        else:
            max_mistakes = 0
        hardest_terms = []

        if max_mistakes > 0:
            mistake_index = 0
            while True:
                try:
                    mistake_index = self.cards_terms_mistakes.index(
                        max_mistakes, mistake_index)
                    hardest_terms.append([self.cards_terms[mistake_index],
                                          max_mistakes])
                    mistake_index += 1  # Offsetting index for the next search
                except ValueError:
                    break

        return hardest_terms

    def reset_stats(self):
        self.cards_terms_mistakes = [0] * len(self.cards_terms_mistakes)


def import_cards(cards_deck_obj, filename):
    with open(filename) as fh:
        counter = 0
        for line in fh:
            term_def = line.split(sep=';')
            cards_deck_obj.update_card(term_def[0].strip(),
                                       term_def[1].strip(),
                                       int(term_def[2].strip()))
            counter += 1
    return counter


def export_cards(cards_deck_obj, filename):
    cards_for_export = [f'{k};{v[0]};{v[1]}\n' for k, v in
                        cards_deck_obj.export_cards().items()]

    with open(filename, 'w') as fh:
        fh.writelines(cards_for_export)

    return len(cards_for_export)


def main():
    args_parser = argparse.ArgumentParser(description="Smth ab' this program.")
    args_parser.add_argument('--import_from')
    args_parser.add_argument('--export_to')
    args = args_parser.parse_args()

    cards_to_study = CardsDeck()
    sys.stdin = sys.stdout = InOutInterceptor()

    if args.import_from:
        try:
            import_result = import_cards(cards_to_study, args.import_from)
            print(f'{import_result} cards have been loaded.')
        except FileNotFoundError:
            print('File not found.')

    while True:
        user_input = input('\nInput the action (add, remove, import, export, '
                           'ask, exit, log, hardest card, reset stats):\n')
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
                import_result = import_cards(cards_to_study, filename)
                print(f'{import_result} cards have been loaded.')
            except FileNotFoundError:
                print('File not found.')
        elif user_input == "export":
            filename = input('File name:\n')
            cards_saved = export_cards(cards_to_study, filename)
            print(f'{cards_saved} cards have been saved.')
        elif user_input == "ask":
            times_to_ask = int(input('How many times to ask?\n'))
            cards_to_study.study(times_to_ask)
        elif user_input == 'hardest card':
            hardest_cards = cards_to_study.get_hardest_cards()

            if hardest_cards:
                hcl = len(hardest_cards)
                if hcl == 1:
                    print(f'The hardest card is "{hardest_cards[0][0]}". '
                          f'You have {hardest_cards[0][1]} errors '
                          f'answering it')
                else:
                    print('The hardest cards are',
                          *[f'"{v[0]}",' if i != hcl - 1 else f'"{v[0]}"'
                            for i, v in enumerate(hardest_cards)])
            else:
                print('There are no cards with errors.')
        elif user_input == 'reset stats':
            cards_to_study.reset_stats()
            print('Card statistics have been reset.')
        elif user_input == 'log':
            log_state = sys.stdin.get_log()  # Freezing log state
            with open(input('File name:'), 'w', encoding='utf-8') as fh:
                fh.write(log_state)
            print('The log has been saved.')
        elif user_input == "exit":
            print("Bye bye!")
            if args.export_to:
                cards_saved = export_cards(cards_to_study, args.export_to)
                print(f'{cards_saved} cards have been saved.')
            break


if __name__ == '__main__':
    main()
