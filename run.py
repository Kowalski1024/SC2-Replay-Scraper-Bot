import os
import mpyq
import json
import argparse
import platform
from pathlib import Path

from loguru import logger
from tqdm import tqdm
import sc2.main
from s2protocol import versions

from observer_bot import ObserverBot


def progress_bar_linux():
    def logger_decorator(func):
        def inner(*args, **kwargs):
            with tqdm.external_write_mode():
                func(*args, **kwargs)

        return inner

    logger._log = logger_decorator(logger._log)


def read_replay_metadata(replay_path):
    archive = mpyq.MPQArchive(replay_path)
    details = archive.read_file('replay.details')
    game_data = json.loads(archive.read_file('replay.gamemetadata.json'))
    game_version = int(game_data['DataBuild'])
    header = versions.build(game_version).decode_replay_details(details)

    return header['m_timeUTC'], game_data


def run_scraper(args, working_dir):
    replays_path = Path(args.replays_path)
    scraper_data_path = args.scraper_data if args.scraper_data else working_dir.joinpath('scraper_data.json')
    dest_dir_path = args.output if args.output else working_dir.joinpath('datasets')
    conf_path = Path(args.config) if args.config else None

    replays = os.listdir(replays_path)

    try:
        with open(scraper_data_path) as file:
            scraper_data = json.load(file)
    except FileNotFoundError:
        scraper_data = {}

    logger.info(f'Starting the Scraper... Replays to check: {len(replays)}')
    for i, replay in enumerate(replays):
        replay_path = replays_path.joinpath(str(replay))
        time_utc, game_data = read_replay_metadata(replay_path)

        winner_id = 0
        race = 'Unknown'
        for player in game_data['Players']:
            if player['Result'] == 'Win':
                winner_id = player['PlayerID']
                race = player['AssignedRace']

        if winner_id == 0:
            logger.info(f'Game {replay} without a winner, skip the replay.')
            continue

        if time_utc in scraper_data:
            logger.info(f'Game already {replay} in the scraper data, skip the replay.')
            continue

        progress_bar = tqdm(
            total=game_data['Duration'],
            desc=f'Replay {i + 1}/{len(replays)}...',
            delay=1, leave=True, ascii=True
        )

        if platform.system() == "Windows":
            progress_bar.close()

        dest_dir_path.joinpath(race).mkdir(parents=True, exist_ok=True)
        dataset_path = dest_dir_path.joinpath(race, f'{time_utc}.csv')
        observer = ObserverBot(dataset_path=dataset_path, config_path=conf_path, progress_bar=progress_bar)
        logger.info(f'Starting game {time_utc} as player ID {winner_id}, duration {game_data["Duration"]}')
        sc2.main.run_replay(ai=observer, replay_path=str(replay_path), observed_id=winner_id, realtime=args.realtime)

        scraper_data[str(time_utc)] = game_data
        with open(scraper_data_path, 'w') as file:
            json.dump(scraper_data, file)


if __name__ == "__main__":
    # define arguments
    parser = argparse.ArgumentParser(prog='SC2 Replay Scraper Bot')
    parser.add_argument('replays_path')
    parser.add_argument('-sd', '--scraper_data')
    parser.add_argument('-rt', '--realtime', action='store_true')
    parser.add_argument('-o', '--output')
    parser.add_argument('-c', '--config')

    _args = parser.parse_args()
    _working_dir = Path(__file__).parent

    if platform.system() == "Linux":
        progress_bar_linux()

    run_scraper(_args, _working_dir)
