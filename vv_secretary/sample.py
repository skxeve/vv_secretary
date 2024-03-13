import logging
import random
from typing import List, NoReturn

from .agency import CharaTag, Speaker
from .speech import Speech

logger = logging.getLogger(__name__)


# 適当にサンプル聞きたい時は囁き系やダウナー系をざっくり外したい
def filter_hello_sampling(sp: Speaker) -> bool:
    if CharaTag.QUIET in sp.tags:
        return False
    if CharaTag.DOWNER in sp.tags:
        return False
    return True


def hello_sampling_speakers(
    speaker_list: List[Speaker], text_tail: str, name_filter: str = "", intonation_scale: float = 1.0
) -> NoReturn:
    speech = []
    if name_filter != "":
        sampling_speakers = filter(lambda x: name_filter in x.name, speaker_list)
    else:
        sampling_speakers = filter(filter_hello_sampling, random.sample(speaker_list, len(speaker_list)))
    for item in sampling_speakers:
        if item.style is not None:
            text = f"はじめまして。ID{item.id}番、{item.name}の{item.style}スタイルです。"
        else:
            text = f"はじめまして。ID{item.id}番、{item.name}です。"
        text += text_tail

        try:
            sp = Speech(text, item.id, intonation_scale)
            sp.prepare()
            speech.append(sp)
            while len(speech) > 0 and speech[0].is_reading:
                sp_top = speech.pop(0)
                sp_top.wait_done()
            logger.debug(speech[0].text)
            speech[0].read()
        except Exception as e:
            logger.exception(f"Catch {e.__class__.__name__} during create wave. text={text}")
    while len(speech) > 0 and speech[0].is_reading:
        sp_top = speech.pop(0)
        sp_top.wait_done()

    logger.info("サンプル挨拶を終了します。")
