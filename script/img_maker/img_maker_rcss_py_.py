from PIL import Image, ImageDraw, ImageFont
import ImageTools
import pandas as pd
import numpy as np

# params

save_img = False
save_npa = True

field_size_X = 512  #  x axis size
field_size_Y = 320  #  y axis size

ball_size = 4  # ball radius pixels
player_size_multiplier = 14  # KickAble_Area multiplier

use_background = False  # use soc cerwindow background
solid_field_color = "black"  # Change for BG_color
ball_color = "white"

use_goals = False  # markout goals
goal_color = "brown"

use_body_angle = True  # draw an arc for body
body_angle_size = 4  # body angle multiplier
body_angle_color = "black"

use_color_range_our = True
use_color_range_opp = False
main_color_jump = 5  # main color get decrised over palyer numbers

data = pd.read_csv(f"g:/SW_pic/test.csv")  # Load Data
image_count = data.count()[0]  # number of image

if use_background:  # use background
    temp_img = Image.open(f"g:/SW_pic/back-full.jpg")
    temp_img.thumbnail(field_size_X, field_size_Y)
else:
    temp_img = Image.new("RGB", (field_size_X, field_size_Y), color=solid_field_color)

if save_npa:
    np_images = np.zeros((image_count, field_size_Y, field_size_X, 3))

if use_goals:  # mark the goals out
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.rectangle(
        (0, field_size_Y * 13 / 32, field_size_X / 265, field_size_Y * 19 / 32),
        fill=goal_color,
    )
    temp_draw.rectangle(
        (
            field_size_X,
            field_size_Y * 13 / 32,
            field_size_X - field_size_X / 265,
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
    draw = ImageDraw.Draw(img)

    # Draw OppPlayers
    for u in range(1, 12):
        player_x = dp[f"p_r_{u}_px"] * field_size_X
        player_y = dp[f"p_r_{u}_py"] * field_size_Y
        plyer_ka = dp[f"p_r_{u}_player_type_kickable"] * player_size_multiplier

        draw.ellipse(
            (
                player_x - plyer_ka,
                player_y - plyer_ka,
                player_x + plyer_ka,
                player_y + plyer_ka,
            ),
            fill=(0, 2 + 23 * u, 255 - main_color_jump * u)
            if use_color_range_opp
            else (0, 2, 255),
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

    # Draw OurPlayers
    for u in range(1, 12):
        player_x = dp[f"p_l_{u}_px"] * field_size_X
        player_y = dp[f"p_l_{u}_py"] * field_size_Y
        plyer_ka = dp[f"p_l_{u}_player_type_kickable"] * player_size_multiplier
        draw.ellipse(
            (
                player_x - plyer_ka,
                player_y - plyer_ka,
                player_x + plyer_ka,
                player_y + plyer_ka,
            ),
            fill=(255 - main_color_jump * u, 2 + 23 * u, 0)
            if use_color_range_our
            else (255, 2, 0),
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

    # Draw Ball
    ball_x = dp.ballpx * field_size_X
    ball_y = dp.ballpy * field_size_Y
    draw.ellipse(
        (
            ball_x - ball_size,
            ball_y - ball_size,
            ball_x + ball_size,
            ball_y + ball_size,
        ),
        fill=ball_color,
    )

    # image save
    # img.show()
    if save_img:
        img.save(f"g:/SW_pic/pic/{i}.jpg")
    if save_npa:
        # PIL images into NumPy arrays
        np_images[i] = np.asarray(img)

if save_npa:
    np.save(f"g:/SW_pic/np_img.npy", np_images)
    print(np_images.shape)

# DONE
print("done")