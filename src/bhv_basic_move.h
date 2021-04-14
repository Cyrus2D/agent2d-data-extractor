// -*-c++-*-

/*
 *Copyright:

 Copyright (C) Hidehisa AKIYAMA

 This code is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3, or (at your option)
 any later version.

 This code is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this code; see the file COPYING.  If not, write to
 the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.

 *EndCopyright:
 */

/////////////////////////////////////////////////////////////////////

#ifndef BHV_BASIC_MOVE_H
#define BHV_BASIC_MOVE_H

#include <rcsc/geom/vector_2d.h>
#include <rcsc/player/soccer_action.h>
#include <action_chain_graph.h>
#include <CppDNN/DeepNueralNetwork.h>

class Bhv_BasicMove
        : public rcsc::SoccerBehavior {
public:
    Bhv_BasicMove() {}

    bool execute(rcsc::PlayerAgent *agent);

private:
    double getDashPower(const rcsc::PlayerAgent *agent);
};


class Unmark {
public:
    enum Who {
        EVERYONE,
        NEAREST,
        TWO_NEAREST,
        ONE_NN,
        TWO_NN,
        ONE_PNN,
        TWO_PNN
    };

    enum Where {
        PASS_SIM,
        PASS_SIM_DIFF,
        PASS_SIM_DIFF_HOMEPOS,
        NN,
        PASS_SIM_NN
    };

public:
    Who who;
    Where where;
    int kicker_unum;

    Unmark(Who _who, Where _where);

    bool (Unmark::*am_i_the_one)(const rcsc::WorldModel &);

    rcsc::Vector2D (Unmark::*where_should_i_go)(const rcsc::WorldModel &);

    bool execute(rcsc::PlayerAgent *agent);

public:
    static DeepNueralNetwork dnn;

public:
    bool who_everyone(const rcsc::WorldModel &wm);

    bool who_nearest(const rcsc::WorldModel &wm);

    bool who_nn(const rcsc::WorldModel &wm);

    bool who_2_nearest(const rcsc::WorldModel &wm);

    bool who_2_nn(const rcsc::WorldModel &wm);

    bool who_pnn(const rcsc::WorldModel &wm);

    bool who_2_pnn(const rcsc::WorldModel &wm);

    rcsc::Vector2D where_pass_sim(const rcsc::WorldModel &wm);

    rcsc::Vector2D where_pass_sim_diff_homepos(const rcsc::WorldModel &wm);

    rcsc::Vector2D where_nn(const rcsc::WorldModel &wm);

    rcsc::Vector2D where_pass_sim_diff(const rcsc::WorldModel &wm);

    rcsc::Vector2D where_pass_sim_nn(const rcsc::WorldModel &wm);

    int get_unum_from_dnn(const rcsc::WorldModel &wm);

    std::pair<int, int> get_2_unum_from_dnn(const rcsc::WorldModel &wm);

    int get_unum_from_dnn(const rcsc::WorldModel &wm, const rcsc::Vector2D new_self_pos);

    std::pair<int, int> get_2_unum_from_dnn(const rcsc::WorldModel &wm, const rcsc::Vector2D new_self_pos);

    int simulate_pass(const rcsc::WorldModel &wm, const rcsc::Vector2D new_self_pos);

    double get_value_from_dnn(const rcsc::WorldModel &wm, const rcsc::Vector2D new_self_pos);

};


#endif













