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
                    self.generate_terrain(max_terrain_height, max_terrain_height // 2)

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
                    self.detailed_coordinates = [
                        self.map.map.terrain[self.map.map.map_x_width // 2][self.map.map.map_y_width // 2],
                        self.map.map.map_x_width // 2, self.map.map.map_y_width // 2]
                    self.simplified_coordinates = [
                        self.map.map.terrain[self.map.map.map_x_width // 2][self.map.map.map_y_width // 2],
                        self.map.map.map_x_width // 2, self.map.map.map_y_width // 2]
                    thread_manager.start_new_thread(self.calculate_current_coordinates)
                    thread_manager.start_new_thread(self.refresh_simplified_coordinates)

                def refresh_simplified_coordinates(self):
                    for x in range(0, 3):
                        self.simplified_coordinates[x] = math.floor(self.detailed_coordinates[x])
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
                        time.sleep(10)
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

    class Cli_graphic():
        class Game_view():
            class Cli_element():
                def __init__(self):
                    self.content = []
                    self.width = 0
                    self.height = 0

                # <section_name> = [{<id>:<value>,<cells>},... <rows>]
                def generate_elememn_as_column(self, **kwargs):
                    def calculate_column_cell_width(**kwargs):
                        cell_width = max(max(max( (len(str(key)) + len(str(value)) + 5) for key,value in row.items()) for row in content) for section_name,content in kwargs.items())
                        row_width = max(cell_width * max(max( len(row) for row in content) for section_name,content in kwargs.items()), max(len(str(section_name)) + 1 for section_name, content in kwargs.items()))
                        return row_width,cell_width

                    self.width, cell_width = calculate_column_cell_width(**kwargs)
                    for section_name, content in kwargs.items():    
                        self.content.append(('=%s' % section_name).ljust(self.width - 1,'='))
                        for row in content:
                            self.content.append('')
                            for key,value in row.items():
                                self.content[-1] += ('%s: ' % key) + ('%s | ' % value).rjust(cell_width - len(key) - 2)
                        self.content = [line.ljust(self.width) for line in self.content]
                    self.height = len(self.content)

                # <y_id> = [<cells values>]
                def generate_element_as_map(self, name, x_indexes, **kwargs):
                    def calculate_column_cell_y_index_width(name, x_indexes, **kwargs):
                        cell_width = max(
                            max(len(x_index) for x_index in x_indexes),
                            max(max(len(str(value)) for value in content) for key, content in kwargs.items())
                        ) + 1
                        y_index_width = max(len(str(key)) for key, value in kwargs.items()) + 3
                        column_width = max(y_index_width + (cell_width * len(x_indexes)), (len(name) + 1))
                        return column_width, cell_width, y_index_width

                    self.width, cell_width, y_index_width = calculate_column_cell_y_index_width(name, x_indexes,
                                                                                                **kwargs)
                    self.content.append('')
                    self.content[-1] += ('=%s' % name).ljust(self.width, '=')
                    self.content.append('')
                    self.content[-1] += (y_index_width) * ' '
                    for x_index in x_indexes:
                        self.content[-1] += (' %s ' % x_index).rjust(cell_width)
                    self.content[-1] = self.content[-1].ljust(self.width)
                    self.content.append('-' * self.width)
                    for key, content in kwargs.items():
                        self.content.append('')
                        self.content[-1] += ('%s | ' % key).rjust(y_index_width)
                        for value in content:
                            self.content[-1] += ('%s ' % value).rjust(cell_width)
                        self.content[-1] = self.content[-1].ljust(self.width)
                    self.height = len(self.content)

            def __init__(self, engine):
                self.position = engine.player.position
                self.movement = engine.player.movement
                self.map = engine.map
                self.data_table = self.Cli_element()
                self.data_map_terrain = self.Cli_element()

            def render_data_table(self):
                def calculate_relative_height(position, map):
                    if position.in_map():
                        return '%.3f' % round(
                            position.detailed_coordinates[0] - map.map.terrain[position.simplified_coordinates[1]][
                                position.simplified_coordinates[2]] + 1, 3)
                    else:
                        return '???'
                self.data_table.content = []
                self.data_table.generate_elememn_as_column(
                    S_Position=[
                        {'z': self.position.simplified_coordinates[0],
                         'x': self.position.simplified_coordinates[1],
                         'y': self.position.simplified_coordinates[2]}
                    ],
                    D_Position=[
                        {'z': "%.3f" % round(self.position.detailed_coordinates[0], 3),
                         'x': "%.3f" % round(self.position.detailed_coordinates[1], 3),
                         'y': "%.3f" % round(self.position.detailed_coordinates[2], 3)},
                        {'R.H.': calculate_relative_height(self.position, self.map)}
                    ],
                    Rotation=[
                        {'z': self.position.movement_engine.lr_rotation,
                         'x': self.position.movement_engine.tb_rotation}
                    ],
                    Velocity=[
                        {'z': "%.1f" % round(self.position.movement_engine.tb_velocity, 1),
                         'x': "%.1f" % round(self.position.movement_engine.fb_velocity, 1),
                         'y': "%.1f" % round(self.position.movement_engine.lr_velocity, 1)},
                        {'tr': self.position.movement_engine.thrust}
                    ]
                )

            def render_terrain_map(self):
                def render_y_index(y):
                    if self.map.check_position_coordinates[0][0][y]:
                        return y
                    else:
                        return '#'
                def render_x_index(x):
                    if self.map.check_position_coordinates[0][x][0]:
                        return x
                    else:
                        return '#'


                self.data_map_terrain.generate_element_as_map(
                    name= 'Terrain_Height_Map',
                    x_indexes= [render_x_index(index) for index in ]

                )




            def test_print(self):
                self.render_data_table()
                os.system('cls')
                for line in self.data_table.content:
                    print(line)
                time.sleep(0.1)

        def __init__(self, engine):
            self.game_view = self.Game_view(engine)

    def __init__(self):
        self.engine = self.Engime(10, 10, 50)
        self.engine.key_manager.register_hotkey(self.g_exit)
        self.cli_test_graphic = self.Cli_graphic(self.engine)
        self.engine.threads_menager.start_new_thread(self.cli_test_graphic.game_view.test_print)

    def g_exit(self):
        pass
        # self.engine.threads_menager.stop_all()
        # keyboard.unhook_all()


os.system('cls')
elo = Command_Line_Python_Space_Simulator()
