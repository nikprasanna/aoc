import math
from collections import defaultdict
from typing import Set, List, Dict

FILENAME = "./aoc4.txt"

with open(FILENAME) as file:
    raw_data = [line.rstrip() for line in file]

class Ticket:
    winning_nums = Set[int]
    ticket_nums = Set[int]
    ticket_number = int

    def __init__(self, raw_card_data: str):
        self.winning_nums = set()
        self.ticket_nums = set()

        self.populate_nums(raw_card_data)

    def populate_nums(self, raw_data: str):
        self.ticket_number = int(raw_data.split(':')[0].split(' ')[-1])
        self.winning_nums = set([int(x) for x in raw_data.split(':')[1].split('|')[0].strip().split(' ') if x])
        self.ticket_nums = set([int(x.strip()) for x in raw_data.split('|')[1].strip().split(' ') if x])

    def get_score(self) -> int:
        winning_count = len(self.ticket_nums.intersection(self.winning_nums))
        # if not winning_count:
        #     return 0
        #
        # score = 2**(winning_count-1)
        return winning_count


class TicketPile:
    tickets: List[Ticket]
    ticket_count_map: Dict[int, int]

    def __init__(self, raw_data: List[str]):
        self.tickets = []
        self.ticket_count_map = defaultdict(lambda: 1)

        for data in raw_data:
            self.tickets.append(Ticket(data))

    def play_game(self):
        ticket_length = len(self.tickets)

        for i in range(0, ticket_length):
            iterations = self.ticket_count_map[i]
            ticket = self.tickets[i]
            score = ticket.get_score()
            for _ in range(iterations):
                self.add_score(curr_index=i, score=score)

        print(self.ticket_count_map)

    def add_score(self, curr_index: int, score: int):
        for i in range(curr_index+1, curr_index+score+1):
            self.ticket_count_map[i] += 1

    def get_total_score(self) -> int:
        return sum(list(self.ticket_count_map.values()))


ticket_pile = TicketPile(raw_data)
for ticket in ticket_pile.tickets:
    print(ticket.get_score())

ticket_pile.play_game()
print('Total score:', ticket_pile.get_total_score())