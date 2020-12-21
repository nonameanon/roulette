import sqlite3 as sql

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

db = sql.connect('roulette.db')
c = db.cursor()


def create_user(name):
    c.execute(f"INSERT INTO users (Name, MoneyBetted, MoneyWon, NumBets, BlackBets, RedBets, FirtsHalfBets, "
              f"SecondHalfBets, EvenBets, OddBets, ZeroBets, FRowBets, SRowBets, TRowBets, "
              f"FColBets, SColBets, TColBets) VALUES ('{name}', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
    db.commit()
    # print(f"<< User '{name}' is created >>")


def find_user(name):
    try:
        c.execute(f"SELECT * FROM users WHERE Name = '{name}'")
        if c.fetchone() is None:
            create_user(name)
            # print(f"<< User '{name}' found on database >>")
    except sql.OperationalError:
        create_user(name)


def get_attr(name, attr):
    c.execute(f"SELECT {attr} FROM users WHERE Name = '{name}'")
    return c.fetchone()[0]


def update_value(name, attr, value):
    if attr == 'num':
        try:
            num = int(value)
            print(f'<< Num is int: {num}>>')
            if num == 0:
                c.execute(f"UPDATE users SET ZeroBets = ZeroBets + 1 WHERE Name = '{name}'")
            elif value == '-18':
                c.execute(f"UPDATE users SET FirtsHalfBets = FirtsHalfBets + 1 WHERE Name = '{name}'")
            else:
                c.execute(f"UPDATE users SET NumBets = NumBets + 1 WHERE Name = '{name}'")
            db.commit()
        except ValueError:
            print(f'<< Num is str: {value}>>')
            print('current value is', value)
            if value == 'red':
                c.execute(f"UPDATE users SET RedBets = RedBets + 1 WHERE Name = '{name}'")
            elif value == 'black':
                c.execute(f"UPDATE users SET BlackBets = BlackBets + 1 WHERE Name = '{name}'")
            elif value == 'even':
                c.execute(f"UPDATE users SET EvenBets = EvenBets + 1 WHERE Name = '{name}'")
            elif value == 'odd':
                c.execute(f"UPDATE users SET OddBets = OddBets + 1 WHERE Name = '{name}'")
            elif value == '19-':
                c.execute(f"UPDATE users SET SecondHalfBets = SecondHalfBets + 1 WHERE Name = '{name}'")
            elif value == '1-row':
                c.execute(f"UPDATE users SET FRowBets = FRowBets + 1 WHERE Name = '{name}'")
            elif value == '2-row':
                c.execute(f"UPDATE users SET SRowBets = SRowBets + 1 WHERE Name = '{name}'")
            elif value == '3-row':
                c.execute(f"UPDATE users SET TRowBets = TRowBets + 1 WHERE Name = '{name}'")
            elif value == '1st':
                c.execute(f"UPDATE users SET FColBets = FColBets + 1 WHERE Name = '{name}'")
            elif value == '2nd':
                c.execute(f"UPDATE users SET SColBets = SColBets + 1 WHERE Name = '{name}'")
            elif value == '3rd':
                c.execute(f"UPDATE users SET TColBets = TColBets + 1 WHERE Name = '{name}'")
            print('value setted')
            db.commit()
    else:
        c.execute(f"UPDATE users SET {attr} = {attr} + {value} WHERE Name = '{name}'")
    db.commit()


def sql_shell():
    while True:
        try:
            command = input('SQL >> ')
            if command.startswith('fetch'):
                command = command.split(' ')
                if command[0] == 'fetchall':
                    if len(command) > 1:
                        print(c.fetchall()[int(command[1])])
                    else:
                        for line in c.fetchall():
                            print(line)
                elif command[0] == 'fetchone':
                    print(c.fetchone())
            elif command.startswith('commit'):
                db.commit()
            elif command == 'quit' or command == 'exit':
                return
            else:
                c.execute(f'{command}')
        except sql.OperationalError:
            print('!!! Wrong command')


# c.execute(f"UPDATE users SET MoneyBetted = MoneyBetted + {user.total_lose}, MoneyWon = MoneyWon + {user.total_wins}")
