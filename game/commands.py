from engine import utils
import math


def quit():
    utils.quit()


def player_main_engine_on(player):
    player.set_thruster('main', True)


def player_main_engine_off(player):
    player.set_thruster('main', False)


def player_retro_engine_on(player):
    player.set_thruster('retro', True)


def player_retro_engine_off(player):
    player.set_thruster('retro', False)


def player_left_engine_on(player):
    player.set_thruster('left', True)


def player_left_engine_off(player):
    player.set_thruster('left', False)


def player_right_engine_on(player):
    player.set_thruster('right', True)


def player_right_engine_off(player):
    player.set_thruster('right', False)


def set_player_heading_from_mouse(event, window, player):
    #convert to be centered around a 0,0 in the middle
    x = event.pos[0] - window.rect.centerx
    y = event.pos[1] - window.rect.centery
    
    theta_rad = math.atan2(y, x)
    degrees = math.degrees(theta_rad)

    if degrees >= 0:
        heading = degrees + 90
    elif degrees < -90:
        heading = 360 - abs(degrees) + 90
    else:
        heading = 90 - abs(degrees)

    if heading == 360:
        heading = 0
    
    heading = round(heading)

    player.order_heading(heading)


def zoom_map_in(event, window, amount):
    set_map_center_from_mouse_click(event, window, unlock_if_locked=False)
    window.zoom_in(amount)


def zoom_map_out(event, window, amount):
    set_map_center_from_mouse_click(event, window, unlock_if_locked=False)
    window.zoom_out(amount)


def set_map_center_from_mouse_click(event, window, unlock_if_locked=True):
    if unlock_if_locked:
        #TODO: review if this error handling is ok
        #this catches a value error when the view is not locked to an object
        try:
            window.unlock_center()
        except ValueError:
            pass

    window.center = window.convert_screen_to_world(event.pos)
