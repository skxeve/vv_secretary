import dataclasses
from enum import Enum, auto
from typing import List, NoReturn, Optional

from voicevox_core import METAS


class CharaTag(Enum):
    MALE = auto()
    FEMALE = auto()
    QUIET = auto()
    DOWNER = auto()
    FAV = auto()


@dataclasses.dataclass
class Speaker:
    id: int
    name: str
    style: Optional[str]
    uuid: str
    version: str
    tags: List[CharaTag]

    def asdict(self) -> dict:
        return dataclasses.asdict(self)


male_names = (
    "玄野武宏",  # 11
    "白上虎太郎",  # 12
    "剣崎雌雄",  # 21
    "ちび式じい",  # 42
    "紅桜",  # 51
    "雀松朱司",  # 52
    "麒ヶ島宗麟",  # 53
    "猫使アル",  # 56
    "栗田まろん",  # 67
    "満別花丸",  # 69
    "青山龍星",  # 83
)
female_names = (
    "四国めたん",  # 0
    "ずんだもん",  # 1
    "春日部つむぎ",  # 8
    "波音リツ",  # 9
    "雨晴はう",  # 10
    "冥鳴ひまり",  # 14
    "九州そら",  # 15
    "もち子さん",  # 20
    "WhiteCUL",  # 25
    "後鬼",  # 28
    "No.7",  # 29
    "櫻歌ミコ",  # 43
    "小夜",  # 46
    "ナースロボ",  # 47
    "春歌ナナ",  # 54
    "猫使ビィ",  # 60
    "中国うさぎ",  # 61
    "波音リツ",  # 65
    "あいえるたん",  # 68
    "琴詠ニア",  # 74
)
fav_ids = (
    0,
    1,
    4,
    10,
    15,
    14,
    17,
    23,
    24,
    29,
    31,
    32,
    43,
    46,
    47,
    48,
    53,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    66,
    68,
    72,
    77,
    78,
    79,
    81,
)


def add_chara_tag(speaker_list: List[Speaker]) -> NoReturn:
    # タグ付け
    for s in speaker_list:
        for key in male_names:
            if key in s.name:
                s.tags.append(CharaTag.MALE)
                break
        for key in female_names:
            if key in s.name:
                s.tags.append(CharaTag.FEMALE)
                break
        if s.style in ("ささやき", "囁き", "内緒話", "ヒソヒソ"):
            s.tags.append(CharaTag.QUIET)
        if s.style in ("びえーん", "なみだめ", "こわがり", "不機嫌", "ヘロヘロ"):
            s.tags.append(CharaTag.DOWNER)
        if s.id in fav_ids:
            s.tags.append(CharaTag.FAV)


def get_all_speaker_list() -> List[Speaker]:
    speaker_list = []
    for mt in METAS:
        if len(mt.styles) == 1:
            speaker_list.append(Speaker(mt.styles[0].id, mt.name, None, mt.speaker_uuid, mt.version, []))
        else:
            for stl in mt.styles:
                # METASにはデータがあるけどモデルをロードしようとするとエラーになるのでリストから消しておく
                if stl.id >= 3000:
                    continue
                speaker_list.append(Speaker(stl.id, mt.name, stl.name, mt.speaker_uuid, mt.version, []))
    add_chara_tag(speaker_list)

    return speaker_list


def get_metas():
    return METAS
