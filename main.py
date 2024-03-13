import logging
import random
from argparse import ArgumentParser
from enum import Enum
from pprint import pformat
from typing import NoReturn, Tuple

from vv_secretary.agency import get_all_speaker_list, get_metas
from vv_secretary.sample import hello_sampling_speakers
from vv_secretary.secretary import get_fav_speaker, hey_secretary
from vv_secretary.speech import Speech


class Mode(Enum):
    SECRETARY = "secretary"
    SAY = "say"
    HELLO = "hello"
    LIST = "list"


def main() -> NoReturn:
    logging.basicConfig(format="[%(asctime)s] [%(levelname)s] %(module)s:%(lineno)d %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    (mode, option, text, speaker_id, intonation_scale_int) = parse_args()
    logger.debug(f"mode:{mode} option:{option} text:{text} speaker_id:{speaker_id}")

    if speaker_id == -1:
        speaker = get_fav_speaker()
        speaker_id = speaker.id

    if intonation_scale_int == -1:
        if mode == Mode.HELLO:
            intonation_scale_int = 10
        else:
            intonation_scale_int = random.randint(10, 20)

    if mode == Mode.HELLO:
        hello_sampling_speakers(get_all_speaker_list(), text, option, intonation_scale_int / 10)
        exit(0)

    elif mode == Mode.LIST:
        if option == "raw":
            logger.info(pformat(get_metas()))
        else:
            speakers = get_all_speaker_list()
            for s in speakers:
                logger.info(str(s.asdict()))
        exit(0)
    elif mode == Mode.SAY:
        sp = Speech(text, speaker_id, intonation_scale_int / 10)
        sp.read(True)
        exit(0)
    elif mode == Mode.SECRETARY:
        hey_secretary(intonation_scale_int / 10, option)
        exit(0)
    else:
        logger.error(f"Unexpected Mode: {mode}")
        exit(1)


def parse_args() -> Tuple[str, str, str, int]:
    parser = ArgumentParser()
    parser.add_argument(
        "--mode",
        default=Mode.SECRETARY,
        type=Mode,
        help="動作モード（{}）".format(",".join([m.value for m in Mode])),
    )
    parser.add_argument(
        "--option",
        default="",
        type=str,
        help="オプション文字列",
    )
    parser.add_argument(
        "--text",
        default="おはようございます。こんにちは。おやすみなさい。よろしくお願いします。",
        help="読み上げさせたい文章",
    )
    parser.add_argument("--id", default=-1, type=int, help="スピーカーIDを指定")
    parser.add_argument("--intonation_scale", default=-1, type=int, help="0から20を指定")
    args = parser.parse_args()
    return (args.mode, args.option, args.text, args.id, args.intonation_scale)


if __name__ == "__main__":
    main()
