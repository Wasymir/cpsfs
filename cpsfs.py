import os
import time

import keyboard


class Console_Python_Space_Flight_Simulator():
    class Cli_graphic():
        class Game_view():

            def __init__(self, engine):
                from graphic import Blinking_light, Cli_element
                self.blink_light = Blinking_light(engine.threads_manager)
                self.blink_light_faster = Blinking_light(engine.threads_manager,frequency=0.1)
                self.position = engine.player.position
                self.movement = engine.player.movement
                self.map = engine.map
                self.auto_pilot = engine.player.auto_pilot
                self.data_table = Cli_element()
                self.data_map_terrain = Cli_element()
                self.graphic_2d_map_x = Cli_element()
                self.graphic_2d_map_y = Cli_element()
                self.message = Cli_element()
                self.screen = Cli_element()

            def render_data_table(self):
                def calculate_relative_height(position, map):
                    if position.in_map():
                        return '%.3f' % round(
                            position.detailed_coordinates[0] - map.map.terrain[position.simplified_coordinates[1]][
                                position.simplified_coordinates[2]], 3)
                    else:
                        return '???'

                def render_relative_height_warning(position, map, blink_light):
                    if position.in_map():
                        if position.detailed_coordinates[0] - map.map.terrain[position.simplified_coordinates[1]][
                            position.simplified_coordinates[2]] < 1:
                            return blink_light.render()
                        else:
                            return '   '
                    else:
                        return '   '

                def render_fuel_level_warning(movement, blink_light):
                    if movement.fuel < 50:
                        return blink_light.render()
                    else:
                        return '   '

                def render_landing_conditions(landing, blink_light,blinking_light_faster):
                    if landing.status == 3:
                        return '###'
                    elif landing.status == 2:
                        return blinking_light_faster.render()
                    elif landing.status == 1:
                        return blink_light.render()
                    elif landing.status == 0:
                        return '   '



                self.data_table.content.clear()
                self.data_table.generate_element_as_column(
                    S_Position=[
                        {'z': self.position.simplified_coordinates[0],
                         'x': self.position.simplified_coordinates[1],
                         'y': self.position.simplified_coordinates[2]}
                    ],
                    D_Position=[
                        {'z': "%.3f" % round(self.position.detailed_coordinates[0], 3),
                         'x': "%.3f" % round(self.position.detailed_coordinates[1], 3),
                         'y': "%.3f" % round(self.position.detailed_coordinates[2], 3)},
                        {'rh': calculate_relative_height(self.position, self.map),
                         'R.H.W': render_relative_height_warning(self.position, self.map, self.blink_light)}
                    ],
                    Rotation=[
                        {'z': self.position.movement_engine.rotation[2],
                         'x': self.position.movement_engine.rotation[0]}
                    ],
                    Velocity=[
                        {'z': "%.1f" % round(self.position.movement_engine.velocity[0], 1),
                         'x': "%.1f" % round(self.position.movement_engine.velocity[1], 1),
                         'y': "%.1f" % round(self.position.movement_engine.velocity[2], 1)},
                        {'tr': self.position.movement_engine.thrust}
                    ],
                    Fuel=[
                        {'fl': '%.2f' % round(self.movement.fuel, 2),
                         'F.L.W': render_fuel_level_warning(self.movement, self.blink_light)}
                    ],
                    Landing=[
                        {'L.A':render_landing_conditions(self.auto_pilot.land_takeoff,self.blink_light,self.blink_light_faster),'s':self.auto_pilot.land_takeoff.status}
                    ],
                )

            def render_terrain_map(self):
                self.data_map_terrain.content.clear()

                def render_y_index(y, map):
                    if map.check_position_coordinates(0, 0, y):
                        return str(y)
                    else:
                        return '?'

                def render_x_index(x, map):
                    if map.check_position_coordinates(0, x, 0):
                        return str(x)
                    else:
                        return '?'

                def render_height(z, x, y, map, position, blink_light):
                    if position.simplified_coordinates[1:] == [x, y]:
                        return '@'
                    if render_x_index(x, map) != '?' and render_y_index(y, map) != '?':
                        if map.map.terrain[x][y] - 1 > z:
                            if blink_light.on:
                                return '!'.rjust(len(str(map.map.terrain[x][y] - 1)))
                            else:
                                return map.map.terrain[x][y] - 1
                        return map.map.terrain[x][y] - 1
                    else:
                        return '#'

                self.data_map_terrain.generate_element_as_map(
                    name='Terrain_Height_Map',
                    x_indexes=[render_x_index(index, self.map) for index in
                               range(self.position.simplified_coordinates[1] - 4,
                                     self.position.simplified_coordinates[1] + 5)],
                    **{render_y_index(y_index, self.map): [
                        render_height(self.position.simplified_coordinates[0], x_index, y_index, self.map,
                                      self.position, self.blink_light)
                        for x_index in
                        range(self.position.simplified_coordinates[1] - 4,
                              self.position.simplified_coordinates[1] + 5)]
                        for y_index in
                        range(self.position.simplified_coordinates[2] - 4,
                              self.position.simplified_coordinates[2] + 5)})

            def render_graphic_2d_map_x(self):
                self.graphic_2d_map_x.content.clear()

                def render_z_index(z, map):
                    if map.check_position_coordinates(z, 0, 0):
                        return str(z)
                    else:
                        return '?'

                def render_x_index(x, map):
                    if map.check_position_coordinates(0, x, 0):
                        return str(x)
                    else:
                        return '?'

                def render_y_index(y, map):
                    if map.check_position_coordinates(0, 0, y):
                        return str(y)
                    else:
                        return '?'

                def render_cell(z, x, y, map, position):
                    if position.simplified_coordinates == [z, x, y]:
                        return '@'
                    elif all(result != '?' for result in (render_y_index(y, map),
                                                          render_x_index(x, map),
                                                          render_z_index(z, map))):
                        if map.is_not_space(z, x, y):
                            return 'X'
                        else:
                            return '*'

                    else:
                        return '#'

                self.graphic_2d_map_x.generate_element_as_map(
                    name='X_axis_AGSS',
                    x_indexes=[render_x_index(index, self.map) for index in
                               range(self.position.simplified_coordinates[1] - 4,
                                     self.position.simplified_coordinates[1] + 5)],
                    **{render_z_index(z_index, self.map): [
                        render_cell(z_index, x_index, self.position.simplified_coordinates[2], self.map, self.position)
                        for x_index in
                        range(self.position.simplified_coordinates[1] - 4, self.position.simplified_coordinates[1] + 5)]
                        for z_index in
                        range(self.position.simplified_coordinates[0] + 2, self.position.simplified_coordinates[0] - 3,
                              -1)}
                )

            def render_graphic_2d_map_y(self):
                self.graphic_2d_map_y.content.clear()

                def render_z_index(z, map):
                    if map.check_position_coordinates(z, 0, 0):
                        return str(z)
                    else:
                        return '?'

                def render_x_index(x, map):
                    if map.check_position_coordinates(0, x, 0):
                        return str(x)
                    else:
                        return '?'

                def render_y_index(y, map):
                    if map.check_position_coordinates(0, 0, y):
                        return str(y)
                    else:
                        return '?'

                def render_cell(z, x, y, map, position):
                    if position.simplified_coordinates == [z, x, y]:
                        return '@'
                    elif all(result != '?' for result in (render_y_index(y, map),
                                                          render_x_index(x, map),
                                                          render_z_index(z, map))):
                        if map.is_not_space(z, x, y):
                            return 'X'
                        else:
                            return '*'

                    else:
                        return '#'

                self.graphic_2d_map_y.generate_element_as_map(
                    name='Y_axis_AGSS',
                    x_indexes=[render_y_index(index, self.map) for index in
                               range(self.position.simplified_coordinates[2] - 4,
                                     self.position.simplified_coordinates[2] + 5)],
                    **{render_z_index(z_index, self.map): [
                        render_cell(z_index, self.position.simplified_coordinates[1], y_index, self.map, self.position)
                        for y_index in
                        range(self.position.simplified_coordinates[2] - 4, self.position.simplified_coordinates[2] + 5)]
                        for z_index in
                        range(self.position.simplified_coordinates[0] + 2, self.position.simplified_coordinates[0] - 3,
                              -1)}
                )

                self.graphic_2d_map_y.content.insert(0, ' ' * self.graphic_2d_map_y.width)

            def render_screen(self):
                self.screen.content.clear()
                self.render_graphic_2d_map_y()
                self.render_graphic_2d_map_x()
                self.render_data_table()
                self.render_terrain_map()
                self.screen.generate_element_as_screen(
                    'Console_Python_Space_Flight_Simulator',
                    [self.data_table,
                     self.data_map_terrain],
                    [self.graphic_2d_map_x,
                     self.graphic_2d_map_y],

                )

            def test_print(self):
                self.render_screen()
                os.system('cls')
                for line in self.screen.content:
                    print(line)
                time.sleep(0.1)

        def __init__(self, engine):
            self.game_view = self.Game_view(engine)

    def __init__(self):
        from engine import Engine
        self.engine = Engine(100, 100, 50)
        self.engine.key_manager.register_hotkey(self.g_exit,True)
        self.cli_test_graphic = self.Cli_graphic(self.engine)
        self.engine.threads_manager.start_new_thread(self.cli_test_graphic.game_view.test_print)

    def g_exit(self):
        self.engine.threads_manager.stop_all()
        keyboard.unhook_all()


os.system('cls')
game = Console_Python_Space_Flight_Simulator()

# 1# todo: baza i refuel
# 2# todo: minerały i wydobycie + sprzedrz w bazie + płatny refuel
# 3# todo:  menu
#  todo: więciej niż 1 baza
# 4#
