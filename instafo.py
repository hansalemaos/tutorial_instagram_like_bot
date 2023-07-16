import glob

from check_if_nan import is_nan
from get_consecutive_filename import get_free_filename
import numpy as np
from adbkit import ADBTools
from time import sleep
from urllib import parse
from random import choice,randint,uniform
from a_cv2_calculate_simlilarity import add_similarity_to_cv2
import cv2
add_similarity_to_cv2()
from a_cv_imwrite_imread_plus import add_imwrite_plus_imread_plus_to_cv2
add_imwrite_plus_imread_plus_to_cv2()
import pandas as pd
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions
pd_add_apply_ignore_exceptions()
def get_uiautomator_frame(screenshotfolder="c:\\ttscreenshots"):
    adb.aa_update_screenshot()
    return adb.aa_get_all_displayed_items_from_uiautomator(
        screenshotfolder=screenshotfolder,  # screenshots will be saved here
        max_variation_percent_x=10,  # used for one of the click functions, to not click exactly in the center - more information below
        max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
        loung_touch_delay=(
            1000,
            1500,
        ),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
        swipe_variation_startx=10,  # swipe coordinate variations in percent
        swipe_variation_endx=10,
        swipe_variation_starty=10,
        swipe_variation_endy=10,
        sdcard="/storage/emulated/0/",  # sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
        tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
        bluestacks_divider=32767,  # coordinates must be recalculated for BlueStacks https://stackoverflow.com/a/73733261/15096247 when using sendevent
    )


ADBTools.aa_kill_all_running_adb_instances()
adb_path = r"C:\ProgramData\chocolatey\bin\adb.exe"
deviceserial = 'localhost:5555'
adb = ADBTools(adb_path=adb_path,
               deviceserial=deviceserial)
adb.aa_start_server()
sleep(3)
adb.aa_connect_to_device()
imagefolder = r'C:\jaclickada'
tags = ['pythonprogramming']
tag = choice(tags)
website = f'https://instagram.com/explore/tags/{parse.quote(tag)}/'
adb.aa_open_website(website)
sleep(5)
while True:
    df=get_uiautomator_frame()
    df=df.loc[(df.bb_area > 125000) & (df.bb_area < 130000)]
    picspath = glob.glob(fr'{imagefolder}\*.png')
    pics = [cv2.imread_plus(pic, channels_in_output=3) for pic
            in picspath]
    for pic in pics:
        df = df.loc[
            df.bb_screenshot.ds_apply_ignore(False,
            lambda x: sum(
            cv2.calculate_simlilarity_of_2_pics(x,
            pic)) < 2.5)]
    if not df.empty:

        fname = get_free_filename(folder=imagefolder, fileextension=".png", leadingzeros=5)
        cv2.imwrite(fname, df.bb_screenshot.iloc[0])
        df.iloc[0].ff_bb_tap_center_variation(10, 10)
        sleep(uniform(2, 3))
        adb.aa_swipe(randint(400, 600),
                     randint(1400, 1800),
                     randint(400, 600),
                     randint(200, 300),
                     uniform(0.5, 1.5))
        sleep(uniform(2,3))
        df = pd.DataFrame()
        while df.empty:
            df = get_uiautomator_frame()
        df = df.loc[(df.bb_area > 1000) & (df.bb_area < 2000)]
        df = df.loc[~df.bb_screenshot.ds_apply_ignore(True,
                                                 lambda x: is_nan(x, emptyiters=True))]
        df2 = df.loc[
            df.bb_screenshot.apply(lambda x: np.any(
                np.where((x[..., 2] == 255) & (x[..., 1] == 48) & (x[..., 0] == 64))))]
        if df2.empty:
            sleep(uniform(1,3))
            df.loc[df.bb_center_x_cropped ==
                   df.bb_center_x_cropped.value_counts().index[0]].iloc[
                0].ff_bb_tap_exact_center()
            sleep(3)
        adb.aa_execute_multiple_adb_shell_commands(['input keyevent 4'])
    else:
        adb.aa_swipe(randint(400, 600),
                     randint(1400, 1800),
                     randint(400, 600),
                     randint(200, 300),
                     uniform(0.5, 1.5))
    sleep(uniform(1,5))