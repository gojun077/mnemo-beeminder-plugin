#!/usr/bin/env python3
# beeminder_plus_one.py
# Created on: Apr 17 2021
# Created by: gojun077@gmail.com
#
# Update a mnemosyne card tracking goal on Beeminder if a card is
# graded as '2' or above. Based on after_repetition.py by
# <Peter.Bienstman@UGent.be>


import datetime
import json
from mnemosyne.libmnemosyne.hook import Hook
from mnemosyne.libmnemosyne.plugin import Plugin
from mnemosyne.libmnemosyne.plugin import register_user_plugin
from pathlib import Path
import requests


def submit(comment_moar: str):
    """
    Increment Beeminder goal by +1.0 via the Beeminder API
    """
    try:
        mnemo_cfg_path = str(Path.home()) + "/.config/mnemosyne"
        beeminder_info = mnemo_cfg_path + "/beeminder.json"
        with open(beeminder_info,"r") as f:
            bmndrD = json.load(f)
            url = "https://www.beeminder.com/api/v1/users"
            epoch_utc = int(datetime.datetime.utcnow().timestamp())
            myuser, mygoal = bmndrD["username"], bmndrD["goalname"]
            endpt = f"{url}/{myuser}/goals/{mygoal}/datapoints.json"
            full_comment = bmndrD["comment"] + " | " + comment_moar
            payload = {"auth_token": bmndrD["auth_token"],
                       "timestamp": epoch_utc,
                       "value": 1.0,
                       "comment": full_comment}
            header = {"Content-Type": "application/json"}
            resp_post = requests.post(endpt, headers=header,
                                      data=json.dumps(payload))
            if resp_post.status_code != 200:
                print(f"HTTP Status: {resp_post.status_code}")
                print(f"Error msg: {resp_post.text}")
                raise Exception
            else:
                print("Data successfully submitted to Beeminder")
                resp_data = resp_post.json()
                print(resp_data)
    except (IOError, ValueError, EOFError) as e:
        print(e)
    except:
        print("error occurred while trying to send data to Beeminder...")


class UpdateBeeminder(Hook):
    """
    If a card has a grade of 2 or higher, update a mnemosyne card
    tracking goal on Beeminder
    """
    used_for = "after_repetition"

    def run(self, card):
        if card.grade > 2:
            submit(f"card grade was {card.grade}")


class AfterRepUpdBmndrPlugin(Plugin):
    """
    """
    name = "Update Beeminder after Rep"
    description = "Send data to Beeminder after card score >= 2"
    components = [UpdateBeeminder]
    supported_API_level = 3


register_user_plugin(AfterRepUpdBmndrPlugin)

