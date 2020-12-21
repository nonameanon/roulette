def get_choice(max_val):
    while True:
        try:
            choice = int(input('>> '))
            if 0 < choice <= max_val:
                return choice
            else:
                print('!!! Wrong num')
                continue
        except ValueError:
            print('!!! Wrong num')
            continue


def debug_menu(user=None, users=None):
    def edit_user(user):
        print(f'1. Name: {user.name}')
        if user.bets:
            print(f'2. Bets: {user.bets}')
            choice = get_choice(2)
        else:
            choice = get_choice(1)
        if choice == 1:
            name = input('New name >> ')
            user.name = name
        elif choice == 2:
            i = 1
            for bet in user.bets:
                print(f'{i}. {bet}: {user.bets[bet]}')
                i += 1
            choice = get_choice(i - 1)
            bet = list(user.bets)[choice - 1]
            while True:
                try:
                    user.bets[bet] = int(input(f'{bet}: >> '))
                    break
                except ValueError:
                    print('!!! Wrong int')
                    continue

    print('DEBUG MENU:')
    if user:
        print('Current user:', user.name)
        print('1. Edit user')
    if users:
        print('2. Edit other users')
    print('3. Quit debug')
    choice = get_choice(3)
    if choice == 1:
        edit_user(user)
    elif choice == 2:
        for i in range(len(users)):
            print(f'{i+1}. {users[i].name}')
        choice = get_choice(len(users))
        edit_user(users[choice - 1])
