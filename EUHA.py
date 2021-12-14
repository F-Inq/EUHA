from time import time, sleep
from keyboard import press_and_release, is_pressed
from winsound import PlaySound, SND_ALIAS
from random import uniform

eu_log = open(r'C:\Users\Flak\Documents\Entropia Universe\chat.log')
startup_time = time()
gun_shortcut = {
    'SA': '2',
    'RG': '3',
}


def read_log_line(logfile):  # reads a log line and returns it if it's not a chat message
    try:
        return logfile.readline()
    except UnicodeDecodeError:  # don't care if it's a message
        return ''


def get_dmg_and_gun(log_line, big_mob):  # extracts damage size from log line and returns a gun that has that damage
    dmg = float(log_line.split()[-4])
    raw_dmg = (dmg / 2) if ('Critical hit' in log_line) else dmg

    if raw_dmg < 2.5:
        gun = 'SA'
    elif 2.5 <= raw_dmg <= 5:
        gun = 'RG'
    elif raw_dmg >= 13:
        gun = 'LP-10'
        if not big_mob:
            dmg = dmg - 40  # same as (hp += 40) and big mobs have 40 hp more than usual mobs, logs look weird though
            big_mob = True
    else:
        gun = 'Bukin'

    return dmg, gun, big_mob


def apply_dmg(dmg, hp):  # returns new hp value after damage has been dealt to the mob
    return round(hp - dmg, 1)


def switch_guns(next_gun):  # mimics an actual keyboard key press with a shortcut for a gun
    sleep(round(uniform(0.1, 0.5), 3))  # i am very human, i press keys with delay
    press_and_release(gun_shortcut[next_gun])  # press a key that has a shortcut for next gun


def switch_to_next_gun(gun, hp):  # checks if a switch to next gun is needed and in that case switches guns
    if gun == 'Bukin':
        return 'Bukin'  # this gun is used for killing rare 1hp spawns, switching back is always manual

    if gun != 'RG' and 3 < hp < 20:
        next_gun = 'RG'
    elif gun != 'SA' and 0 < hp < 3.1:
        next_gun = 'SA'
    else:
        next_gun = gun

    if next_gun != gun:
        switch_guns(next_gun)

    return next_gun


def lasthit_handler(gun, hp, big_mob):  # checks if last damage killed the mob
    global same_mob
    if hp <= 0:
        same_mob = False  # if mob is dead - start over (loop is while same_mob:)
        if gun != 'RG':
            switch_guns('RG')  # whatever gun was used last, switch back to RG
    else:  # if mob is not dead, continue with same hp and size
        one_mob(hp, big_mob)


def print_info(dmg, gun, hp, big_mob):  # logs to console after each shot
    print(f'Damage = {dmg}'
          f'Weapon is {gun}'
          f'HP = {hp}'
          f'Mob is {"Big" if big_mob else "Small"}\n')


def one_mob(hp, big_mob):  # main function, consisting of all steps of killing one mob
    global same_mob
    while same_mob:
        line = read_log_line(eu_log)
        if '[System] []' in line and 'You inflicted' in line:  # check if damage was dealt
            dmg, gun, big_mob = get_dmg_and_gun(line, big_mob)
            hp = apply_dmg(dmg, hp)
            # print_info(dmg, gun, hp, big_mob)  # uncomment to write logs to console
            gun = switch_to_next_gun(gun, hp)
            lasthit_handler(gun, hp, big_mob)
        elif is_pressed('`'):  # if something went wrong, reset by pressing `
            print('-')
            same_mob = False
            sleep(0.2)
        else:
            continue  # read next log
    else:
        return  # when mob is dead, start over with same_mob = True


while time() < startup_time + 3:  # Delay to skip the old logs
    read_log_line(eu_log)
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
print('Ready')

while True:
    same_mob = True  # set same_mob back to True on each new mob
    PlaySound('*', SND_ALIAS)  # sound signal for mob is dead and start of the hunt
    # print('-----\n\n')  # UNCOMMENT TO DIVIDE LOGS
    one_mob(9.9, False)
