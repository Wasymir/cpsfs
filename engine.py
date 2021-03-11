import math
import os
import random
import threading
import time

import keyboard


class Engine():
    class Threads_manager():
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
        def __init__(self):
            self.blocked = False

        def register_hotkey(self, function,important=False):
            keyboard.add_hotkey((function.__name__).split('_')[0],self.key_function,args=[function,important], timeout=0.2)

        def key_function(self,function,important):
            if not self.blocked or important:
                function()

        def block_keyboard(self):
            self.blocked = True

        def un_block_keyboard(self):
            self.blocked = False





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
                self.velocity = [0,0,0]
                self.rotation = [0,0,0]
                self.stop_active = False
                self.thrust = 0
          
                # 
                self.rotation[2] = 0
                self.rotation[0] = 0
                self.velocity[2] = 0
                self.rotation[1] = 90


                self.velocity[1] = 0
                self.fuel = 500
                self.threading = thread_manager
                key_manager.register_hotkey(self.a_l_rotation)
                key_manager.register_hotkey(self.d_r_rotation)
                key_manager.register_hotkey(self.w_t_rotation)
                key_manager.register_hotkey(self.s_b_rotation)
                key_manager.register_hotkey(self.q_trust_up)
                key_manager.register_hotkey(self.e_trust_down)
                key_manager.register_hotkey(self.r_landing_engine_up)
                key_manager.register_hotkey(self.f_landing_engine_down)
                thread_manager.start_new_thread(self.calculate_current_velocity)
                key_manager.register_hotkey(self.x_emergency_trust_brake)
                key_manager.register_hotkey(self.z_thrust_max)
                key_manager.register_hotkey(self.c_thrust_min)
                thread_manager.start_new_thread(self.calculate_fuel)

            def valid_fuel(self):
                if self.fuel <= 0:
                    self.threading.stop_all()
                    keyboard.unhook_all()
                    os.system('cls')
                    print("No Fuel".center(os.get_terminal_size()[0]))
                    time.sleep(10)

            def calculate_fuel(self):
                self.fuel -= abs(self.thrust) / 300
                self.valid_fuel()
                time.sleep(0.1)

            def valid_angle(self, angle):
                if angle >= 360:
                    return self.valid_angle(angle - 360)
                elif angle < 0:
                    return self.valid_angle(angle + 360)
                else:
                    return angle

            def valid_trust(self, trust):
                if trust < -100:
                    return -100
                elif trust > 100:
                    return 100
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
                self.rotation[2] = self.valid_angle(self.rotation[2] - 2)
                if self.calculate_angle_factor(self.rotation[0]) != 0:
                    if self.calculate_angle_factor(self.rotation[1]) != 0:
                        self.rotation[0] = self.valid_angle(self.rotation[0] - 1)
                        self.rotation[1] = self.valid_angle(self.rotation[1] - 1)
                    else:
                        self.rotation[0] = self.valid_angle(self.rotation[0] - 2)
                else:
                    self.rotation[1] = self.valid_angle(self.rotation[1] - 2)

            def d_r_rotation(self):
                self.rotation[2] = self.valid_angle(self.rotation[2] + 2)
                if self.calculate_angle_factor(self.rotation[0]) != 0:
                    if self.calculate_angle_factor(self.rotation[1]) != 0:
                        self.rotation[0] = self.valid_angle(self.rotation[0] + 1)
                        self.rotation[1] = self.valid_angle(self.rotation[1] + 1)
                    else:
                        self.rotation[0] = self.valid_angle(self.rotation[0] + 2)
                else:
                    self.rotation[1] = self.valid_angle(self.rotation[1] + 2)

            def w_t_rotation(self):
                self.rotation[0] = self.valid_angle(self.rotation[0] + 2)
                if self.calculate_angle_factor(self.rotation[2]) != 0:
                    if self.calculate_angle_factor(self.rotation[1]) != 0:
                        self.rotation[2] = self.valid_angle(self.rotation[2] - 1)
                        self.rotation[1] = self.valid_angle(self.rotation[1] - 1)
                    else:
                        self.rotation[2] = self.valid_angle(self.rotation[2] - 2)
                else:
                    self.rotation[1] = self.valid_angle(self.rotation[1] - 2)

            def s_b_rotation(self):
                self.rotation[0] = self.valid_angle(self.rotation[0] - 2)
                if self.calculate_angle_factor(self.rotation[2]) != 0:
                    if self.calculate_angle_factor(self.rotation[1]) != 0:
                        self.rotation[2] = self.valid_angle(self.rotation[2] + 1)
                        self.rotation[1] = self.valid_angle(self.rotation[1] + 1)
                    else:
                        self.rotation[2] = self.valid_angle(self.rotation[2] + 2)
                else:
                    self.rotation[1] = self.valid_angle(self.rotation[1] + 2)

            def q_trust_up(self):
                self.thrust = self.valid_trust(self.thrust + 1)

            def e_trust_down(self):
                self.thrust = self.valid_trust(self.thrust - 1)

            def r_landing_engine_up(self):
                self.velocity[0] = self.valid_trust(self.velocity[0] + 0.2)
                self.fuel -= 0.2
                self.valid_fuel()

            def f_landing_engine_down(self):
                self.velocity[0] = self.valid_trust(self.velocity[0] - 0.2)
                self.fuel -= 0.2
                self.valid_fuel()

            def x_emergency_trust_brake(self):
                self.thrust = 0

            def z_thrust_max(self):
                self.thrust = 100

            def c_thrust_min(self):
                self.thrust = -100

            def calculate_velocity_delta(self):
                def calculate_delta(angle_factor, thrust):
                    return thrust * angle_factor / 900

                return {
                    'lr': calculate_delta(self.calculate_angle_factor(self.rotation[2]), self.thrust),
                    'tb': calculate_delta(self.calculate_angle_factor(self.rotation[0]), self.thrust),
                    'fb': calculate_delta(self.calculate_angle_factor(self.rotation[1]), self.thrust)
                }

            def validate_velocity(self, velocity):
                if velocity > 750:
                    return 750
                elif velocity < -750:
                    return - 750
                else:
                    return velocity

            def calculate_current_velocity(self):
                self.velocity[0] = self.validate_velocity(self.calculate_velocity_delta()['tb'] + self.velocity[0])
                self.velocity[2] = self.validate_velocity(self.calculate_velocity_delta()['lr'] + self.velocity[2])
                self.velocity[1] = self.validate_velocity(self.calculate_velocity_delta()['fb'] + self.velocity[1])
                time.sleep(0.1)

        class Position():
            def __init__(self, movement_engine, thread_manager, map):
                self.map = map
                self.movement_engine = movement_engine
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
                return {'z': self.movement_engine.velocity[0] / 10000,
                        'x': self.movement_engine.velocity[1] / 10000,
                        'y': self.movement_engine.velocity[2] / 10000, }

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
                    print("You've crashed".center(os.get_terminal_size()[0]))
                    time.sleep(10)
                time.sleep(0.1)

        class Auto_pilot():
            class Land_Takeoff():
                def __init__(self, movement, position, thread_manager, key_manager, map):
                    self.key_manager = key_manager
                    self.landed = True
                    self.movement = movement
                    self.position = position
                    self.map = map
                    self.status = 3
                    thread_manager.start_new_thread(self.refresh_landing_contidions)
                    thread_manager.start_new_thread(self.refresh_keyboard)
                    key_manager.register_hotkey(self.l_land)
                    key_manager.register_hotkey(self.t_takeoff,important=True)

                def refresh_keyboard(self):
                    if self.status == 2 or self.status == 3:
                        self.key_manager.block_keyboard()
                    else:
                        self.key_manager.un_block_keyboard()
                    time.sleep(0.1)

                def refresh_landing_contidions(self):
                    if all([
                                all(velocity <= 0.2 for velocity in self.movement.velocity),
                                self.position.detailed_coordinates[0] - self.map.map.terrain[self.position.simplified_coordinates[1]][self.position.simplified_coordinates[2]] <= 0.5,
                                self.position.detailed_coordinates[0] - self.map.map.terrain[self.position.simplified_coordinates[1]][self.position.simplified_coordinates[2]] >= 0.05,
                                self.movement.thrust == 0,
                                self.status <= 1

                           ]):
                        self.status = 1
                    elif self.status <= 1:
                        self.status = 0

                    time.sleep(0.1)

                def l_land(self):
                    def remove_rotation(rotation):
                        for index,value in enumerate(rotation[:1]):
                            while rotation[index] != 0:
                                if rotation[index] > 0:
                                    rotation[index] -= 1
                                elif rotation[index] < 0:
                                    rotation[index] += 1
                                time.sleep(0.1)

                    def landing_procedure(movement,position,map):
                        def landing_controller(position,map):
                            if round(position.detailed_coordinates[0] - map.map.terrain[position.simplified_coordinates[1]][position.simplified_coordinates[2]],3) == 0:
                                return False
                            else:
                                return True

                        movement.fuel -= 2
                        movement.valid_fuel()
                        while landing_controller(position,map):
                            movement.velocity = [-4,0,0]
                            time.sleep(0.05)
                        movement.velocity = [0, 0, 0]

                    self.status = 2
                    self.movement.velocity = [0,0,0]
                    remove_rotation(self.movement.rotation)
                    landing_procedure(self.movement,self.position,self.map)
                    self.status = 3

                def t_takeoff(self):
                    if self.status == 3:
                        self.status = 2
                        self.movement.fuel -= 2
                        self.movement.valid_fuel()
                        while self.position.detailed_coordinates[0] - self.map.map.terrain[self.position.simplified_coordinates[1]][self.position.simplified_coordinates[2]] < 0.05:
                            self.movement.velocity = [5,0,0]
                            time.sleep(0.01)
                        self.movement.velocity = [0,0,0]
                        self.status = 0













            def __init__(self, movement, position, thread_manager, key_manager, map):
                self.land_takeoff = self.Land_Takeoff(movement, position, thread_manager, key_manager, map)
        def __init__(self, map, key_manager, thread_manager):
            self.movement = self.Movement(key_manager, thread_manager)
            self.position = self.Position(self.movement, thread_manager, map)
            self.collision = self.Collision(thread_manager, map, self.position)
            self.auto_pilot = self.Auto_pilot(self.movement,self.position,thread_manager,key_manager,map)




    def __init__(self, map_width, map_length, map_height):
        self.map = self.Game_Map(map_height, map_length, map_width)
        self.threads_manager = self.Threads_manager()
        self.key_manager = self.Key_manager()
        self.player = self.Space_Ship(self.map, self.key_manager, self.threads_manager)

