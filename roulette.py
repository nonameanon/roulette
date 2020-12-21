import sqlite3 as sql
import roulette_db as db
import menu

TABLE = {0: ['0'],
         32: ['32', 'red', '2-row', '3rd', 'even', '19-'],
         15: ['15', 'black', '1-row', '2nd', 'odd', '-18'],
         19: ['19', 'black', '3-row', '2nd', 'odd', '19-'],
         4: ['4', 'black', '3-row', '1st', 'even', '-18'],
         21: ['21', 'red', '1-row', '2nd', 'odd', '19-'],
         2: ['2', 'red', '2-row', '1st', 'even', '-18'],
         25: ['25', 'red', '3-row', '3rd', 'odd', '19-'],
         17: ['17', 'black', '2-row', '2nd', 'odd', '-18'],
         34: ['34', 'red', '3-row', '3rd', 'even', '19-'],
         6: ['6', 'black', '1-row', '1st', 'even', '-18'],
         27: ['27', 'red', '1-row', '3rd', 'odd', '19-'],
         13: ['13', 'black', '3-row', '2nd', 'odd', '-18'],
         36: ['36', 'red', '1-row', '3rd', 'even', '19-'],
         11: ['11', 'black', '2-row', '1st', 'odd', '-18'],
         30: ['30', 'red', '1-row', '3rd', 'even', '19-'],
         8: ['8', 'black', '2-row', '1st', 'even', '-18'],
         23: ['23', 'red', '2-row', '2nd', 'odd', '19-'],
         10: ['10', 'black', '3-row', '1st', 'even', '-18'],
         5: ['5', 'red', '2-row', '1st', 'odd', '-18'],
         24: ['24', 'black', '1-row', '2nd', 'even', '19-'],
         16: ['16', 'red', '3-row', '2nd', 'even', '-18'],
         33: ['33', 'black', '1-row', '3rd', 'odd', '19-'],
         1: ['1', 'red', '3-row', '1st', 'odd', '-18'],
         20: ['20', 'black', '2-row', '2nd', 'even', '19-'],
         14: ['14', 'red', '2-row', '2nd', 'even', '-18'],
         31: ['31', 'black', '3-row', '3rd', 'odd', '19-'],
         9: ['9', 'red', '1-row', '1st', 'odd', '-18'],
         22: ['22', 'black', '3-row', '2nd', 'even', '19-'],
         18: ['18', 'red', '1-row', '2nd', 'even', '-18'],
         29: ['29', 'black', '2-row', '3rd', 'odd', '19-'],
         7: ['7', 'red', '3-row', '1st', 'odd', '-18'],
         28: ['28', 'red', '3-row', '3rd', 'even', '19-'],
         12: ['12', 'red', '1-row', '1st', 'even', '-18'],
         35: ['35', 'black', '2-row', '3rd', 'odd', '19-'],
         3: ['3', 'red', '1-row', '1st', 'odd', '-18'],
         26: ['26', 'black', '2-row', '3rd', 'even', '19-']}
COMBOS2X = ['red', 'black', 'even', 'odd', '-18', '19-']
COMBOS3X = ['1-row', '2-row', '3-row', '1st', '2nd', '3rd']


"""
TABLE VALUES:
users (
ID INTEGER PRIMARY KEY, 
Name varchar(255) NOT NULL, 
MoneyBetted int, 
MoneyWon int, 
NumBets int, 
BlackBets int, 
RedBets int, 
FirtsHalfBets int, 
SecondHalfBets int, 
EvenBets int, 
OddBets int,
ZeroBets int, 
FRowBets int, 
SRowBets int, 
TRowBets int, 
FColBets int, 
SColBets int, 
TColBets int))
"""

all_users = []


class User:
    def __init__(self, name):
        db.find_user(name)
        self.name = name
        self.id = db.get_attr(self.name, 'ID')
        self.bets = dict()
        self.win = False
        self.total_wins = 0
        self.total_lose = 0

    def add_bet(self, num, mon):
        if num in self.bets.keys():
            self.bets[num] += mon
        else:
            self.bets[num] = mon
        self.total_lose -= mon
        db.update_value(self.name, 'MoneyBetted', mon)
        db.update_value(self.name, 'num', num)

    def total_round(self):
        res = 0
        for i in self.bets.values():
            res += i
        self.total_wins += res
        return res

    def total_game(self):
        res = self.total_wins+self.total_lose
        return res

    def save(self, attr, val):
        pass


def check_user(users, name):
    for u in users:
        if name.lower() in u.name.lower():
            return u
    u = User(name)
    users.append(u)
    return u


def get_users():
    global all_users
    users = []
    while True:
        name = input('Name   >> ')
        if name == 'quit' or name == 'exit':
            break
        user = check_user(all_users, name)
        try:
            num_bet = input('Bet on >> ')
            if num_bet not in check_table() and int(num_bet) not in TABLE.keys():
                print('!!! Wrong bet')
                continue
            mon_bet = int(input('Money  >> '))
        except ValueError:
            print('!!! Wrong int')
            continue
        except KeyboardInterrupt:
            menu.debug_menu(user, users)
            continue
        user.add_bet(num_bet, mon_bet)
        if user.name not in [u.name for u in users]:
            users.append(user)
        print('-'*20)

    print('-'*40)
    print('\n'.join(['{:<20}|{:<5}'.format(u.name[:20], str(u.bets)) for u in users]))
    print('-'*40)
    return users


def check_table():
    a = {'nums': 0, 'black': 0, 'red': 0, 'even': 0, 'odd': 0,
         '1-row': 0, '2-row': 0, '3-row': 0,
         '1st': 0, '2nd': 0, '3rd': 0,
         '-18': 0, '19-': 0, 0: 0}
    for key in TABLE:
        for value in TABLE[key]:
            if value in a.keys():
                a[value] += 1
        a['nums'] += 1

    # for key in a:
    #     print(f'{key} : {a[key]}')

    return a.keys()


def get_winners(users):
    win_num = None
    win_combos = []
    try:
        win_num = int(input('\n...And winning number is >> '))
    except ValueError:
        print('!!! Wrong int !!!')
        get_winners(users)
    if win_num in TABLE.keys():
        win_combos = TABLE[win_num]
    else:
        print('Пиздишь')
        get_winners(users)

    winners = []

    print()
    print('-'*70)
    print('{:^20}|{:^20}|{:^20}|{:^10} '.format('User', 'Bets', 'Won', 'Total'))
    print('-' * 70)
    for u in users:
        for bet in u.bets:
            if bet in win_combos:
                if u not in winners:
                    winners.append(u)
                if bet in COMBOS2X:
                    u.bets[bet] *= 2
                elif bet in COMBOS3X:
                    u.bets[bet] *= 3
                else:
                    u.bets[bet] *= 36
            else:
                u.bets[bet] = 0
        db.update_value(u.name, 'MoneyWon', u.total_round())
        print('{:<20}|{:<20}|{:<20}|{:<10}'.format(u.name[:20],
                                                   ', '.join(u.bets.keys()),
                                                   ', '.join([str(bet) for bet in u.bets.values()]),
                                                   u.total_round()))
    print('-'*70)
    print('Победители: ')
    for winner in winners:
        print(f'{winner.name}: {winner.total_round()}')

    for u in users:
        u.bets = dict()


def game():
    while True:
        get_winners(get_users())
        a = input('\nContinue?(y/n) >> ')
        if a == 'y' or a == 'yes':
            continue
        else:
            break

    print()
    print('-'*50)
    print('Session results:')
    print('{:^20}|{:^10}|{:^10}|{:^10}'.format('Name', 'Won', 'Lost', 'Total'))
    print('-'*50)
    for u in all_users:
        res = str(u.total_game())
        print('{:<20}|{:<10}|{:<10}|{:<10}'.format(u.name[:20], str(u.total_wins), str(u.total_lose), res))
    print('-'*50)
    main_menu()


def main_menu():
    print('-'*30)
    print('ROULETTE: SHIKME EDITION')
    print('-' * 30)
    print('1. Start the game')
    print('2. Check DB')
    print('3. Exit')
    print('-' * 30)
    choice = menu.get_choice(3)
    if choice == 1:
        game()
    elif choice == 2:
        db.sql_shell()
        main_menu()
    elif choice == 3:
        quit()
    else:
        main_menu()


main_menu()
