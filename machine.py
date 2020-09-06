# machine.py
# author: Ryosuke MATSUZAWA
# チューリングマシンをシミュレートするプログラム．
# 必要なモジュールの読み込み
from collections import defaultdict
import sys
import time
import subprocess


# 読み書き用のテープを定義する．引数は，テープの初期状態．
class Tape():
    def __init__(self, input_tape):
        # 何も書き込まれていない部分を参照した場合，空白(' ')を返す（collectioins.defaultdictを参照）
        self.content = defaultdict(lambda: ' ')
        # 初期状態の読み込み
        for number, character in zip(range(len(input_tape)), list(input_tape)):
            self.content[number] = character


# ヘッドを定義する．引数は読み書きテープ．
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
        self.head_input = self.tape.content[self.position]

    def head_write(self, character):
        self.tape.content[self.position] = character

    def change_state(self, next_state):
        self.state = next_state

    # テープの状態とヘッドの位置を，出力用に整形する．
    def print_tape_with_position(self):
        self.tape.content[self.position]
        tape_list = sorted(self.tape.content.items(), key=lambda item: item[0])

        # テープを，
        # - ヘッドより左にある文字列
        # - ちょうどヘッドの位置にある文字
        # - ヘッドより右側にある文字列
        # に分ける．
        list_less = [item[1] for item in tape_list if item[0] < self.position]
        just = [item[1] for item in tape_list if item[0] == self.position][0]
        list_over = [item[1] for item in tape_list if item[0] > self.position]

        # 各ステップに間合いをもたせる
        time.sleep(0.15)
        # コンソールのクリア
        subprocess.run('clear')

        if len(list_less) == 0:
            return ' '.join(list_less) + '[' + just + ']' + ' '.join(list_over)
        else:
            # ヘッドが左端に来たときに，テープの表示がずれてしまうを調整
            tape = ' ' + ' '.join(list_less) + '[' + just + ']'\
                   + ' '.join(list_over)
            return tape

    # テープの状態とヘッドの位置，ヘッドの状態(state)を出力する．
    def print_tape(self):
        tape_result = self.print_tape_with_position()
        print(tape_result + '\n\nstate:' + self.state + '\033[2E')

    # 命令に合わせて，一連の動き（テープの読み書き，ヘッドの移動・状態遷移，出力）を行う．
    def sequence(self, order):
        # ヘッドが受理状態ならば終了．
        if self.state == 'fin':
            print('Accept!')
            exit()

        # 状態とテープの文字がともに一致する命令があれば，それを実行する．
        if (self.state, self.head_input) == (order.now, order.head_input):
            self.head_write(order.head_output)
            self.print_tape()
            self.move[order.direction]()
            self.change_state(order.next)
            self.print_tape()
            return 0


# 命令を定義する．
# now: 現在のヘッドの状態
# head_input: テープから読み取った文字
# head_output: テープに書き込む文字
# direction: ヘッドの移動方向
# next: ヘッドの遷移先
class Order():
    def __init__(self, now, head_input, head_output, direction, next):
        self.now = str(now)
        self.head_input = str(head_input)
        self.head_output = str(head_output)
        self.direction = str(direction)
        self.next = str(next)


# 命令が書かれたファイルから，命令を読み取る
def load_order(order_file):
    with open(order_file) as file:
        line = [((i[:-1]).split(',')) for i in file.readlines()]
    try:
        return [Order(*order) for order in line]
    except TypeError as terror:
        print('Error: your orders_file may be invalid.\n')
        print(terror)
        exit(1)


# 実行できる命令がなければ，'reject!'を返して停止する．
# acceptされた場合の停止は，sequence()に記述されている．
def main_sequence(machine, orders):
    machine.head_read()
    for order in orders:
        if machine.sequence(order) == 0:
            break
    else:
        print('reject!')
        exit()


# メイン処理．ファイルからテープ・命令を読み込んで実行する．
def main(input_tape, orders_file):
    tape = Tape(input_tape)
    machine = Machine(tape)
    orders = load_order(orders_file)
    print('start!')
    machine.print_tape()
    while True:
        main_sequence(machine, orders)


# コマンドラインで実行するための処理．
# 実行方法：
# python machine.py tape_strings orders_file
# tape_strings: テープの初期状態となる文字列
# orders_file: 命令一式を書いたファイル
if __name__ == "__main__":
    if len(sys.argv) == 3:
        tape = sys.argv[1]
        orders_file = sys.argv[2]
        main(tape, orders_file)
    else:
        # 引数に過不足がある場合のエラーメッセージ
        print('----------------------------------------------------------')
        print('USAGE: python machine.py tape_strings orders_file')
        print('')
        print('tape_strings: strings that you would like to set as tape')
        print("orders_file: file in which machine's behavior is written")
        print('----------------------------------------------------------')
