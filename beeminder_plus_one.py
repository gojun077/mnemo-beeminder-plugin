#!/usr/bin/env python3
# beeminder_plus_one.py
# Created on: Apr 17 2021
# Created by: gojun077@gmail.com
# Last Updated: Sep 23 2021
#
# Update a mnemosyne card tracking goal on Beeminder if a card is
# graded as '2' or above. Based on after_repetition.py by
# <Peter.Bienstman@UGent.be>


import datetime
import json
import requests
from mnemosyne.libmnemosyne.hook import Hook
from mnemosyne.libmnemosyne.plugin import Plugin
from mnemosyne.libmnemosyne.plugin import register_user_plugin
from pathlib import Path
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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

            retry_strategy = Retry(
                total = 3,
                status_forcelist = [429, 500, 502, 503, 504],
                method_whitelist = ["HEAD", "GET", "PUT", "DELETE", "OPTIONS",
                                    "POST", "TRACE"],
                backoff_factor = 2
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            sess = requests.Session()
            sess.mount = ("https://", adapter)
            resp_sess = sess.post(endpt, headers=header,
                                      data=json.dumps(payload))
            resp_sess.raise_for_status()
            resp_data = resp_sess.json()
            print(resp_data)
    except requests.exceptions.ConnectionError as e:
        print(f"ConnError: {e}, payload: {full_comment}")
    except requests.exceptions.Timeout as e:
        print(f"Conn TIMEOUT: {e}, payload: {full_comment}")
    except requests.exceptions.HTTPError as e:
        print(f"status code {resp_sess.status_code} from {url}: {e}, payload: {full_comment}")
    except:
        print("error occurred while trying to send data to Beeminder...")


class UpdateBeeminder(Hook):
    """
    If a card has a grade of 2 or higher, update a mnemosyne card
    tracking goal on Beeminder
    """
    used_for = "after_repetition"

    def run(self, card):
        if card.grade >= 2:
            submit(f"card grade was {card.grade}")


class AfterRepUpdBmndrPlugin(Plugin):
    """
    """
    name = "Update Beeminder after Rep"
    description = "Send data to Beeminder after card score >= 2"
    components = [UpdateBeeminder]
    supported_API_level = 3


register_user_plugin(AfterRepUpdBmndrPlugin)

