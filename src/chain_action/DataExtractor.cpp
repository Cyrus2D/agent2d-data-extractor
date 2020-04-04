//
// Created by aref on 11/28/19.
//

#include "DataExtractor.h"
#include "cooperative_action.h"
#include <rcsc/player/world_model.h>
#include <random>
#include <time.h>

#define cm ","
#define ADD_ELEM(key, value) fout << (value) << cm

double invalid_data = -2.0;

using namespace rcsc;

DataExtractor::DataExtractor() :
        last_update_cycle(-1) {
}

DataExtractor::~DataExtractor() {
}

#include "../sample_player.h"

void DataExtractor::update(const PlayerAgent *agent, const ActionStatePair *first_layer) {
    const WorldModel &wm = option.worldMode == FULLSTATE ? agent->fullstateWorld() : agent->world();

    if (last_update_cycle == wm.time().cycle())
        return;
    if (!wm.self().isKickable())
        return;
    if (wm.gameMode().type() != rcsc::GameMode::PlayOn)
        return;
    if (!fout.is_open()) {
        init_file(wm);
    }
    last_update_cycle = wm.time().cycle();
    data.clear();

    if (
            ((CooperativeAction &) first_layer->action()).category() > 2
            ||
            !((CooperativeAction &) first_layer->action()).targetPoint().isValid()
            ||
            ((CooperativeAction &) first_layer->action()).targetPlayerUnum() > 11
            ||
            ((CooperativeAction &) first_layer->action()).targetPlayerUnum() < 1
            )
        return;
    // cycle
    ADD_ELEM("cycle", convertor_cycle(last_update_cycle));

    // ball
    extract_ball(wm);

    // kicker
    extract_kicker(wm);

    // players
    extract_players(wm);

    // output
    extract_output(wm,
                   ((CooperativeAction &) first_layer->action()).category(),
                   ((CooperativeAction &) first_layer->action()).targetPoint(),
                   ((CooperativeAction &) first_layer->action()).targetPlayerUnum(),
                   ((CooperativeAction &) first_layer->action()).description(),
                   ((CooperativeAction &) first_layer->action()).firstBallSpeed());
    fout << std::endl;

}

DataExtractor &DataExtractor::i() {
    static DataExtractor instance;
    return instance;
}

void DataExtractor::init_file(const rcsc::WorldModel &wm) {
    time_t rawtime;
    struct tm *timeinfo;
    char buffer[80];

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    std::string dir = "./data/";
    strftime(buffer, sizeof(buffer), "%Y-%m-%d-%H-%M-%S", timeinfo);
    std::string str(buffer);
    std::string rand_name = std::to_string(SamplePlayer::player_port);
    str += "_" + std::to_string(wm.self().unum()) + "_" + wm.opponentTeamName() + "_E" + rand_name + ".csv";

    fout = std::ofstream((dir + str).c_str());

    // Cycle and BALL
    std::string header = "cycle,ballpx,ballpy,ballrx,ballry,ballr,ballt,"
                         "ballvx,ballvy,ballvr,ballvt,ofside_count,";

    // Kicker
    for (int i = 0; i < option.nDribleAngle; i++) {
        header += "drible_angle_" + std::to_string(i) + ",";
    }

    for (int i = 1; i <= 11; i++) {
        if (option.side == TM || option.side == BOTH)
            header += "p_l_" + std::to_string(i) + "_side,";
        if (option.unum == TM || option.unum == BOTH)
            header += "p_l_" + std::to_string(i) + "_unum,";
        if (option.type == TM || option.type == BOTH) {
            header += "p_l_" + std::to_string(i) + "_player_type_id,";
            header += "p_l_" + std::to_string(i) + "_player_type_dash_rate,";
            header += "p_l_" + std::to_string(i) + "_player_type_effort_max,";
            header += "p_l_" + std::to_string(i) + "_player_type_effort_min,";
            header += "p_l_" + std::to_string(i) + "_player_type_kickable,";
            header += "p_l_" + std::to_string(i) + "_player_type_margin,";
            header += "p_l_" + std::to_string(i) + "_player_type_kick_power,";
            header += "p_l_" + std::to_string(i) + "_player_type_decay,";
            header += "p_l_" + std::to_string(i) + "_player_type_size,";
            header += "p_l_" + std::to_string(i) + "_player_type_speed_max,";
        }
        if (option.body == TM || option.body == BOTH)
            header += "p_l_" + std::to_string(i) + "_body,";
        if (option.face == TM || option.face == BOTH)
            header += "p_l_" + std::to_string(i) + "_face,";
        if (option.tackling == TM || option.tackling == BOTH)
            header += "p_l_" + std::to_string(i) + "_tackling,";
        if (option.kicking == TM || option.kicking == BOTH)
            header += "p_l_" + std::to_string(i) + "_kicking,";
        if (option.card == TM || option.card == BOTH)
            header += "p_l_" + std::to_string(i) + "_card,";
        if (option.pos == TM || option.pos == BOTH) {
            header += "p_l_" + std::to_string(i) + "_px,";
            header += "p_l_" + std::to_string(i) + "_py,";
        }
        if (option.relativePos == TM || option.relativePos == BOTH) {
            header += "p_l_" + std::to_string(i) + "_rx,";
            header += "p_l_" + std::to_string(i) + "_ry,";
        }
        if (option.polarPos == TM || option.polarPos == BOTH) {
            header += "p_l_" + std::to_string(i) + "_r,";
            header += "p_l_" + std::to_string(i) + "_t,";
        }
        if (option.in_offside == TM)
            header += "p_l_" + std::to_string(i) + "_in_ofside,";
        if (option.vel == TM || option.vel == BOTH) {
            header += "p_l_" + std::to_string(i) + "_vx,";
            header += "p_l_" + std::to_string(i) + "_vy,";
        }
        if (option.polarVel == TM || option.polarVel == BOTH) {
            header += "p_l_" + std::to_string(i) + "_vr,";
            header += "p_l_" + std::to_string(i) + "_vt,";
        }
        if (option.counts == TM || option.counts == BOTH) {
            header += "p_l_" + std::to_string(i) + "_poscount,";
            header += "p_l_" + std::to_string(i) + "_velcount,";
        }
        if (option.isKicker == TM || option.isKicker == BOTH)
            header += "p_l_" + std::to_string(i) + "_iskicker,";
        if (option.openAnglePass == TM || option.openAnglePass == BOTH) {
            header += "p_l_" + std::to_string(i) + "_passangle,";
            header += "p_l_" + std::to_string(i) + "_dpassdist,";
        }
        if (option.nearestOppDist == TM || option.nearestOppDist == BOTH)
            header += "p_l_" + std::to_string(i) + "_nearoppdist,";
        if (option.polarGoalCenter == TM || option.polarGoalCenter == BOTH) {
            header += "p_l_" + std::to_string(i) + "_angleGCr_angleGCr,";
            header += "p_l_" + std::to_string(i) + "_angleGCt_angleGCt,";
        }
        if (option.openAngleGoal == TM || option.openAngleGoal == BOTH)
            header += "p_l_" + std::to_string(i) + "_openGAngle_openGAngle,";
    }
    for (int i = 1; i <= 11; i++) {
        if (option.side == OPP || option.side == BOTH)
            header += "p_r_" + std::to_string(i) + "_side,";
        if (option.unum == OPP || option.unum == BOTH)
            header += "p_r_" + std::to_string(i) + "_unum,";
        if (option.type == OPP || option.type == BOTH) {
            header += "p_r_" + std::to_string(i) + "_player_type_id,";
            header += "p_r_" + std::to_string(i) + "_player_type_dash_rate,";
            header += "p_r_" + std::to_string(i) + "_player_type_effort_max,";
            header += "p_r_" + std::to_string(i) + "_player_type_effort_min,";
            header += "p_r_" + std::to_string(i) + "_player_type_kickable,";
            header += "p_r_" + std::to_string(i) + "_player_type_margin,";
            header += "p_r_" + std::to_string(i) + "_player_type_kick_power,";
            header += "p_r_" + std::to_string(i) + "_player_type_decay,";
            header += "p_r_" + std::to_string(i) + "_player_type_size,";
            header += "p_r_" + std::to_string(i) + "_player_type_speed_max,";
        }
        if (option.body == OPP || option.body == BOTH)
            header += "p_r_" + std::to_string(i) + "_body,";
        if (option.face == OPP || option.face == BOTH)
            header += "p_r_" + std::to_string(i) + "_face,";
        if (option.tackling == OPP || option.tackling == BOTH)
            header += "p_r_" + std::to_string(i) + "_tackling,";
        if (option.kicking == OPP || option.kicking == BOTH)
            header += "p_r_" + std::to_string(i) + "_kicking,";
        if (option.card == OPP || option.card == BOTH)
            header += "p_r_" + std::to_string(i) + "_card,";
        if (option.pos == OPP || option.pos == BOTH) {
            header += "p_r_" + std::to_string(i) + "_px,";
            header += "p_r_" + std::to_string(i) + "_py,";
        }
        if (option.relativePos == OPP || option.relativePos == BOTH) {
            header += "p_r_" + std::to_string(i) + "_rx,";
            header += "p_r_" + std::to_string(i) + "_ry,";
        }
        if (option.polarPos == OPP || option.polarPos == BOTH) {
            header += "p_r_" + std::to_string(i) + "_r,";
            header += "p_r_" + std::to_string(i) + "_t,";
        }
        if (option.vel == OPP || option.vel == BOTH) {
            header += "p_r_" + std::to_string(i) + "_vx,";
            header += "p_r_" + std::to_string(i) + "_vy,";
        }
        if (option.polarVel == OPP || option.polarVel == BOTH) {
            header += "p_r_" + std::to_string(i) + "_vr,";
            header += "p_r_" + std::to_string(i) + "_vt,";
        }
        if (option.counts == OPP || option.counts == BOTH) {
            header += "p_r_" + std::to_string(i) + "_poscount,";
            header += "p_r_" + std::to_string(i) + "_velcount,";
        }
        if (option.isKicker == OPP || option.isKicker == BOTH)
            header += "p_r_" + std::to_string(i) + "_iskicker,";
        if (option.openAnglePass == OPP || option.openAnglePass == BOTH) {
            header += "p_r_" + std::to_string(i) + "_passangle,";
            header += "p_r_" + std::to_string(i) + "_dpassdist,";
        }
        if (option.nearestOppDist == OPP || option.nearestOppDist == BOTH)
            header += "p_r_" + std::to_string(i) + "_nearoppdist,";
        if (option.polarGoalCenter == OPP || option.polarGoalCenter == BOTH) {
            header += "p_r_" + std::to_string(i) + "_angleGCr,";
            header += "p_r_" + std::to_string(i) + "_angleGCt,";
        }
        if (option.openAngleGoal == OPP || option.openAngleGoal == BOTH)
            header += "p_r_" + std::to_string(i) + "_openGAngle,";
    }
    header += "out_category,out_targetx,out_targety,out_unum,out_unum_index,out_ball_speed, out_ball_dir,out_desc,";
    fout << header << std::endl;
}

void DataExtractor::extract_ball(const rcsc::WorldModel &wm) {
    if (wm.ball().posValid()) {
        ADD_ELEM("x", convertor_x(wm.ball().pos().x));
        ADD_ELEM("y", convertor_y(wm.ball().pos().y));
        ADD_ELEM("rx", convertor_x(wm.ball().rpos().x));
        ADD_ELEM("ry", convertor_y(wm.ball().rpos().y));
        Polar ball(wm.ball().rpos());
        ADD_ELEM("r", convertor_dist(ball.r));
        ADD_ELEM("teta", convertor_angle(ball.teta));
    } else {
        ADD_ELEM("x", invalid_data);
        ADD_ELEM("y", invalid_data);
        ADD_ELEM("rx", invalid_data);
        ADD_ELEM("ry", invalid_data);
        ADD_ELEM("r", invalid_data);
        ADD_ELEM("teta", invalid_data);
    }
    if (wm.ball().velValid()) {
        ADD_ELEM("vx", convertor_bvx(wm.ball().vel().x));
        ADD_ELEM("vy", convertor_bvy(wm.ball().vel().y));
        Polar vball(wm.ball().vel());
        ADD_ELEM("vr", convertor_bv(vball.r));
        ADD_ELEM("vteta", convertor_angle(vball.teta));
    } else {
        ADD_ELEM("vx", invalid_data);
        ADD_ELEM("vy", invalid_data);
        ADD_ELEM("vr", invalid_data);
        ADD_ELEM("vteta", invalid_data);
    }
    ADD_ELEM("ofside_count", wm.offsideLineCount());
}

void DataExtractor::extract_kicker(const rcsc::WorldModel &wm) {
    extract_drible_angles(wm);
}

void DataExtractor::extract_players(const rcsc::WorldModel &wm) {
    auto players = sort_players(wm);
    for (uint i = 0; i < players.size(); i++) {
        const AbstractPlayerObject *player = players[i];
        if (player == NULL) {
            add_null_player(invalid_data,
                            (i <= 10 ? TM : OPP));
            continue;
        }

        DataSide side = player->side() == wm.ourSide() ? TM : OPP;
        extract_base_data(player, side);
        extract_pos(player, wm, side);
        extract_vel(player, side);
        extract_counts(player, side);

        if (option.isKicker == side || option.isKicker == BOTH) {
            if (player->unum() == wm.self().unum()) {
                ADD_ELEM("iskicker", 1);
            } else
                ADD_ELEM("iskicker", 0);
        }

        extract_pass_angle(player, wm, side);
        extract_goal_polar(player, side);
        extract_goal_open_angle(player, wm, side);
    }
}

std::vector<const AbstractPlayerObject *>
DataExtractor::sort_players(const rcsc::WorldModel &wm) {
    std::vector<const AbstractPlayerObject *> tms;
    std::vector<const AbstractPlayerObject *> opps;
    tms.clear();
    opps.clear();
    for (int i = 1, j = 0; i <= 11 && j <= 1; i++) {
        const AbstractPlayerObject *player;
        if (j == 0)
            player = wm.ourPlayer(i);
        else
            player = wm.theirPlayer(i);

        if (player == NULL
            || player->isGhost()
            || player->unum() < 1
            || !player->pos().isValid()
            || !player->vel().isValid())
            continue;
        if (j == 0)
            tms.push_back(player);
        else
            opps.push_back(player);

        if (i == 11) {
            i = 0;
            j += 1;
        }
    }
    auto x_sort = [](const AbstractPlayerObject *p1, const AbstractPlayerObject *p2) -> bool {
        return p1->pos().x > p2->pos().x;
    };
    const AbstractPlayerObject *self = wm.ourPlayer(wm.self().unum());
    auto degree_sort = [self](const AbstractPlayerObject *p1, const AbstractPlayerObject *p2) -> bool {
        return (p1->pos() - self->pos()).th().abs() < (p2->pos() - self->pos()).th().abs();
    }; // TODO sort from -180 to 180, change it by ABS to change from back to front, IS IT OKEY???!

    if (option.playerSortMode == ANGLE) {
        std::sort(tms.begin(), tms.end(), degree_sort);
        std::sort(opps.begin(), opps.end(), degree_sort);
    } else if (option.playerSortMode == X) {
        std::sort(tms.begin(), tms.end(), x_sort);
        std::sort(opps.begin(), opps.end(), x_sort);
    }

    for (; tms.size() < 11; tms.push_back(static_cast<AbstractPlayerObject *>(0)));
    for (; opps.size() < 11; opps.push_back(static_cast<AbstractPlayerObject *>(0)));

    tms.insert(tms.end(), opps.begin(), opps.end());
    return tms;
}


void DataExtractor::add_null_player(int unum, DataSide side) {
    if (option.side == side || option.side == BOTH)
        ADD_ELEM("side", side == OPP ? -1 : 1);
    if (option.unum == side || option.unum == BOTH)
        ADD_ELEM("unum", convertor_unum(unum));
    if (option.type == side || option.type == BOTH) {
        ADD_ELEM("player_type_id", invalid_data);
        ADD_ELEM("player_type_dash_rate", invalid_data);
        ADD_ELEM("player_type_effort_max", invalid_data);
        ADD_ELEM("player_type_effort_min", invalid_data);
        ADD_ELEM("player_type_kickable", invalid_data);
        ADD_ELEM("player_type_margin", invalid_data);
        ADD_ELEM("player_type_kick_power", invalid_data);
        ADD_ELEM("player_type_decay", invalid_data);
        ADD_ELEM("player_type_size", invalid_data);
        ADD_ELEM("player_type_speed_max", invalid_data);
    }
    if (option.body == side || option.body == BOTH)
        ADD_ELEM("body", invalid_data);
    if (option.face == side || option.face == BOTH)
        ADD_ELEM("face", invalid_data);
    if (option.tackling == side || option.tackling == BOTH)
        ADD_ELEM("tackling", invalid_data);
    if (option.kicking == side || option.kicking == BOTH)
        ADD_ELEM("kicking", invalid_data);
    if (option.card == side || option.card == BOTH)
        ADD_ELEM("card", invalid_data);
    if (option.pos == side || option.pos == BOTH) {
        ADD_ELEM("x", invalid_data);
        ADD_ELEM("y", invalid_data);
    }
    if (option.in_offside == side || option.in_offside == BOTH) {
        ADD_ELEM("in_ofside", invalid_data);
    }
    if (option.relativePos == side || option.relativePos == BOTH) {
        ADD_ELEM("rx", invalid_data);
        ADD_ELEM("ry", invalid_data);
    }
    if (option.polarPos == side || option.polarPos == BOTH) {
        ADD_ELEM("r", invalid_data);
        ADD_ELEM("teta", invalid_data);
    }
    if (option.vel == side || option.vel == BOTH) {
        ADD_ELEM("vx", invalid_data);
        ADD_ELEM("vy", invalid_data);
    }
    if (option.polarVel == side || option.polarVel == BOTH) {
        ADD_ELEM("vr", invalid_data);
        ADD_ELEM("vteta", invalid_data);
    }
    if (option.counts == side || option.counts == BOTH) {
        ADD_ELEM("poscount", invalid_data);
        ADD_ELEM("velcount", invalid_data);
    }
    if (option.isKicker == side || option.isKicker == BOTH)
        ADD_ELEM("iskicker", invalid_data);
    if (option.openAnglePass == side || option.openAnglePass == BOTH) {
        ADD_ELEM("min_pass_angle", invalid_data);
        ADD_ELEM("direct_pass_dist", invalid_data);
    }
    if (option.nearestOppDist == side || option.nearestOppDist == BOTH)
        ADD_ELEM("opp_dist", invalid_data);
    if (option.polarGoalCenter == side || option.polarGoalCenter == BOTH) {
        ADD_ELEM("angleGCr", invalid_data);
        ADD_ELEM("angleGCt", invalid_data);
    }
    if (option.openAngleGoal == side || option.openAngleGoal == BOTH)
        ADD_ELEM("openGAngle", invalid_data);
}

void DataExtractor::extract_output(const rcsc::WorldModel &wm,
                                   int category,
                                   const rcsc::Vector2D &target,
                                   const int &unum,
                                   const char *desc,
                                   double ball_speed) {
    ADD_ELEM("category", category);
    ADD_ELEM("targetx", target.x);
    ADD_ELEM("targety", target.y);
    ADD_ELEM("unum", unum);
    ADD_ELEM("unum_index", find_unum_index(wm, unum));
    ADD_ELEM("ball_speed", ball_speed);
    ADD_ELEM("ball_dir", convertor_angle((target - wm.ball().pos()).th().degree()));
    if (category == 2) {
        if (std::string(desc) == "strictDirect") {
            ADD_ELEM("desc", 0);
        } else if (std::string(desc) == "strictLead") {
            ADD_ELEM("desc", 1);
        } else if (std::string(desc) == "strictThrough") {
            ADD_ELEM("desc", 2);
        } else if (std::string(desc) == "cross") {
            ADD_ELEM("desc", 3);
        }
    } else {
        ADD_ELEM("desc", 4);
    }
}

void DataExtractor::extract_pass_angle(const AbstractPlayerObject *player, const WorldModel &wm, DataSide side) {
    Vector2D ball_pos = wm.ball().pos();
    Vector2D tm_pos = player->pos();
    double min_angle = 180;
    double min_dist = 200;
    for (int o = 1; o <= 11; o++) {
        const AbstractPlayerObject *opp = wm.theirPlayer(o);
        if (opp == nullptr || opp->unum() != o)
            continue;
        if (opp->pos().dist(tm_pos) < min_dist)
            min_dist = opp->pos().dist(tm_pos);
        if (opp->pos().dist(ball_pos) > tm_pos.dist(ball_pos))
            continue;
        AngleDeg diff = (tm_pos - ball_pos).th() - (opp->pos() - ball_pos).th();
        double diff_double = diff.abs();
        if (diff_double < min_angle)
            min_angle = diff_double;
    }
    if (option.openAnglePass == side || option.openAnglePass == BOTH) {
        ADD_ELEM("min_pass_angle", convertor_angle(min_angle));
        ADD_ELEM("direct_pass_dist", convertor_dist(ball_pos.dist(tm_pos)));
    }
    if (option.nearestOppDist == side || option.nearestOppDist == BOTH)
        ADD_ELEM("opp_dist", convertor_dist(min_dist));
}

void DataExtractor::extract_vel(const AbstractPlayerObject *player, DataSide side) {
    if (option.vel == side || option.vel == BOTH) {
        ADD_ELEM("vx", convertor_pvx(player->vel().x));
        ADD_ELEM("vy", convertor_pvy(player->vel().y));
    }
    if (option.polarVel == side || option.polarVel == BOTH) {
        Polar vball(player->vel());
        ADD_ELEM("vr", convertor_pv(vball.r));
        ADD_ELEM("vteta", convertor_angle(vball.teta));
    }
}

void DataExtractor::extract_pos(const AbstractPlayerObject *player, const WorldModel &wm, DataSide side) {
    if (option.pos == side || option.pos == BOTH) {
        ADD_ELEM("x", convertor_x(player->pos().x));
        ADD_ELEM("y", convertor_y(player->pos().y));
    }
    Vector2D rpos = player->pos() - wm.self().pos();
    if (option.relativePos == side || option.relativePos == BOTH) {
        ADD_ELEM("rx", convertor_x(rpos.x));
        ADD_ELEM("ry", convertor_y(rpos.y));
    }
    if (option.polarPos == side || option.polarPos == BOTH) {
        Polar ball(rpos);
        ADD_ELEM("r", convertor_dist(ball.r));
        ADD_ELEM("teta", convertor_angle(ball.teta));
    }
    if (option.in_offside == side || option.in_offside == BOTH) {
        if (player->pos().x > wm.offsideLineX()) {
            ADD_ELEM("in_ofside", 1);
        } else {
            ADD_ELEM("in_ofside", 0);
        }
    }
}

void DataExtractor::extract_goal_polar(const AbstractPlayerObject *player, DataSide side) {
    if (!(option.polarGoalCenter == side || option.polarGoalCenter == BOTH))
        return;
    Vector2D goal_center = Vector2D(52, 0);

    Polar polar = Polar(goal_center - player->pos());
    ADD_ELEM("angleGCr", convertor_dist(polar.r));
    ADD_ELEM("angleGCt", convertor_angle(polar.teta));
}

void DataExtractor::extract_goal_open_angle(const rcsc::AbstractPlayerObject *player,
                                            const rcsc::WorldModel &wm,
                                            DataSide side) {
    if (!(option.openAngleGoal == side || option.openAngleGoal == BOTH))
        return;
    Vector2D goal_t = Vector2D(52, -7);
    Vector2D goal_b = Vector2D(52, 7);
    Triangle2D player_goal_area = Triangle2D(goal_b, goal_t, player->pos());

    std::vector<Vector2D> players_in_area;

    for (int i = 1; i <= 11; i++) {
        const AbstractPlayerObject *opp = wm.theirPlayer(i);
        if (opp == NULL || opp->unum() < 1)
            continue;
        if (!player_goal_area.contains(opp->pos()))
            continue;

        players_in_area.push_back(opp->pos());
    }
    players_in_area.push_back(goal_t);
    players_in_area.push_back(goal_b);

    std::sort(players_in_area.begin(), players_in_area.end(),
              [player](Vector2D p1, Vector2D p2) -> bool {
                  return (p1 - player->pos()).th().degree() < (p2 - player->pos()).th().degree();
              });

    double max_open_angle = -1000;
    for (uint i = 1; i < players_in_area.size(); i++) {
        double angle_diff = fabs((players_in_area[i] - player->pos()).th().degree()
                                 - (players_in_area[i - 1] - player->pos()).th().degree());
        if (angle_diff > max_open_angle)
            max_open_angle = angle_diff;
    }


    ADD_ELEM("goal_open_angle", convertor_angle(max_open_angle));
}

void DataExtractor::extract_base_data(const rcsc::AbstractPlayerObject *player, DataSide side) {
    if (option.side == side || option.side == BOTH)
        ADD_ELEM("side", player->side());
    if (option.unum == side || option.unum == BOTH)
        ADD_ELEM("unum", convertor_unum(player->unum()));
    if (option.type == side || option.type == BOTH)
        extract_type(player, side);
    if (option.body == side || option.body == BOTH)
        ADD_ELEM("body", convertor_angle(player->body().degree()));
    if (option.face == side || option.face == BOTH)
        ADD_ELEM("face", convertor_angle(player->face().degree()));
    if (option.tackling == side || option.tackling == BOTH)
        ADD_ELEM("tackling", player->isTackling());
    if (option.kicking == side || option.kicking == BOTH)
        ADD_ELEM("kicking", player->kicked());
    if (option.card == side || option.card == BOTH)
        ADD_ELEM("card", player->card());
}

void DataExtractor::extract_type(const AbstractPlayerObject *player, DataSide side) {
    ADD_ELEM("player_type_id", convertor_type(player->playerTypePtr()->id()));
    ADD_ELEM("player_type_dash_rate", player->playerTypePtr()->dashPowerRate());
    ADD_ELEM("player_type_effort_max", player->playerTypePtr()->effortMax());
    ADD_ELEM("player_type_effort_min", player->playerTypePtr()->effortMin());
    ADD_ELEM("player_type_kickable", player->playerTypePtr()->kickableArea());
    ADD_ELEM("player_type_margin", player->playerTypePtr()->kickableMargin());
    ADD_ELEM("player_type_kick_power", player->playerTypePtr()->kickPowerRate());
    ADD_ELEM("player_type_decay", player->playerTypePtr()->playerDecay());
    ADD_ELEM("player_type_size", player->playerTypePtr()->playerSize());
    ADD_ELEM("player_type_speed_max", player->playerTypePtr()->realSpeedMax());
}

void DataExtractor::extract_counts(const rcsc::AbstractPlayerObject *player, DataSide side) {
    if (!(option.counts == side || option.counts == BOTH))
        return;

    ADD_ELEM("posCount", convertor_counts(player->posCount()));
    ADD_ELEM("velCount", convertor_counts(player->velCount()));
}

void DataExtractor::extract_drible_angles(const WorldModel &wm) {

//    const PlayerObject *kicker = wm.interceptTable()->fastestTeammate(); // TODO What is error ?!?!
    const AbstractPlayerObject *kicker = wm.ourPlayer(wm.self().unum());
    if (kicker == NULL || kicker->unum() < 0) {
        for (int i = 1; i <= option.nDribleAngle; i++)
            ADD_ELEM("drible_angle", -2);
        return;
    }

    double delta = 360.0 / option.nDribleAngle;
    for (double angle = -180; angle < 180; angle += delta) {

        double min_opp_dist = 1000;
        for (int i = 1; i <= 11; i++) {
            const AbstractPlayerObject *opp = wm.theirPlayer(i);
            if (opp == NULL || opp->unum() < 0)
                continue;

            Vector2D kicker2opp = (opp->pos() - kicker->pos());
            if (kicker2opp.th().degree() < angle || kicker2opp.th().degree() > angle + delta)
                continue;

            double dist = kicker2opp.r();
            if (dist < min_opp_dist)
                min_opp_dist = dist;
        }

        if (min_opp_dist > 30.0)
            ADD_ELEM("drible_angle", convertor_dist(30));
        else
            ADD_ELEM("drible_angle", convertor_dist(min_opp_dist));
    }
}

double DataExtractor::convertor_x(double x) {
    if (!option.use_convertor)
        return x;
//    return x / 52.5;
    return (x + 52.5) / 105.0;
}

double DataExtractor::convertor_y(double y) {
    if (!option.use_convertor)
        return y;
//    return y / 34.0;
    return (y + 34.0) / 68.0;
}

double DataExtractor::convertor_dist(double dist) {
    if (!option.use_convertor)
        return dist;
//    return dist / 63.0 - 1.0;
    return dist / 30.0;
}

double DataExtractor::convertor_angle(double angle) {
    if (!option.use_convertor)
        return angle;
//    return angle / 180.0;
    return (angle + 180.0) / 360.0;
}

double DataExtractor::convertor_type(double type) {
    if (!option.use_convertor)
        return type;
//    return type / 9.0 - 1.0;
    return type / 18.0;
}

double DataExtractor::convertor_cycle(double cycle) {
    if (!option.use_convertor)
        return cycle;
//    return cycle / 3000.0 - 1.0;
    return cycle / 6000.0;
}

double DataExtractor::convertor_bv(double bv) {
    if (!option.use_convertor)
        return bv;
//    return bv / 3.0 * 2 - 1;
    return bv / 3.0;
}

double DataExtractor::convertor_bvx(double bvx) {
    if (!option.use_convertor)
        return bvx;
//    return bvx / 3.0;
    return (bvx + 3.0) / 6.0;
}

double DataExtractor::convertor_bvy(double bvy) {
    if (!option.use_convertor)
        return bvy;
//    return bvy / 3.0;
    return (bvy + 3.0) / 6.0;
}

double DataExtractor::convertor_pv(double pv) {
    if (!option.use_convertor)
        return pv;
    return pv / 1.5;
}

double DataExtractor::convertor_pvx(double pvx) {
    if (!option.use_convertor)
        return pvx;
//    return pvx / 1.5;
    return (pvx + 1.5) / 3.0;
}

double DataExtractor::convertor_pvy(double pvy) {
    if (!option.use_convertor)
        return pvy;
//    return pvy / 1.5;
    return (pvy + 1.5) / 3.0;
}

double DataExtractor::convertor_unum(double unum) {
    if (!option.use_convertor)
        return unum;
    return unum / 11.0;
}

double DataExtractor::convertor_card(double card) {
    if (!option.use_convertor)
        return card;
    return card / 2.0;
}

double DataExtractor::convertor_stamina(double stamina) {
    if (!option.use_convertor)
        return stamina;
    return stamina / 8000.0;
}

double DataExtractor::convertor_counts(double count) {
    count = std::min(count, 20.0);
    if (!option.use_convertor)
        return count;
    return count / 20; // TODO I Dont know the MAX???
}

uint DataExtractor::find_unum_index(const rcsc::WorldModel &wm, uint unum) {
    auto players = sort_players(wm);
    for (uint i = 0; i < 11; i++) {
        auto player = players[i];
        if (player == NULL)
            return 0;
        if (player->unum() == unum)
            return i + 1; // TODO add 1 or not??
    }
}

Polar::Polar(rcsc::Vector2D p) {
    teta = p.th().degree();
    r = p.r();
}

DataExtractor::Option::Option() {
    side = BOTH;
    unum = BOTH;
    type = BOTH;
    body = BOTH;
    face = BOTH;
    tackling = BOTH;
    kicking = BOTH;
    card = BOTH;
    pos = BOTH;
    relativePos = BOTH;
    polarPos = BOTH;
    vel = BOTH;
    polarVel = BOTH;
    counts = BOTH;
    isKicker = BOTH;
    openAnglePass = TM;
    nearestOppDist = TM;
    polarGoalCenter = TM;
    openAngleGoal = TM;
    in_offside = TM;

    dribleAngle = Kicker;
    nDribleAngle = 12;

    worldMode = NONE_FULLSTATE;
    playerSortMode = X;

    use_convertor = true;
}
