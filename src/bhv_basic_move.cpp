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

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include "bhv_basic_move.h"

#include "strategy.h"

#include "bhv_basic_tackle.h"

#include <rcsc/action/basic_actions.h>
#include <rcsc/action/body_go_to_point.h>
#include <rcsc/action/body_intercept.h>
#include <rcsc/action/neck_turn_to_ball_or_scan.h>
#include <rcsc/action/neck_turn_to_low_conf_teammate.h>

#include <rcsc/player/player_agent.h>
#include <rcsc/player/debug_client.h>
#include <rcsc/player/intercept_table.h>

#include <rcsc/common/logger.h>
#include <rcsc/common/server_param.h>

#include "neck_offensive_intercept_neck.h"

using namespace rcsc;


Unmark::Unmark(Unmark::Who _who, Unmark::Where _where) {
    this->who = _who;
    this->where = _where;


    if (this->who == EVERYONE)
        am_i_the_one = &Unmark::who_everyone;
    else if (this->who == NEAREST)
        am_i_the_one = &Unmark::who_nearest;
    else if (this->who == TWO_NEAREST)
        am_i_the_one = &Unmark::who_2_nearest;
    else if (this->who == ONE_NN)
        am_i_the_one = &Unmark::who_nn;
    else if (this->who == TWO_NN)
        am_i_the_one = &Unmark::who_2_nn;
    else if (this->who == ONE_PNN)
        am_i_the_one = &Unmark::who_pnn;
    else if (this->who == TWO_PNN)
        am_i_the_one = &Unmark::who_2_pnn;
    else
        am_i_the_one = nullptr;

    if (this->where == PASS_SIM)
        where_should_i_go = &Unmark::where_pass_sim;
    else if (this->where == PASS_SIM_DIFF)
        where_should_i_go = &Unmark::where_pass_sim_diff;
    else if (this->where == PASS_SIM_DIFF_HOMEPOS)
        where_should_i_go = &Unmark::where_pass_sim_diff_homepos;
    else if (this->where == NN)
        where_should_i_go = &Unmark::where_nn;
    else if (this->where == PASS_SIM_NN)
        where_should_i_go = &Unmark::where_pass_sim_nn;
    else
        where_should_i_go = nullptr;

}

bool Unmark::execute(PlayerAgent *agent) {
    const WorldModel& wm = agent->world();
    if (!(this->*am_i_the_one)(wm))
        return false;
    Vector2D target = (this->*where_should_i_go)(wm);
    if (Body_GoToPoint(target, 0.5, 100).execute(agent))
        return true;
    if (Body_TurnToPoint(target).execute(agent))
        return true;
    return false;
}

bool Unmark::who_nearest(const WorldModel &wm) {
    return false;
}

bool Unmark::who_nn(const WorldModel &wm) {
    return false;
}

rcsc::Vector2D Unmark::where_pass_sim(const WorldModel &wm) {
    return rcsc::Vector2D();
}

rcsc::Vector2D Unmark::where_pass_sim_diff_homepos(const WorldModel &wm) {
    return rcsc::Vector2D();
}

rcsc::Vector2D Unmark::where_nn(const WorldModel &wm) {
    return rcsc::Vector2D();
}

rcsc::Vector2D Unmark::where_pass_sim_diff(const WorldModel &wm) {
    return rcsc::Vector2D();
}

rcsc::Vector2D Unmark::where_pass_sim_nn(const WorldModel &wm) {
    return rcsc::Vector2D();
}

bool Unmark::who_2_nearest(const WorldModel &wm) {
    return false;
}

bool Unmark::who_2_nn(const WorldModel &wm) {
    return false;
}

bool Unmark::who_pnn(const WorldModel &wm) {
    return false;
}

bool Unmark::who_2_pnn(const WorldModel &wm) {
    return false;
}

bool Unmark::who_everyone(const WorldModel &wm) {
    return false;
}


/*-------------------------------------------------------------------*/
/*!
 *
 *

 */

bool
Bhv_BasicMove::execute(PlayerAgent *agent) {
    dlog.addText(Logger::TEAM,
                 __FILE__": Bhv_BasicMove");

    //-----------------------------------------------
    // tackle
    if (Bhv_BasicTackle(0.8, 80.0).execute(agent)) {
        return true;
    }

    const WorldModel &wm = agent->world();
    /*--------------------------------------------------------*/
    // chase ball
    const int self_min = wm.interceptTable()->selfReachCycle();
    const int mate_min = wm.interceptTable()->teammateReachCycle();
    const int opp_min = wm.interceptTable()->opponentReachCycle();

    if (!wm.existKickableTeammate()
        && (self_min <= 3
            || (self_min <= mate_min
                && self_min < opp_min + 3)
        )
            ) {
        dlog.addText(Logger::TEAM,
                     __FILE__": intercept");
        Body_Intercept().execute(agent);
        agent->setNeckAction(new Neck_OffensiveInterceptNeck());

        return true;
    }

    const Vector2D target_point = Strategy::i().getPosition(wm.self().unum());
    const double dash_power = Strategy::get_normal_dash_power(wm);

    double dist_thr = wm.ball().distFromSelf() * 0.1;
    if (dist_thr < 1.0) dist_thr = 1.0;

    dlog.addText(Logger::TEAM,
                 __FILE__": Bhv_BasicMove target=(%.1f %.1f) dist_thr=%.2f",
                 target_point.x, target_point.y,
                 dist_thr);

    agent->debugClient().addMessage("BasicMove%.0f", dash_power);
    agent->debugClient().setTarget(target_point);
    agent->debugClient().addCircle(target_point, dist_thr);

    if (!Body_GoToPoint(target_point, dist_thr, dash_power
    ).execute(agent)) {
        Body_TurnToBall().execute(agent);
    }

    if (wm.existKickableOpponent()
        && wm.ball().distFromSelf() < 18.0) {
        agent->setNeckAction(new Neck_TurnToBall());
    } else {
        agent->setNeckAction(new Neck_TurnToBallOrScan());
    }

    return true;
}
