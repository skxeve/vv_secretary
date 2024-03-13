import random
from datetime import datetime
from typing import Callable, List, NoReturn, Optional, Tuple

from .agency import CharaTag, Speaker, get_all_speaker_list
from .speech import Speech


def _get_tag_speaker(tags: List[CharaTag], additional_filter: Optional[Callable] = None) -> Speaker:
    speaker_list = get_all_speaker_list()
    for tag in tags:
        speaker_list = list(filter(lambda s: tag in s.tags, speaker_list))
    if additional_filter is not None:
        speaker_list = list(filter(additional_filter, speaker_list))
    return random.choice(speaker_list)


def get_fav_speaker() -> Speaker:
    return _get_tag_speaker([CharaTag.FAV])


def get_fav_male_speaker() -> Speaker:
    return _get_tag_speaker([CharaTag.FAV, CharaTag.MALE])


def get_fav_female_speaker() -> Speaker:
    return _get_tag_speaker([CharaTag.FAV, CharaTag.FEMALE])


def get_quiet_speaker() -> Speaker:
    return _get_tag_speaker([CharaTag.QUIET])


def _get_signal_text(now: datetime) -> str:
    if now.minute == 0:
        return f"現在、{now.hour}時ちょうどです。"
    else:
        return f"現在、{now.hour}時{now.minute}分です。"


def _get_default_time_signal_data(now: datetime) -> Tuple[str, Optional[Speaker]]:
    if now.hour >= 22 or now.hour == 0:
        return ("そろそろ寝る準備をしましょう。", None)
    elif now.hour <= 3:
        speaker = get_fav_female_speaker()
        if CharaTag.MALE in speaker.tags:
            return ("こんな時間まで起きていて大丈夫か？", speaker)
        else:
            return ("こんな時間まで起きていて大丈夫ですか？", speaker)
    elif now.hour <= 6:
        speaker = get_fav_female_speaker()
        return ("今日は随分と早起きですね。", speaker)
    elif now.hour <= 8:
        speaker = get_fav_female_speaker()
        return ("おはようございます。良い一日をお過ごしください。", speaker)
    else:
        speaker = get_fav_speaker()
        if CharaTag.MALE in speaker.tags:
            return ("適度に休憩を取るんだぞ。", speaker)
        elif CharaTag.FEMALE in speaker.tags:
            return ("適度に休憩を取るようにしてくださいね。", speaker)
        else:
            return ("適当に休憩を取ってください。", speaker)


def hey_secretary(intonation_scale: float, option: str) -> NoReturn:
    now = datetime.now()
    speaker = None
    if option == "":
        (add_text, speaker) = _get_default_time_signal_data(now)
        text = _get_signal_text(now) + add_text
    elif option == "eyedrop":
        speaker = get_fav_female_speaker()
        text = _get_signal_text(now) + "目薬をさしてください。"

    if speaker is None:
        speaker = get_fav_speaker()
    sp = Speech(text, speaker.id, intonation_scale)
    sp.read(True)
