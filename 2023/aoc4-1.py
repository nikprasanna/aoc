import math
from typing import Set, List

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
        if not winning_count:
            return 0

        score = 2**(winning_count-1)
        return score


class TicketPile:
    tickets: List[Ticket]

    def __init__(self, raw_data: List[str]):
        self.tickets = []
        for data in raw_data:
            self.tickets.append(Ticket(data))

    def get_total_score(self) -> int:
        return sum([ticket.get_score() for ticket in self.tickets])


ticket_pile = TicketPile(raw_data)
for ticket in ticket_pile.tickets:
    print(ticket.get_score())

print('Total score:', ticket_pile.get_total_score())