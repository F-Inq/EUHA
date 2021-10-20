from time import time, sleep
from keyboard import press_and_release, read_key
from winsound import PlaySound, SND_ALIAS
import random

eu_log = open(r'C:\Users\Flak\Documents\Entropia Universe\chat.log')
startup_time = time()

while time() < startup_time + 3:  # Delay to skip the old logs
    try:
        eu_log.readline()
    except UnicodeDecodeError:
        pass
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nReady')


def one_mob(hp, gun):
    global same_mob
    while same_mob:
        try:
            line = eu_log.readline()
        except UnicodeDecodeError:  # don't care if it's a message
            line = ''
        if '[System] []' in line and 'You inflicted' in line:  # check if damage dealt
            dmg = float(line.split()[-4])  # extract damage size
            if dmg > 12.9:
                if gun != 'LP-10':  # check if using LP-10
                    hp = hp + 40  # if using LP-10 (for the first time), then mob is big
                    gun = 'LP-10'
            hp = round(hp - dmg, 1)  # substract hp from mob
            if gun == 'LP-10' and 3 < hp < 20:  # switch guns if big mob has <20 hp
                sleep(round(random.uniform(0, 0.6), 3))  # i am very human i press keys with delay
                press_and_release('3')  # switch to RG
                gun = 'RG'
            elif gun != 'SA' and 0 < hp < 3.1:  # switch guns if any mob has <3 hp
                sleep(round(random.uniform(0, 0.5), 3))
                press_and_release('2')  # switch to SA
                gun = 'SA'
            if hp <= 0:  # if mob is dead, start over
                same_mob = False
                if gun != 'RG':  # whatever gun was used, switch back to RG
                    sleep(round(random.uniform(0.1, 0.6), 3))
                    press_and_release('3')
                    gun = 'RG'
            else:  # if mob is not dead, continue with same hp and gun
                one_mob(hp, gun)
        elif read_key() == '`':  # if something went wrong, reset
            print('-')
            sleep(0.2)  # read_key() can sometimes work multiple times
            same_mob = False
        else:
            continue  # read next log
    else:
        return  # when mob is dead, start over with same_mob = True


while True:
    same_mob = True
    PlaySound('*', SND_ALIAS)  # sound signal for mob is dead and start of the hunt
    one_mob(9.9, 'RG')