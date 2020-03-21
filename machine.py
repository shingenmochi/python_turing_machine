from collections import defaultdict
import os
import sys
import time


class Tape():
    def __init__(self, input_tape):
        self.content = defaultdict(lambda: ' ')
        for number, character in zip(range(len(input_tape)), list(input_tape)):
            self.content[number] = character


class Machine():
    def __init__(self, setted_tape):
        self.tape = setted_tape
        self.position = 0
        self.state = 's0'
        self.head_input = ''
        self.head_output = ''
        self.move = {'L': self.move_left, 'R': self.move_right, 'S': self.stay}

    def move_left(self):
        self.position -= 1

    def move_right(self):
        self.position += 1

    def stay(self):
        pass  # 移動しない

    def head_read(self):
        # return self.tape.content[self.position]
        self.head_input = self.tape.content[self.position]

    def head_write(self, character):
        self.tape.content[self.position] = character

    def change_state(self, next_state):
        self.state = next_state

    def print_tape_with_position(self):
        tape_list = sorted(self.tape.content.items(), key=lambda item: item[0])
        list_less = [item[1] for item in tape_list if item[0] < self.position]
        just = [item[1] for item in tape_list if item[0] == self.position][0]
        list_over = [item[1] for item in tape_list if item[0] > self.position]
        time.sleep(0.1)
        os.system('clear')
        if len(list_less) == 0:
            print(' '.join(list_less) + '[' + just + ']' + ' '.join(list_over))
        else:
            # [分のズレを調整
            tape = ' ' + ' '.join(list_less) + '[' + just + ']'\
                   + ' '.join(list_over)
            print(tape)

    def sequence(self, order):
        if self.state == 'fin':
            print('Accept!')
            exit()
        if (self.state, self.head_input) == (order.now, order.head_input):
            self.head_write(order.head_output)
            self.print_tape_with_position()
            self.move[order.direction]()
            self.change_state(order.next)
            print('\nstate:', self.state)
            return 0


class Order():
    def __init__(self, now, head_input, head_output, direction, next):
        self.now = str(now)
        self.head_input = str(head_input)
        self.head_output = str(head_output)
        self.direction = str(direction)
        self.next = str(next)


def load_order(order_file):
    with open(order_file) as file:
        line = [((i[:-1]).split(',')) for i in file.readlines()]
    try:
        return [Order(*order) for order in line]
    except TypeError as terror:
        print('Error: your orders_file may be invalid.\n')
        print(terror)
        exit(1)


def main_sequence(machine, orders):
    machine.head_read()
    machine.print_tape_with_position()
    print('\nstate:', machine.state)

    for order in orders:
        if machine.sequence(order) == 0:
            break
    else:
        print('reject!')
        exit()


def main(input_tape, orders_file):
    tape = Tape(input_tape)
    machine = Machine(tape)
    orders = load_order(orders_file)
    print('start!')
    while True:
        main_sequence(machine, orders)


if len(sys.argv) == 3:
    tape = sys.argv[1]
    orders_file = sys.argv[2]
    main(tape, orders_file)
else:
    print('----------------------------------------------------------')
    print('USAGE: python machine.py tape_strings orders_file')
    print('')
    print('tape_strings: strings that you would like to set as tape')
    print("orders_file: file in which machine's behavior is written")
    print('----------------------------------------------------------')
