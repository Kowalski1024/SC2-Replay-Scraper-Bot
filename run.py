import os
import csv
import platform
import mpyq
from pathlib import Path
from typing import Union
from loguru import logger
from multiprocessing import Process

from sc2.main import run_replay
from s2protocol import versions

from observer_bot import ObserverBot
from player_details import PlayerDetails, MetaData
import time

def _metadata(replay_name):
    archive = mpyq.MPQArchive(replay_name)
    contents = archive.read_file('replay.details')
    header = versions.latest().decode_replay_details(contents)
    p1 = PlayerDetails(header['m_playerList'][0])
    p2 = PlayerDetails(header['m_playerList'][1])
    map_name = header['m_title'].decode('ascii')
    return {MetaData.Player_1: p1, MetaData.Player_2: p2, MetaData.Map: map_name}


def write_metadata(replay_name, data):
    output_file = os.path.basename(replay_name).split('.')[0]
    p1, p2 = data[MetaData.Player_1], data[MetaData.Player_2]
    with open('data/datasets/'+output_file+'.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([*p1.get_info, *p2.get_info, data[MetaData.Map]])


def start_replay(replay_name: Union[str, os.PathLike]):
    # Enter replay name here
    # The replay should be either in this folder and you can give it a relative path, or change it to the absolute path
    if platform.system() == "Linux":
        home_replay_folder = Path.home() / "Documents" / "StarCraft II" / "Replays"
        replay_path = home_replay_folder / replay_name
        if not replay_path.is_file():
            logger.warning(f"You are on linux, please put the replay in directory {home_replay_folder}")
            raise FileNotFoundError
        replay_path = str(replay_path)
    elif os.path.isabs(replay_name):
        replay_path = replay_name
    else:
        # Convert relative path to absolute path, assuming this replay is in this folder
        folder_path = os.path.dirname(__file__)
        replay_path = os.path.join(folder_path, replay_name)
    assert os.path.isfile(
        replay_path
    ), "Run worker_rush.py in the same folder first to generate a replay. Then run watch_replay.py again."
    observer = ObserverBot(os.path.basename(replay_name).split('.')[0])
    metadata = _metadata(replay_name)
    if metadata[MetaData.Player_1].result == 1:
        winner_id = 1
    elif metadata[MetaData.Player_2].result == 1:
        winner_id = 2
    else:
        return
    write_metadata(replay_name, metadata)
    logger.info(f"Observer as player {winner_id}")
    return run_replay(observer, replay_path=replay_path, observed_id=winner_id, realtime=False)


if __name__ == "__main__":
    replays = ["data/replays/" + file for file in os.listdir("data\\replays") if file.endswith(".SC2Replay")]
    for replay in replays:
        res = start_replay(replay)
    pass

