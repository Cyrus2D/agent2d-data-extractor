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
#include <DataExtractor.h>

#include "neck_offensive_intercept_neck.h"

#define UNMARK_DEBUG

using namespace rcsc;

DeepNueralNetwork Unmark::dnn = DeepNueralNetwork();

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
    std::cout << "UNMARK" << std::endl;
    const WorldModel &wm = agent->fullstateWorld();

    const AbstractPlayerObject *kicker = wm.interceptTable()->fastestTeammate();
    if (kicker == nullptr || kicker->unum() < 1)
        return false;

    this->kicker_unum = kicker->unum();

    if (!(this->*am_i_the_one)(wm))
        return false;
    std::cout << "am i the one done" << std::endl;
    Vector2D target = (this->*where_should_i_go)(wm);
    std::cout << "where should i go done" << std::endl;

    if (!target.isValid())
        return false;
    if (Body_GoToPoint(target, 0.5, 100).execute(agent))
        return true;
    if (Body_TurnToPoint(target).execute(agent))
        return true;
    return false;
}

bool Unmark::who_everyone(const WorldModel &wm) {
    return true;
}

bool Unmark::who_nearest(const WorldModel &wm) {
    int unum = -1;
    double min_dist = 10000;
    for (int i = 1; i <= 11; i++) {
        const AbstractPlayerObject *tm = wm.ourPlayer(i);
        if (tm == nullptr || tm->unum() < 1)
            continue;

        double dist = tm->distFromBall();
        if (dist < min_dist) {
            min_dist = dist;
            unum = i;
        }
    }
    if (unum == wm.self().unum())
        return true;
    return false;
}


bool Unmark::who_2_nearest(const WorldModel &wm) {
    int unum2 = -1;
    double min_dist2 = 10000;
    int unum = -1;
    double min_dist = 10000;
    for (int i = 1; i <= 11; i++) {
        const AbstractPlayerObject *tm = wm.ourPlayer(i);
        if (tm == nullptr || tm->unum() < 1)
            continue;

        double dist = tm->distFromBall();
        if (dist < min_dist2) {
            min_dist2 = dist;
            unum2 = i;
        }
        if (dist < min_dist) {
            min_dist2 = min_dist;
            unum2 = unum;
            min_dist = dist;
            unum = i;
        }
    }
    if (unum == wm.self().unum() || unum2 == wm.self().unum())
        return true;
    return false;
}

bool Unmark::who_nn(const WorldModel &wm) {
    int unum = get_unum_from_dnn(wm);
    if (unum == wm.self().unum())
        return true;
    return false;
}

bool Unmark::who_2_nn(const WorldModel &wm) {
    std::pair<int, int> unums = get_2_unum_from_dnn(wm);
    if (unums.first == wm.self().unum() || unums.second == wm.self().unum())
        return true;
    return false;
}

bool Unmark::who_pnn(const WorldModel &wm) {
    const double dist = 5;
    const double n_angle = 10.;
    const double angle_step = 360. / n_angle;

    for (int i = 0; i < n_angle; i++) {
        const double angle = (double) i * angle_step;
        const Vector2D new_self_pos = wm.self().pos() + Vector2D::polar2vector(dist, angle);
        if (new_self_pos.absX() > 52.5 || new_self_pos.absY() > 34)
            continue;

        int unum = get_unum_from_dnn(wm, new_self_pos);
        if (unum == wm.self().unum())
            return true;
    }
    return false;
}

bool Unmark::who_2_pnn(const WorldModel &wm) {
    const double dist = 5;
    const double n_angle = 10.;
    const double angle_step = 360. / n_angle;

    for (int i = 0; i < n_angle; i++) {
        double angle = (double) i * angle_step;
        const Vector2D new_self_pos = wm.self().pos() + Vector2D::polar2vector(dist, angle);
        if (new_self_pos.absX() > 52.5 || new_self_pos.absY() > 34)
            continue;

        std::pair<int, int> unums = get_2_unum_from_dnn(wm, new_self_pos);
        if (unums.first == wm.self().unum() || unums.second == wm.self().unum())
            return true;
    }
    return false;
}


rcsc::Vector2D Unmark::where_pass_sim(const WorldModel &wm) {
    const double n_dist = 2.;
    const double dist_step = 5. / n_dist;
    const double n_angle = 10.;
    const double angle_step = 360. / n_angle;

    for (int i_dist = 0; i_dist < n_dist; i_dist++) {
        const double dist = (double) i_dist * dist_step;

        for (int i_angle = 0; i_angle < n_angle; i_angle++) {
            const double angle = (double) i_angle * angle_step;
            const Vector2D new_self_pos = wm.self().pos() + Vector2D::polar2vector(dist, angle);
            int diff = simulate_pass(wm, new_self_pos);
            if (diff > 0)
                return new_self_pos;
        }
    }
    return Vector2D().invalidate();

}

rcsc::Vector2D Unmark::where_pass_sim_diff(const WorldModel &wm) {
    const double n_dist = 2.;
    const double dist_step = 5. / n_dist;
    const double n_angle = 10.;
    const double angle_step = 360. / n_angle;

    int max_diff = 0;
    Vector2D best_pos = Vector2D().invalidate();

    for (int i_dist = 0; i_dist < n_dist; i_dist++) {
        const double dist = (double) i_dist * dist_step;

        for (int i_angle = 0; i_angle < n_angle; i_angle++) {
            const double angle = (double) i_angle * angle_step;
            const Vector2D new_self_pos = wm.self().pos() + Vector2D::polar2vector(dist, angle);
            int diff = simulate_pass(wm, new_self_pos);

            if (diff > max_diff) {
                best_pos = new_self_pos;
                max_diff = diff;
            }
        }
    }
    return best_pos;
}

rcsc::Vector2D Unmark::where_pass_sim_diff_homepos(const WorldModel &wm) {
    const double n_dist = 2.;
    const double dist_step = 5. / n_dist;
    const double n_angle = 10.;
    const double angle_step = 360. / n_angle;

    int max_diff = 0;
    Vector2D best_pos = Vector2D().invalidate();

    for (int i_dist = 0; i_dist < n_dist; i_dist++) {
        const double dist = (double) i_dist * dist_step;

        for (int i_angle = 0; i_angle < n_angle; i_angle++) {
            const double angle = (double) i_angle * angle_step;
            const Vector2D new_self_pos = Strategy::i().getPosition(wm.self().unum())
                                          + Vector2D::polar2vector(dist, angle);
            int diff = simulate_pass(wm, new_self_pos);

            if (diff > max_diff) {
                best_pos = new_self_pos;
                max_diff = diff;
            }
        }
    }
    return best_pos;

}

rcsc::Vector2D Unmark::where_nn(const WorldModel &wm) {
    const double n_dist = 2.;
    const double dist_step = 5. / n_dist;
    const double n_angle = 10.;
    const double angle_step = 360. / n_angle;

    double max_value = -100;
    Vector2D best_pos = Vector2D().invalidate();

    for (int i_dist = 0; i_dist < n_dist; i_dist++) {
        const double dist = (double) i_dist * dist_step;

        for (int i_angle = 0; i_angle < n_angle; i_angle++) {
            const double angle = (double) i_angle * angle_step;
            const Vector2D new_self_pos = wm.self().pos() + Vector2D::polar2vector(dist, angle);
            double value = get_value_from_dnn(wm, new_self_pos);

            if (value > max_value) {
                best_pos = new_self_pos;
                max_value = value;
            }
        }
    }
    return best_pos;
}

rcsc::Vector2D Unmark::where_pass_sim_nn(const WorldModel &wm) {
    const double n_dist = 2.;
    const double dist_step = 5. / n_dist;
    const double n_angle = 10.;
    const double angle_step = 360. / n_angle;

    double max_value = -100;
    Vector2D best_pos = Vector2D().invalidate();

    for (int i_dist = 1; i_dist <= n_dist; i_dist++) {
        const double dist = (double) i_dist * dist_step;

        for (int i_angle = 0; i_angle < n_angle; i_angle++) {
            const double angle = (double) i_angle * angle_step;
            const Vector2D new_self_pos = wm.self().pos() + Vector2D::polar2vector(dist, angle);

            int diff = simulate_pass(wm, new_self_pos);
            if (diff > 0) {
                double value = get_value_from_dnn(wm, new_self_pos);

                if (value > max_value) {
                    best_pos = new_self_pos;
                    max_value = value;
                }
            }
        }
    }
    return best_pos;

}

int Unmark::get_unum_from_dnn(const WorldModel &wm) {
    DataExtractor::i().update(wm);
    std::vector<double> &data = DataExtractor::i().data;
    MatrixXd input(data.size(), 1);
    for (int i = 0; i < data.size(); i++)
        input(i, 0) = data[i];

    Unmark::dnn.Calculate(input);
    int unum = -1;
    double max_val = -10;
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif
    for (int i = 0; i < 11; i++) {
#ifdef UNMARK_DEBUG
        dlog.addText(Logger::MARK, "%f.3", dnn.mOutput(i, 0));
#endif
        if (dnn.mOutput(i, 0) > max_val) {
            max_val = dnn.mOutput(i, 0);
            unum = i + 1;
        }
    }
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif;

    return unum;
}

std::pair<int, int> Unmark::get_2_unum_from_dnn(const WorldModel &wm) {
    DataExtractor::i().update(wm);
    std::vector<double> &data = DataExtractor::i().data;
    MatrixXd input(data.size(), 1);
    for (int i = 0; i < data.size(); i++)
        input(i, 0) = data[i];

    Unmark::dnn.Calculate(input);
    int unum1 = -1;
    int unum2 = -1;
    double max_val1 = -10;
    double max_val2 = -10;
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif;
    for (int i = 0; i < 11; i++) {
#ifdef UNMARK_DEBUG
        dlog.addText(Logger::MARK, "%f.3", dnn.mOutput(i, 0));
#endif
        if (dnn.mOutput(i, 0) > max_val2) {
            max_val2 = dnn.mOutput(i, 0);
            unum2 = i + 1;
        }
        if (dnn.mOutput(i, 0) > max_val1) {
            max_val2 = max_val1;
            unum2 = unum1;
            max_val1 = dnn.mOutput(i, 0);
            unum1 = i + 1;
        }
    }
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif

    return std::pair<int, int>(unum1, unum2);
}

int Unmark::get_unum_from_dnn(const rcsc::WorldModel &wm, const rcsc::Vector2D new_self_pos) {
    DataExtractor::i().update(wm, new_self_pos);
    std::vector<double> &data = DataExtractor::i().data;
    MatrixXd input(data.size(), 1);
    for (int i = 0; i < data.size(); i++)
        input(i, 0) = data[i];

    Unmark::dnn.Calculate(input);
    int unum = -1;
    double max_val = -10;
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif
    for (int i = 0; i < 11; i++) {
#ifdef UNMARK_DEBUG
        dlog.addText(Logger::MARK, "%f.3", dnn.mOutput(i, 0));
#endif
        if (dnn.mOutput(i, 0) > max_val) {
            max_val = dnn.mOutput(i, 0);
            unum = i + 1;
        }
    }
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif

    return unum;
}

std::pair<int, int> Unmark::get_2_unum_from_dnn(const rcsc::WorldModel &wm, const rcsc::Vector2D new_self_pos) {
    DataExtractor::i().update(wm, new_self_pos);
    std::vector<double> &data = DataExtractor::i().data;
    MatrixXd input(data.size(), 1);
    for (int i = 0; i < data.size(); i++)
        input(i, 0) = data[i];

    Unmark::dnn.Calculate(input);
    int unum1 = -1;
    int unum2 = -1;
    double max_val1 = -10;
    double max_val2 = -10;
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif
    for (int i = 0; i < 11; i++) {
#ifdef UNMARK_DEBUG
        dlog.addText(Logger::MARK, "%f.3", dnn.mOutput(i, 0));
#endif
        if (dnn.mOutput(i, 0) > max_val2) {
            max_val2 = dnn.mOutput(i, 0);
            unum2 = i + 1;
        }
        if (dnn.mOutput(i, 0) > max_val1) {
            max_val2 = max_val1;
            unum2 = unum1;
            max_val1 = dnn.mOutput(i, 0);
            unum1 = i + 1;
        }
    }
#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "##########");
#endif

    return std::pair<int, int>(unum1, unum2);
}

int Unmark::simulate_pass(const WorldModel &wm, const rcsc::Vector2D new_self_pos) {
    Vector2D ball_pos = wm.ball().pos();

    double ball_reach_vel = 1;
    double dist = wm.ball().pos().dist(new_self_pos);
    while (dist > 0) {
        dist -= ball_reach_vel;
        ball_reach_vel /= ServerParam::i().ballDecay();
    }

    Vector2D ball_vel = Vector2D::polar2vector(ball_reach_vel, (new_self_pos - ball_pos).th());
    ball_pos += ball_vel;
    ball_vel *= ServerParam::i().ballDecay();
    int min_diff = 100;
    int cycle = 1;
    while (cycle < 40) {

        if (ball_pos.dist(new_self_pos) < 1.1)
            break;

        for (int i = 1; i <= 11; i++) {
            const AbstractPlayerObject *opp = wm.theirPlayer(i);
            if (opp == nullptr || opp->unum() < 0)
                continue;
            auto ptype = opp->playerTypePtr();

            int n_turn = 0;

            double my_speed = opp->vel().r();
            double dir_diff = (opp->body() - (ball_pos - opp->pos()).th()).abs();
            while (dir_diff > 10.0) {
                dir_diff -= ptype->effectiveTurn(ServerParam::i().maxMoment(), my_speed);
                if (dir_diff < 0.0) dir_diff = 0.0;
                my_speed *= ptype->playerDecay();
                ++n_turn;
            }

            int n_dash = ptype->cyclesToReachDistance(opp->pos().dist(ball_pos));
            const int opp_cycle = n_dash + n_turn;

            int diff = opp_cycle - cycle;
            if (diff < 0) {
#ifdef UNMARK_DEBUG
                dlog.addText(Logger::MARK,
                             "new_self_pos(%f.2, %f.2) failed at(%f.2, %f.2), opp%d: ball_cycle(%d), opp_cycle(%d)",
                             new_self_pos.x,
                             new_self_pos.y,
                             ball_pos.x,
                             ball_pos.y,
                             opp->unum(),
                             cycle,
                             opp_cycle);
#endif
                return diff;
            }
            if (diff < min_diff) {
                min_diff = diff;
            }
        }

        ball_pos += ball_vel;
        ball_vel *= ServerParam::i().ballDecay();
        cycle++;
    }

#ifdef UNMARK_DEBUG
    dlog.addText(Logger::MARK, "new_self_pos(%f.2, %f.2) succeed, min_diff: %d",
                 new_self_pos.x,
                 new_self_pos.y,
                 min_diff);
    dlog.addCircle(Logger::MARK, new_self_pos, 0.2, "#000000", true);
#endif

    return min_diff;
}

double Unmark::get_value_from_dnn(const WorldModel &wm, const rcsc::Vector2D new_self_pos) {
    DataExtractor::i().update(wm, new_self_pos);
    std::vector<double> &data = DataExtractor::i().data;
    MatrixXd input(data.size(), 1);
    for (int i = 0; i < data.size(); i++)
        input(i, 0) = data[i];

    Unmark::dnn.Calculate(input);
    double value = dnn.mOutput(wm.self().unum() - 1, 0);
    return value;
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

    if (mate_min < self_min && mate_min < opp_min + 2)
        if (Unmark(Unmark::TWO_NN, Unmark::PASS_SIM_DIFF).execute(agent))
            return true;

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
