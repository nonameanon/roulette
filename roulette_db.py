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
    print(f"<< User '{name}' is created >>")


def find_user(name):
    try:
        c.execute(f"SELECT * FROM users WHERE Name = '{name}'")
        if c.fetchone() is None:
            create_user(name)
        else:
            print(f"<< User '{name}' found on database >>")
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
            else:
                c.execute(f"UPDATE users SET NumBets = NumBets + 1 WHERE Name = '{name}'")
        except ValueError:
            print(f'<< Num is str: {value}>>')
            if attr == 'red':
                c.execute(f"UPDATE users SET RedBets = RedBets + 1 WHERE Name = '{name}'")
            elif attr == 'black':
                c.execute(f"UPDATE users SET BlackBets = BlackBets + 1 WHERE Name = '{name}'")
            elif attr == 'even':
                c.execute(f"UPDATE users SET EvenBets = EvenBets + 1 WHERE Name = '{name}'")
            elif attr == 'odd':
                c.execute(f"UPDATE users SET OddBets = OddBets + 1 WHERE Name = '{name}'")
            elif attr == '-18':
                c.execute(f"UPDATE users SET FirtsHalfBets = FirtsHalfBets + 1 WHERE Name = '{name}'")
            elif attr == '19-':
                c.execute(f"UPDATE users SET SecondHalfBets = SecondHalfBets + 1 WHERE Name = '{name}'")
            elif attr == '1-row':
                c.execute(f"UPDATE users SET FRowBets = FRowBets + 1 WHERE Name = '{name}'")
            elif attr == '2-row':
                c.execute(f"UPDATE users SET SRowBets = SRowBets + 1 WHERE Name = '{name}'")
            elif attr == '3-row':
                c.execute(f"UPDATE users SET TRowBets = TRowBets + 1 WHERE Name = '{name}'")
            elif attr == '1st':
                c.execute(f"UPDATE users SET FColBets = FColBets + 1 WHERE Name = '{name}'")
            elif attr == '2nd':
                c.execute(f"UPDATE users SET SColBets = SColBets + 1 WHERE Name = '{name}'")
            elif attr == '3rd':
                c.execute(f"UPDATE users SET TColBets = TColBets + 1 WHERE Name = '{name}'")
    else:
        c.execute(f"UPDATE users SET {attr} = {attr} + {value} WHERE Name = '{name}'")


# c.execute(f"UPDATE users SET MoneyBetted = MoneyBetted + {user.total_lose}, MoneyWon = MoneyWon + {user.total_wins}")
