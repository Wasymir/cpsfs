import time
import os
import threading
import keyboard
import random
import math


class Command_Line_Python_Space_Simulator():
    class Engime():
        class Threads_menager():
            class Thread():
                def __init__(self, function):
                    self.running = True
                    self.thread = threading.Thread(target=self.thread_function, args=(function,)).start()

                def thread_function(self, function):
                    while self.running:
                        function()

                def stop_thread(self):
                    self.running = False

            def __init__(self):
                self.threads = []

            def start_new_thread(self, function):
                self.threads.append(self.Thread(function))

            def stop_all(self):
                for thread in self.threads:
                    thread.stop_thread()

        class Key_manager():
            def register_hotkey(self, function):
                keyboard.add_hotkey(function.__name__[0], function, timeout=0.2)

            def unhook_all(self):
                keyboard.unhook_all()

        class Game_Map():
            class Map():
                def __init__(self, z_height, x_width, y_width, max_terrain_height):
                    self.map = []
                    for z in range(z_height):
                        self.map.append([])
                        for x in range(x_width):
                            self.map[-1].append([])
                            for y in range(y_width):
                                self.map[-1][-1].append(False)
                    self.map_y_width = y_width
                    self.map_x_width = x_width
                    self.map_z_height = z_height
                    self.generate_terrain(max_terrain_height, max_terrain_height//2)

                def check_position_coordinates(self, z, x, y):
                    if z < 0 or x < 0 or y < 0:
                        return False
                    try:
                        test = self.map[z][x][y]
                    except IndexError:
                        return False
                    return True

                def generate_terrain(self, max_terrain_height, step):
                    def get_adjacent_cells_height_average(x_index, y_index):
                        values = []
                        for x in range(x_index - 1, x_index + 1):
                            for y in range(y_index - 1, y_index + 1):
                                if self.check_position_coordinates(0, y, x):
                                    values.append(self.terrain[x][y])
                        return sum(values) // len(values)

                    def generate_terrain_height(avr_value, max_terrain_height, step):
                        terrain_height = random.randint(avr_value - step, avr_value + step)
                        if terrain_height <= 0:
                            return 1
                        elif terrain_height > max_terrain_height:
                            return max_terrain_height

                        return terrain_height

                    def render_terrain_to_map(terrain, map, x_width, y_width):
                        for x_index in range(x_width):
                            for y_index in range(y_width):
                                for height in range(terrain[x_index][y_index]):
                                    map[height][x_index][y_index] = True

                    # create
                    self.terrain = []
                    for x in range(self.map_x_width):
                        self.terrain.append([])
                        for y in range(self.map_y_width):
                            self.terrain[-1].append(1)
                    # generate
                    for x_index in range(len(self.terrain)):
                        for y_index in range(len(self.terrain[x_index])):
                            self.terrain[x_index][y_index] = generate_terrain_height(
                                get_adjacent_cells_height_average(x_index, y_index), max_terrain_height, step)
                    # render
                    render_terrain_to_map(self.terrain, self.map, self.map_x_width, self.map_y_width)

            def __init__(self, map_z, map_x, map_y):
                self.map = self.Map(map_z, map_x, map_y, map_z // 2)

            def is_not_space(self, z, x, y):

                return self.map.map[z][x][y]

            def check_position_coordinates(self, z, x, y):
                return self.map.check_position_coordinates(z, x, y)

        class Space_Ship():
            class Movement():
                def __init__(self, key_manager, thread_manager):
                    self.stop_active = False
                    self.reverse_thrust = False
                    self.thrust = 0
                    self.lr_rotation = 0
                    self.tb_rotation = 0
                    self.lr_velocity = 0
                    self.fb_rotation = 90
                    self.tb_velocity = 0
                    self.fb_velocity = 0
                    key_manager.register_hotkey(self.a_l_rotation)
                    key_manager.register_hotkey(self.d_r_rotation)
                    key_manager.register_hotkey(self.w_t_rotation)
                    key_manager.register_hotkey(self.s_b_rotation)

                    key_manager.register_hotkey(self.q_trust_up)
                    key_manager.register_hotkey(self.e_trust_down)
                    key_manager.register_hotkey(self.r_landing_engine_up)
                    key_manager.register_hotkey(self.f_landing_engine_down)
                    thread_manager.start_new_thread(self.calculate_current_vectolity)
                    # thread_manager.start_new_thread(self.stop)
                    key_manager.register_hotkey(self.z_reverse_trust)
                    # key_manager.register_hotkey(self.x_stop_ship)

                def valid_angle(self, angle):
                    if angle >= 360:
                        return self.valid_angle(angle - 360)
                    elif angle < 0:
                        return self.valid_angle(angle + 360)
                    else:
                        return angle

                def valid_trust(self, trust):
                    if self.reverse_thrust:
                        if trust < -100:
                            return -100
                        elif trust > 0:
                            return 0
                        else:
                            return trust
                    else:
                        if trust > 100:
                            return 100
                        elif trust < 0:
                            return 0
                        else:
                            return trust

                def calculate_angle_factor(self, angle):
                    if angle < 90:
                        return angle
                    elif angle < 180:
                        return 180 - angle
                    elif angle == 180:
                        return 0
                    elif angle < 270:
                        return (angle - 180) * -1
                    else:
                        return (360 - angle) * -1

                def a_l_rotation(self):
                    self.lr_rotation = self.valid_angle(self.lr_rotation - 2)
                    if self.calculate_angle_factor(self.tb_rotation) != 0:
                        if self.calculate_angle_factor(self.fb_rotation) != 0:
                            self.tb_rotation = self.valid_angle(self.tb_rotation - 1)
                            self.fb_rotation = self.valid_angle(self.fb_rotation - 1)
                        else:
                            self.tb_rotation = self.valid_angle(self.tb_rotation - 2)
                    else:
                        self.fb_rotation = self.valid_angle(self.fb_rotation - 2)

                def d_r_rotation(self):
                    self.lr_rotation = self.valid_angle(self.lr_rotation + 2)
                    if self.calculate_angle_factor(self.tb_rotation) != 0:
                        if self.calculate_angle_factor(self.fb_rotation) != 0:
                            self.tb_rotation = self.valid_angle(self.tb_rotation + 1)
                            self.fb_rotation = self.valid_angle(self.fb_rotation + 1)
                        else:
                            self.tb_rotation = self.valid_angle(self.tb_rotation + 2)
                    else:
                        self.fb_rotation = self.valid_angle(self.fb_rotation + 2)

                def w_t_rotation(self):
                    self.tb_rotation = self.valid_angle(self.tb_rotation + 2)
                    if self.calculate_angle_factor(self.lr_rotation) != 0:
                        if self.calculate_angle_factor(self.fb_rotation) != 0:
                            self.lr_rotation = self.valid_angle(self.lr_rotation - 1)
                            self.fb_rotation = self.valid_angle(self.fb_rotation - 1)
                        else:
                            self.lr_rotation = self.valid_angle(self.lr_rotation - 2)
                    else:
                        self.fb_rotation = self.valid_angle(self.fb_rotation - 2)

                def s_b_rotation(self):
                    self.tb_rotation = self.valid_angle(self.tb_rotation - 2)
                    if self.calculate_angle_factor(self.lr_rotation) != 0:
                        if self.calculate_angle_factor(self.fb_rotation) != 0:
                            self.lr_rotation = self.valid_angle(self.lr_rotation + 1)
                            self.fb_rotation = self.valid_angle(self.fb_rotation + 1)
                        else:
                            self.lr_rotation = self.valid_angle(self.lr_rotation + 2)
                    else:
                        self.fb_rotation = self.valid_angle(self.fb_rotation + 2)

                def q_trust_up(self):
                    self.thrust = self.valid_trust(self.thrust + 1)
                    # time.sleep(0.2)

                def e_trust_down(self):
                    self.thrust = self.valid_trust(self.thrust - 1)
                    # time.sleep(0.2)

                def r_landing_engine_up(self):
                    self.tb_velocity = self.valid_trust(self.tb_velocity + 0.2)
                    # time.sleep(0.2)

                def f_landing_engine_down(self):
                    self.tb_velocity = self.valid_trust(self.tb_velocity - 0.2)
                    # time.sleep(0.2)

                def z_reverse_trust(self):
                    self.thrust = 0
                    self.reverse_thrust = not self.reverse_thrust

                def calculate_velocity_delta(self):
                    def calculate_delta(angle_factor, thrust):
                        return thrust * angle_factor / 900

                    return {
                        'lr': calculate_delta(self.calculate_angle_factor(self.lr_rotation), self.thrust),
                        'tb': calculate_delta(self.calculate_angle_factor(self.tb_rotation), self.thrust),
                        'fb': calculate_delta(self.calculate_angle_factor(self.fb_rotation), self.thrust)
                    }

                def validate_vectolity(self, vectolity):
                    if vectolity > 750:
                        return 750
                    elif vectolity < -750:
                        return - 750
                    else:
                        return vectolity

                def calculate_current_vectolity(self):
                    self.tb_velocity = self.validate_vectolity(self.calculate_velocity_delta()['tb'] + self.tb_velocity)
                    self.lr_velocity = self.validate_vectolity(self.calculate_velocity_delta()['lr'] + self.lr_velocity)
                    self.fb_velocity = self.validate_vectolity(self.calculate_velocity_delta()['fb'] + self.fb_velocity)
                    time.sleep(0.1)

            class Position():
                def __init__(self, movement_engine, thread_manager, map):
                    self.map = map
                    self.movement_engine = movement_engine
                    # todo: tu zmiń po testach
                    self.detailed_coordinates = [self.map.map.terrain[self.map.map.map_x_width // 2][ self.map.map.map_y_width // 2],self.map.map.map_x_width // 2, self.map.map.map_y_width // 2]
                    self.simplified_coordinates = [self.map.map.terrain[self.map.map.map_x_width // 2][ self.map.map.map_y_width // 2],self.map.map.map_x_width // 2, self.map.map.map_y_width // 2]
                    thread_manager.start_new_thread(self.calculate_current_coordinates)
                    thread_manager.start_new_thread(self.refresh_simplified_coordinates)

                def refresh_simplified_coordinates(self):
                    for x in range(0, 3):
                        self.simplified_coordinates[x] = math.ceil(self.detailed_coordinates[x])
                    time.sleep(0.1)

                def calculate_coordinates_delta(self):
                    return {'z': self.movement_engine.tb_velocity / 10000,
                            'x': self.movement_engine.fb_velocity / 10000,
                            'y': self.movement_engine.lr_velocity / 10000, }

                def calculate_current_coordinates(self):
                    self.detailed_coordinates[0] = self.detailed_coordinates[0] + self.calculate_coordinates_delta()[
                        'z']
                    self.detailed_coordinates[1] = self.detailed_coordinates[1] + self.calculate_coordinates_delta()[
                        'x']
                    self.detailed_coordinates[2] = self.detailed_coordinates[2] + self.calculate_coordinates_delta()[
                        'y']
                    time.sleep(0.1)

                def in_map(self):
                    if any(n < 0 for n in self.detailed_coordinates):
                        return False
                    else:
                        return self.map.map.check_position_coordinates(self.simplified_coordinates[0],
                                                                       self.simplified_coordinates[1],
                                                                       self.simplified_coordinates[2])

            class Collision():
                def __init__(self, threading_manager, map, position):
                    self.threading = threading_manager
                    self.map = map
                    self.position = position
                    self.threading.start_new_thread(self.test_collision)

                def check_collision(self):
                    if self.map.check_position_coordinates(
                            self.position.simplified_coordinates[0], self.position.simplified_coordinates[1],
                            self.position.simplified_coordinates[2]):
                        return self.map.is_not_space(
                            self.position.simplified_coordinates[0], self.position.simplified_coordinates[1],
                            self.position.simplified_coordinates[2])
                    else:
                        return False

                def test_collision(self):
                    if self.check_collision():
                        self.threading.stop_all()
                        keyboard.unhook_all()
                        os.system('cls')
                        print("You've crashed")
                        time.sleep(6)
                    time.sleep(0.1)

            def __init__(self, map, key_manager, thread_manager):
                self.movement = self.Movement(key_manager, thread_manager)
                self.position = self.Position(self.movement, thread_manager, map)
                self.collision = self.Collision(thread_manager, map, self.position)

        def __init__(self, map_width, map_lenght, map_height):
            self.map = self.Game_Map(map_height, map_lenght, map_width)
            self.threads_menager = self.Threads_menager()
            self.key_manager = self.Key_manager()
            self.player = self.Space_Ship(self.map, self.key_manager, self.threads_menager)

    class Cli_test_graphic():
        def __init__(self, engine):
            self.engine = engine
            self.engine.threads_menager.start_new_thread(self.print_screen)

        def print_screen(self):
            os.system('cls')
            print('-_-_-Position detailed-_-_-')
            print('z: %9s  | ' % str(round(self.engine.player.position.detailed_coordinates[0], 3)), end='')
            print('x: %9s  | ' % str(round(self.engine.player.position.detailed_coordinates[1], 3)), end='')
            print('y: %9s  | ' % str(round(self.engine.player.position.detailed_coordinates[2], 3)))
            print('-_-_-Position simplyfied-_-_-')
            print('z: %9s  | ' % str(round(self.engine.player.position.simplified_coordinates[0], 3)), end='')
            print('x: %9s  | ' % str(round(self.engine.player.position.simplified_coordinates[1], 3)), end='')
            print('y: %9s  | ' % str(round(self.engine.player.position.simplified_coordinates[2], 3)))
            print('relative height: ', end='')
            if self.engine.player.position.in_map():
                print('%11s  |' % str(round((self.engine.player.position.detailed_coordinates[0] - self.engine.map.map.terrain[
                    self.engine.player.position.simplified_coordinates[1]][
                    self.engine.player.position.simplified_coordinates[2]] + 1), 3)))
            else:
                print('unavailable  |')
            print('-_-_-Rotation-_-_-')
            print('rot z: %5s  | ' % str(round(self.engine.player.movement.lr_rotation, 3)), end='')
            # print('rot fb: ' + str(round(self.engine.player.movement.fb_rotation, 3)) + '  |  ', end='')
            print('rot y: %5s  | ' % str(round(self.engine.player.movement.tb_rotation, 3)))
            print('-_-_-speed-_-_-')
            print('x: %9s  | ' % str(round(self.engine.player.movement.fb_velocity, 3)), end='')
            print('z: %9s  | ' % str(round(self.engine.player.movement.tb_velocity, 3)), end='')
            print('y: %9s  | ' % str(round(self.engine.player.movement.lr_velocity, 3)))
            print('-_-_-thrust-_-_-')
            print('tr: ' + str(round(self.engine.player.movement.thrust, 3)) + '  |  ')
            print('-_-_-map-_-_-')
            print(self.generte_minimap())
            print('\n')

            time.sleep(0.1)
        def generte_minimap(self):
            self.minimap = '       '
            for column in range(self.engine.player.position.simplified_coordinates[1] - 4,self.engine.player.position.simplified_coordinates[1] + 5):
                if column == self.engine.player.position.simplified_coordinates[1]:
                    self.minimap += '%4s' % ('_' * len(str(self.engine.player.position.simplified_coordinates[1])))
                else:
                    self.minimap += '%4s' % ' '
            self.minimap += '\n'
            self.minimap += ''' |x > |'''
            for column in range(self.engine.player.position.simplified_coordinates[1] - 4,self.engine.player.position.simplified_coordinates[1] + 5):
                if self.engine.map.check_position_coordinates(0,column,0):
                    self.minimap += '%4s' % column
                else:
                    self.minimap += '%4s' % '#'
            self.minimap += '\n'
            self.minimap += ' |y \/|'
            for column in range(self.engine.player.position.simplified_coordinates[1] - 4,self.engine.player.position.simplified_coordinates[1] + 5):
                self.minimap += '-' * 4
            self.minimap += '\n'
            for row in range(self.engine.player.position.simplified_coordinates[2] - 4,self.engine.player.position.simplified_coordinates[2] + 5):
                if row == self.engine.player.position.simplified_coordinates[2]:
                    self.minimap += '|'
                else:
                    self.minimap += ' '

                if self.engine.map.check_position_coordinates(0,0,row):
                    self.minimap += '|%4s|' % row
                else:
                    self.minimap += '|%4s|' % '#'
                for column in range(self.engine.player.position.simplified_coordinates[1] - 4,self.engine.player.position.simplified_coordinates[1] + 5):
                    if self.engine.map.check_position_coordinates(0,column,row):
                        self.minimap += '%4s' % (self.engine.map.map.terrain[row][column] - 1)
                    else:
                        self.minimap += '%4s' % '?'


                self.minimap += '\n\n'






            return self.minimap


    def __init__(self):
        self.engine = self.Engime(100, 100, 50)
        self.cli_test_graphic = self.Cli_test_graphic(self.engine)
        self.engine.key_manager.register_hotkey(self.g_exit)

    def g_exit(self):
        self.engine.threads_menager.stop_all()
        keyboard.unhook_all()

os.system('cls')
elo = Command_Line_Python_Space_Simulator()
