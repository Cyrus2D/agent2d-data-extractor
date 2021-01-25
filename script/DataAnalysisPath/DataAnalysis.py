from enum import Enum, auto

from State import State
from Vector2D import Vector2D


class SortType(Enum):
    X = auto(),
    UNUM = auto(),
    ANGLE_FIELD_CENTER = auto(),
    ANGLE_KICKER = auto(),
    ANGLE_KICKER_GOAL = auto()


class DataAnalysis:
    def __init__(self, file_in, file_out, sort_type=None, randomize=0, img_mode=False, normalize=True):
        self.headers = []

        self.analys_file(file_in, file_out, sort_type, randomize, img_mode, normalize)

    def analys_file(self, file_in, file_out, sort_type, randomize, img_mode, normalize):
        file = open(file_in)
        out = None
        if not img_mode:
            out = open(file_out, 'w')
        self.headers = file.readline().split(',')
        if not img_mode:
            out.write(f"{','.join(self.headers)}")

        # line_number = 0
        while True:
            # line_number += 1
            # if line_number % 100 == 0:
            #     print(line_number / len(content))
            line = file.readline()
            if not line:
                break
            val = line.split(',')

            # Make State
            state: State = State(self.headers, val)
            if state.cycle == State.INVALID_DATA:
                continue

            # Randomize
            if randomize != 0:
                state.randomize(randomize)

            # Sort State
            if sort_type is not None:
                state.sort(self.find_function(state, sort_type))

            # Save State
            if normalize:
                state.normalize()
                
            if img_mode:
                state.export_img(file_out)
            else:
                out.write(f"{state}\n")

    def find_function(self, state, type):
        kicker_pos = Vector2D(state.kicker['pos_x'], state.kicker['pos_y'])
        if type == SortType.ANGLE_KICKER_GOAL:
            return sort_by_angle_kicker(state.kicker, (Vector2D(+52.5, 0) - kicker_pos).th().degree())
        elif type == SortType.ANGLE_KICKER:
            return sort_by_angle_kicker(state.kicker)
        elif type == SortType.ANGLE_FIELD_CENTER:
            return sort_by_angle_field_center()
        elif type == SortType.X:
            return sort_by_x
        elif type == SortType.UNUM:
            return sort_by_unum


# sort functions:
def sort_by_x(player):
    if player['pos_x'] == State.INVALID_DATA:
        return State.INVALID_DATA
    return player['pos_x']


def sort_by_unum(player):
    return -player['unum']


def sort_by_angle_field_center():
    return sort_by_angle_kicker()


def sort_by_angle_kicker(relative_pos=None, relative_angle=0):  # FUNCTIONEHAAAAAAA :D
    if relative_pos is None:
        relative_pos = {'pos_x': 0, 'pos_y': 0}

    def sort(player):

        if player['pos_x'] == State.INVALID_DATA:
            return State.INVALID_DATA
        center = Vector2D(relative_pos['pos_x'], relative_pos['pos_y'])
        player_pos = Vector2D(player['pos_x'], player['pos_y'])
        diff = (player_pos - center).th().degree() - relative_angle  # TODO ABS...?
        if diff > 180:
            diff = -(360 - diff)
        if diff < -180:
            diff = 360 + diff
        return diff

    return sort
