from PIL import Image, ImageDraw, ImageFont
import ImageTools
import pandas as pd
import numpy as np

# params
show_img = False
save_img = False
save_npa = True


field_size_X = 256  #  x axis size
field_size_Y = 160  #  y axis size

center_kicker = True

ball_size = 3  # ball radius pixels
player_size_multiplier = 10  # KickAble_Area multiplier

use_background = False  # use soc cerwindow background
solid_field_color = "black"  # Change for BG_color
ball_color = "white"

use_goals = True  # markout goals
goal_color = (128, 96, 78, 200)

use_body_angle = True  # draw an arc for body
body_angle_size = 4  # body angle multiplier
body_angle_color = "black"

use_transparent = True
use_color_range_our = True
use_color_range_opp = False
main_color_jump = 5  # main color get decrised over palyer numbers
transparent_alpha = 150  # transparent_alpha 0 - 255

data = pd.read_csv(f"g:/SW_pic/test.csv")  # Load Data
image_count = 2  # data.count()[0]  # number of image

if use_background:  # use background
    temp_img = Image.open(f"g:/SW_pic/back-full.jpg")
    temp_img.thumbnail(field_size_X, field_size_Y)
else:
    temp_img = Image.new(
        "RGB",
        (field_size_X * 2, field_size_Y * 2)
        if center_kicker
        else (field_size_X, field_size_Y),
        color=solid_field_color,
    )

if save_npa:
    np_images = np.zeros((image_count, field_size_Y, field_size_X, 3))
label = np.zeros(image_count)

if use_goals and not center_kicker:  # mark the goals out
    temp_draw = ImageDraw.Draw(temp_img, "RGBA")
    temp_draw.rectangle(
        (0, field_size_Y * 13 / 32, field_size_X / 256, field_size_Y * 19 / 32),
        fill=goal_color,
    )
    temp_draw.rectangle(
        (
            field_size_X,
            field_size_Y * 13 / 32,
            field_size_X - field_size_X / 256,
            field_size_Y * 19 / 32,
        ),
        fill=goal_color,
    )

temp_img.save(f"g:/SW_pic/temp_img.jpg")


# Start
for i in range(image_count):

    dp = data.loc[i]

    # set image
    img = Image.open(f"g:/SW_pic/temp_img.jpg")
    draw = ImageDraw.Draw(img, "RGBA")

    if center_kicker:
        kicker_unum = 0
        for u in range(1, 12):
            if dp[f"p_l_{u}_iskicker"]:
                kicker_unum = u

        kicker_pos_change = [
            (1 - dp[f"p_l_{kicker_unum}_px"]) * field_size_X,
            (1 - dp[f"p_l_{kicker_unum}_py"]) * field_size_Y,
        ]

        if use_goals:
            draw.rectangle(
                (
                    kicker_pos_change[0],
                    field_size_Y * 13 / 32 + kicker_pos_change[1],
                    field_size_X / 256 + kicker_pos_change[0],
                    field_size_Y * 19 / 32 + kicker_pos_change[1],
                ),
                fill=goal_color,
            )
            draw.rectangle(
                (
                    field_size_X + kicker_pos_change[0],
                    field_size_Y * 13 / 32 + kicker_pos_change[1],
                    field_size_X - field_size_X / 256 + kicker_pos_change[0],
                    field_size_Y * 19 / 32 + kicker_pos_change[1],
                ),
                fill=goal_color,
            )
    # Draw OppPlayers
    for u in range(1, 12):
        player_x = dp[f"p_r_{u}_px"] * field_size_X
        player_y = dp[f"p_r_{u}_py"] * field_size_Y
        if center_kicker:
            player_x += kicker_pos_change[0]
            player_y += kicker_pos_change[1]

        plyer_ka = dp[f"p_r_{u}_player_type_kickable"] * player_size_multiplier

        draw.ellipse(
            (
                player_x - plyer_ka,
                player_y - plyer_ka,
                player_x + plyer_ka,
                player_y + plyer_ka,
            ),
            fill=(
                0,
                2 + 23 * u,
                255 - main_color_jump * u,
                transparent_alpha if use_transparent else 255,
            )
            if use_color_range_opp
            else (0, 2, 255, transparent_alpha if use_transparent else 255),
        )
        if use_body_angle:
            player_body = dp[f"p_r_{u}_body"] * 360
            draw.pieslice(
                (
                    player_x - plyer_ka,
                    player_y - plyer_ka,
                    player_x + plyer_ka,
                    player_y + plyer_ka,
                ),
                player_body - body_angle_size + 180,
                player_body + body_angle_size + 180,
                fill=body_angle_color,
            )
            draw.arc(
                (
                    player_x - plyer_ka,
                    player_y - plyer_ka,
                    player_x + plyer_ka,
                    player_y + plyer_ka,
                ),
                player_body - body_angle_size + 180,
                player_body + body_angle_size + 180,
                fill=(
                    0,
                    2 + 23 * u,
                    255 - main_color_jump * u,
                    transparent_alpha if use_transparent else 255,
                )
                if use_color_range_opp
                else (0, 2, 255, transparent_alpha if use_transparent else 255),
            )

    # Draw OurPlayers
    for u in range(1, 12):
        player_x = dp[f"p_l_{u}_px"] * field_size_X
        player_y = dp[f"p_l_{u}_py"] * field_size_Y
        if center_kicker:
            player_x += kicker_pos_change[0]
            player_y += kicker_pos_change[1]

        plyer_ka = dp[f"p_l_{u}_player_type_kickable"] * player_size_multiplier
        draw.ellipse(
            (
                player_x - plyer_ka,
                player_y - plyer_ka,
                player_x + plyer_ka,
                player_y + plyer_ka,
            ),
            fill=(
                255 - main_color_jump * u,
                2 + 23 * u,
                0,
                transparent_alpha if use_transparent else 255,
            )
            if use_color_range_our
            else (255, 2, 0, transparent_alpha if use_transparent else 255),
        )
        if use_body_angle:
            player_body = dp[f"p_l_{u}_body"] * 360
            draw.pieslice(
                (
                    player_x - plyer_ka,
                    player_y - plyer_ka,
                    player_x + plyer_ka,
                    player_y + plyer_ka,
                ),
                player_body - body_angle_size + 180,
                player_body + body_angle_size + 180,
                fill=body_angle_color,
            )
            draw.arc(
                (
                    player_x - plyer_ka,
                    player_y - plyer_ka,
                    player_x + plyer_ka,
                    player_y + plyer_ka,
                ),
                player_body - body_angle_size + 180,
                player_body + body_angle_size + 180,
                (
                    255 - main_color_jump * u,
                    2 + 23 * u,
                    0,
                    transparent_alpha if use_transparent else 255,
                )
                if use_color_range_our
                else (255, 2, 0, transparent_alpha if use_transparent else 255),
            )

    # Draw Ball
    ball_x = dp.ballpx * field_size_X
    ball_y = dp.ballpy * field_size_Y
    if center_kicker:
        ball_x += kicker_pos_change[0]
        ball_y += kicker_pos_change[1]
    draw.ellipse(
        (
            ball_x - ball_size,
            ball_y - ball_size,
            ball_x + ball_size,
            ball_y + ball_size,
        ),
        fill=ball_color,
    )

    label[i] = dp["out_unum"]

    # if i == 1:
    #     img.save(f"g:/SW_pic/pic/sb_{i}.jpg")
    # if i == 0:
    #     img.save(f"g:/SW_pic/pic/sb_{i}.jpg")

    if show_img:
        img.show()
    if save_img:
        img.save(f"g:/SW_pic/pic/s_{i}.jpg")
    if save_npa:
        # PIL images into NumPy arrays
        np_images[i] = np.asarray(img)

if save_npa:
    np.save(f"g:/SW_pic/np_img.npy", np_images)
    print(np_images.shape)

np.save(f"g:/SW_pic/img_label.npy", label)
# DONE
print("done")