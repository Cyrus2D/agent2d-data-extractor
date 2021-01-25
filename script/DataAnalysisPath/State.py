from random import randint

import numpy as np
from PIL import Image

from Vector2D import Vector2D


def converter_inv(a=1.0, b=0.0):
    def convert(x):
        return (a * x) - b

    return convert


def converter_y_inv():
    return converter_inv(68, 34)


def converter_x_inv():
    return converter_inv(105, 52)


def converter_dist_inv():
    return converter_inv(30, 0)


def converter_angle_inv():
    return converter_inv(360, 180)


def converter_count_inv():
    return converter_inv(20, 0)


def converter(a=1.0, b=0.0):
    def convert(x):
        return (x + b) / a

    return convert


def converter_y():
    return converter(68, 34)


def converter_x():
    return converter(105, 52)


def converter_dist():
    return converter(30, 0)


def converter_angle():
    return converter(360, 180)


def converter_count():
    return converter(20, 0)


class State:
    INVALID_DATA = -2
    KICKER_BE_FIRST = False
    CONVERTER_INV = {
        'cycle': converter_inv(6000, 0),
        'ball_pos_x': converter_x_inv(),
        'ball_pos_y': converter_y_inv(),
        'ball_kicker_x': converter_x_inv(),
        'ball_kicker_y': converter_y_inv(),
        'ball_kicker_r': converter_dist_inv(),
        'ball_kicker_t': converter_angle_inv(),
        'ball_pos_r': converter_dist_inv(),
        'ball_pos_t': converter_angle_inv(),
        'ball_vel_x': converter_inv(6, 3),
        'ball_vel_y': converter_inv(6, 3),
        'ball_vel_r': converter_inv(3, 0),
        'ball_vel_t': converter_angle_inv(),
        'offside_count': converter_inv(1, 0),
        'drible_angle': converter_dist_inv(),
        'side': converter_inv(),
        'unum': converter_inv(11),
        'player_type_id': converter_inv(18),
        'player_type_dash_rate': converter_inv(),
        'player_type_effort_max': converter_inv(),
        'player_type_effort_min': converter_inv(),
        'player_type_kickable': converter_inv(),
        'player_type_margin': converter_inv(),
        'player_type_kick_power': converter_inv(),
        'player_type_decay': converter_inv(),
        'player_type_size': converter_inv(),
        'player_type_speed_max': converter_inv(),
        'body': converter_angle_inv(),
        'face': converter_angle_inv(),
        'tackling': converter_inv(),
        'kicking': converter_inv(),
        'card': converter_inv(),
        'pos_x': converter_x_inv(),
        'pos_y': converter_y_inv(),
        'kicker_x': converter_x_inv(),
        'kicker_y': converter_y_inv(),
        'kicker_r': converter_dist_inv(),
        'kicker_t': converter_angle_inv(),
        'pos_r': converter_dist_inv(),
        'pos_t': converter_angle_inv(),  # todo pos r,t ?
        'in_offside': converter_inv(),
        'vel_x': converter_inv(3, 1.5),
        'vel_y': converter_inv(3, 1.5),
        'vel_r': converter_inv(1.5),
        'vel_t': converter_angle_inv(),
        'poscount': converter_count_inv(),
        'velcount': converter_count_inv(),
        'is_kicker': converter_inv(),
        'pass_angle': converter_angle_inv(),
        'pass_dist': converter_dist_inv(),
        'nearoppdist': converter_dist_inv(),
        'angle_goal_center_r': converter_dist_inv(),
        'angle_goal_center_t': converter_angle_inv(),
        'openGAngle_openGAngle': converter_angle_inv(),
        'stamina': converter_inv(8000),
        'stamina_count': converter_count_inv(),
        'out_category': converter_inv(),
        'out_target_x': converter_inv(),
        'out_target_y': converter_inv(),
        'out_unum': converter_inv(),
        'out_unum_index': converter_inv(),
        'out_ball_speed': converter_inv(),
        'out_ball_dir': converter_angle_inv(),
        'out_desc': converter_inv(),
    }
    CONVERTER = {
        'cycle': converter(6000, 0),
        'ball_pos_x': converter_x(),
        'ball_pos_y': converter_y(),
        'ball_kicker_x': converter_x(),
        'ball_kicker_y': converter_y(),
        'ball_kicker_r': converter_dist(),
        'ball_kicker_t': converter_angle(),
        'ball_pos_r': converter_dist(),
        'ball_pos_t': converter_angle(),
        'ball_vel_x': converter(6, 3),
        'ball_vel_y': converter(6, 3),
        'ball_vel_r': converter(3, 0),
        'ball_vel_t': converter_angle(),
        'offside_count': converter(1, 0),
        'drible_angle': converter_dist(),
        'side': converter(),
        'unum': converter(11),
        'player_type_id': converter(18),
        'player_type_dash_rate': converter(),
        'player_type_effort_max': converter(),
        'player_type_effort_min': converter(),
        'player_type_kickable': converter(),
        'player_type_margin': converter(),
        'player_type_kick_power': converter(),
        'player_type_decay': converter(),
        'player_type_size': converter(),
        'player_type_speed_max': converter(),
        'body': converter_angle(),
        'face': converter_angle(),
        'tackling': converter(),
        'kicking': converter(),
        'card': converter(),
        'pos_x': converter_x(),
        'pos_y': converter_y(),
        'kicker_x': converter_x(),
        'kicker_y': converter_y(),
        'kicker_r': converter_dist(),
        'kicker_t': converter_angle(),
        'pos_r': converter_dist(),
        'pos_t': converter_angle(),  # todo pos r,t ?
        'in_offside': converter(),
        'vel_x': converter(3, 1.5),
        'vel_y': converter(3, 1.5),
        'vel_r': converter(1.5),
        'vel_t': converter_angle(),
        'poscount': converter_count(),
        'velcount': converter_count(),
        'is_kicker': converter(),
        'pass_angle': converter_angle(),
        'pass_dist': converter_dist(),
        'nearoppdist': converter_dist(),
        'angle_goal_center_r': converter_dist(),
        'angle_goal_center_t': converter_angle(),
        'openGAngle_openGAngle': converter_angle(),
        'stamina': converter(8000),
        'stamina_count': converter_count(),
        'out_category': converter(),
        'out_target_x': converter(),
        'out_target_y': converter(),
        'out_unum': converter(),
        'out_unum_index': converter(),
        'out_ball_speed': converter(),
        'out_ball_dir': converter_angle(),
        'out_desc': converter(),
    }

    FILE_COUNT = 0

    def __init__(self, headers, val):
        self.cycle = State.INVALID_DATA
        self.other = {}

        self.ball = {}
        self.teammates = []
        self.opponents = []

        self.kicker = {}
        self.target_player = {}

        self.output = {}

        data = {}
        for h, v in zip(headers, val):
            data[h] = v

        self.set_cycle(data)
        print(self.cycle)

        self.set_others(data)

        self.set_output(data)

        self.set_players(data)

    def set_cycle(self, data):
        if data['cycle'] == '':
            return
        self.cycle = round(State.CONVERTER_INV['cycle'](float(data['cycle'])))

    def set_players(self, data):
        oppu = [i for i in range(1, 12)]
        tmu = [i for i in range(1, 12)]
        for j in range(2):
            for i in range(1, 12):
                start_key = f"p_" \
                            f"{'l' if j == 0 else 'r'}_" \
                            f"{i}_"
                keys = [key for key in data.keys() if key.strip(' ').startswith(start_key)]
                if keys == []:
                    continue

                player = {}
                side = 1 if j == 0 else -1
                for key in keys:
                    if key[len(start_key):].startswith("pass_opp") \
                            or key[len(start_key):].startswith("near"):
                        if key.endswith("dist") or key.endswith("line") or key.endswith("proj"):
                            player[key[len(start_key):]] = State.CONVERTER_INV['pass_dist'](float(data[key]))
                        elif key.endswith("angle") or key.endswith("diffbody"):
                            player[key[len(start_key):]] = State.CONVERTER_INV['pass_angle'](float(data[key]))
                    else:
                        player[key[len(start_key):]] = State.CONVERTER_INV[key[len(start_key):]](float(data[key]))
                player['unum'] = round(player['unum'])
                if side == 1:
                    player['is_kicker'] = round(player['is_kicker'])
                if side == -1:
                    self.opponents.append(player)
                    if 11 < player['unum'] or player['unum'] < 1:
                        player['unum'] = oppu.pop(0)
                    else:
                        oppu.pop(oppu.index(player['unum']))
                elif side == 1:
                    self.teammates.append(player)

                    if 11 < player['unum'] or player['unum'] < 1:
                        player['unum'] = tmu.pop(0)
                    else:
                        tmu.pop(tmu.index(player['unum']))

                    if player['unum'] == self.output['unum']:
                        self.target_player = player
                    if side and player["is_kicker"] == 1:
                        self.kicker = player

    def set_output(self, data):
        start_key = "out_"
        keys = [key for key in data.keys() if key.strip(' ').startswith(start_key)]
        for key in keys:
            self.output[key[len(start_key):]] = State.CONVERTER_INV[key](float(data[key]))

    def sort(self, function):
        # SORTING PLAYERS
        self.opponents.sort(key=function, reverse=True)
        if (State.KICKER_BE_FIRST):
            player = self.teammates.pop(self.teammates.index(self.kicker))
            self.teammates.sort(key=function, reverse=True)
            self.teammates = [player] + self.teammates
        else:
            self.teammates.sort(key=function, reverse=True)

        # CHANGE UNUM_INDEX OUTPUT
        self.output['unum_index'] = self.teammates.index(self.target_player) + 1

    def set_others(self, data):
        if self.cycle == State.INVALID_DATA:
            return
            # BALL
        start_key = 'ball'
        ball_keys = [key for key in data.keys() if key.strip(' ').startswith(start_key)]
        for key in ball_keys:
            self.ball[key[len(start_key):]] = State.CONVERTER_INV[key](float(data[key]))

        # OFFSIDE COUNT and drible feature
        other_keys = ['offside_count'] + [key for key in data.keys() if key.strip(' ').startswith('drible_angle')]
        for key in other_keys:
            if key.startswith('drible_angle'):
                self.other[key] = State.CONVERTER_INV['drible_angle'](float(data[key]))
            else:
                self.other[key] = State.CONVERTER_INV[key](float(data[key]))

    def normalize(self):
        self.cycle = State.CONVERTER['cycle'](self.cycle)
        for k in self.other:
            if k.startswith('drible_angle'):
                self.other[k] = State.CONVERTER['drible_angle'](self.other[k])
            else:
                self.other[k] = State.CONVERTER[k](self.other[k])

        for k in self.ball:
            self.ball[k] = State.CONVERTER['ball' + k](self.ball[k])

        for p in self.teammates:
            for k in p:
                if k.startswith("pass_opp") \
                        or k.startswith("near"):
                    if k.endswith("dist") or k.endswith("line") or k.endswith("proj"):
                        p[k] = State.CONVERTER['pass_dist'](p[k])
                    elif k.endswith("angle") or k.endswith("diffbody"):
                        p[k] = State.CONVERTER['pass_angle'](p[k])
                else:
                    p[k] = State.CONVERTER[k](p[k])

        for p in self.opponents:
            for k in p:
                p[k] = State.CONVERTER[k](p[k])

        for k in self.output:
            if k == '_ball_dir':
                self.output[k] = State.CONVERTER[" out" + k](self.output[k])
            else:
                self.output[k] = State.CONVERTER["out_" + k](self.output[k])

    def __repr__(self):
        o = ""
        o += f"{self.cycle},{','.join([str(d) for d in self.ball.values()])},"
        o += f"{','.join([str(d) for d in self.other.values()])},"
        for p in self.teammates + self.opponents:
            o += f"{','.join([str(d) for d in p.values()])},"
        o += f"{','.join([str(d) for d in self.output.values()])},"
        return o

    def headers(self):
        o = (['cycle']
             + [f"ball{k}" for k in self.ball.keys()]
             + list(self.other.keys())
             + [f"p_l_1_{k}" for k in self.teammates[0].keys()]
             + [f"p_r_1_{k}" for k in self.opponents[0].keys()]
             + list(self.output.keys()))
        return o

    def randomize(self, randomize):
        for players in ['tm', 'opp']:
            valid_players = self.valid_teammates() if players == 'tm' else self.valid_opponents()
            if len(valid_players) % 2 == 1:
                valid_players += [valid_players[randint(0, len(valid_players) - 1)]]
            rand = min(randomize, int(len(valid_players) / 2))

            for i in range(rand):
                u1 = valid_players.pop(randint(0, len(valid_players) - 1))
                u2 = valid_players.pop(randint(0, len(valid_players) - 1))

                self.swap_players(players, u1, u2)

    def swap_players(self, players, u1, u2):
        players = self.teammates if players == 'tm' else self.opponents

        for p in players:
            if p['unum'] == u1:
                p['unum'] = u2
            elif p['unum'] == u2:
                p['unum'] = u1

    def valid_teammates(self):
        unum = []

        for p in self.teammates:
            if p['px'] == State.INVALID_DATA:
                break
            unum.append(p['unum'])

        return unum

    def valid_opponents(self):
        unum = []

        for p in self.opponents:
            if p['px'] == State.INVALID_DATA:
                break
            unum.append(p['unum'])

        return unum

    def export_img(self, dir):  # 24x39
        data = np.zeros((24, 39))
        data[0, 0] = self.cycle
        data[0, 1:11] = list(self.ball.values())
        data[0, 11:24] = list(self.other.values())

        for i in range(11):
            data[i + 1, :] = list(self.teammates[i].values())
        for i in range(11):
            data[i + 12, :30] = list(self.opponents[i].values())

        im = Image.fromarray(data * 255)
        if im.mode != 'RGB':
            im = im.convert('RGB')

        file_name = f"{dir}/{State.FILE_COUNT}"
        for out in self.output.values():
            file_name += f"_{out}"
        im.save(f"{file_name}.png")
        State.FILE_COUNT += 1
