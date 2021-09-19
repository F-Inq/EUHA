import time
import keyboard
import winsound
import random

eu_log = open('C:\\Users\\Flak\\Documents\\Entropia Universe\\chat.log')
startup_time = time.time()

while time.time() < startup_time + 3:  # Delay to skip the old logs
    try:
        eu_log.readline()
    except UnicodeDecodeError:
        pass
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nReady')


def one_mob(hp, gun):
    global same_mob
    while same_mob:
        try:
            line = eu_log.readline()  # read a log
        except UnicodeDecodeError:  # don't care if it's a message
            line = ''
        if '[System] []' in line and 'You inflicted' in line:  # check if damage dealt
            dmg = float(line.split()[-4])  # extract damage size
            if dmg > 12.9:
                if gun != 'LP-10':  # check if LP-10
                    hp = hp + 40  # if LP-10, then mob is big
                    gun = 'LP-10'
                else:
                    gun = 'LP-10'
            hp = round(hp - dmg, 1)  # substract hp from mob
            if gun == 'LP-10' and 0 < hp < 27:
                if 3 < hp < 27:
                    gun = 'RG'
                    time.sleep(round(random.uniform(0, 0.6), 3))
                    keyboard.press_and_release('3')
                elif 0 < hp < 3.1:
                    gun = 'SA'
                    time.sleep(round(random.uniform(0, 0.6), 3))
                    keyboard.press_and_release('2')
            elif gun == 'RG' and 0 < hp < 3.1:
                gun = 'SA'
                time.sleep(round(random.uniform(0, 0.5), 3))
                keyboard.press_and_release('2')
            if hp <= 0:  # if mob is dead, start over
                same_mob = False
                if gun != 'RG':
                    time.sleep(round(random.uniform(0.1, 0.6), 3))
                    keyboard.press_and_release('3')
                    gun = 'RG'
            else:  # if mob is not dead, continue with same hp and gun
                one_mob(hp, gun)
        elif keyboard.is_pressed('`'):  # something went wrong, reset
            print('-')
            time.sleep(1)
            same_mob = False
        else:
            continue  # read next log
    else:
        return


while True:
    same_mob = True
    winsound.PlaySound('*', winsound.SND_ALIAS)
    one_mob(9.9, 'RG')
