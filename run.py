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

from sc2.paths import get_user_sc2_install, BASEDIR, PF


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
    with open('data/' + output_file + '.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([*p1.get_info, *p2.get_info, data[MetaData.Map]])


def start_replay(replay_name: Union[str, os.PathLike]):
    # Enter replay name here
    # The replay should be either in this folder and you can give it a relative path, or change it to the absolute path
    home_replay_folder = Path.home() / "Documents" / "StarCraftII" / "Replays"
    replay_path = home_replay_folder / replay_name
    if not replay_path.is_file():
        logger.warning(f"You are on linux, please put the replay in directory {home_replay_folder}")
        raise FileNotFoundError
    replay_path = str(replay_path)
    assert os.path.isfile(
        replay_path
    ), "Replay not exists"
    observer = ObserverBot(os.path.basename(replay_name).split('.')[0])
    metadata = _metadata(replay_path)
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
    replays = [file for file in os.listdir(Path.home() / "Documents" / "StarCraftII" / "Replays")]
    for replay in replays:
        res = start_replay(replay)
    print('end')
