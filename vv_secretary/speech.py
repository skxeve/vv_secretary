import hashlib
import logging
import os
from pathlib import Path
from typing import NoReturn, Optional

import simpleaudio as sa

from voicevox_core import VoicevoxCore

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

path_open_jtalk = Path(os.path.dirname(__file__) + "/../voicevox_core/open_jtalk_dic_utf_8-1.11")
core = VoicevoxCore(open_jtalk_dict_dir=path_open_jtalk.resolve())


class Speech:
    def __init__(self, text: str, speaker_id: int, intonation_scale: float = 1.0, wav_dir_path: Optional[str] = None):
        self.text = text
        self.speaker_id = speaker_id
        self.intonation_scale = intonation_scale
        if wav_dir_path is not None:
            self._wav_dir_path = wav_dir_path
        else:
            self._wav_dir_path = "/tmp/"
        self._wave = None
        self._play = None

    @property
    def voice_text(self) -> str:
        return self._replace_text_for_voice(self.text)

    @staticmethod
    def _replace_text_for_voice(text: str) -> str:
        # TODO 本当はjtalk_dictでやるべきな気がする
        return (
            text.replace("No.7", "No.セブン")
            .replace("WhiteCUL", "ホワイトカル")
            .replace("ver.", "バージョン")
            .replace("雨晴はう", "アメハレハウ")
            .replace("小夜/SAYO", "小夜")
            .replace("虎太郎", "小太郎")
            .replace("玄野", "黒野")
            .replace("雌雄", "メスオ")
            .replace("楽々", "ラクラク")
            .replace("雀松朱司", "わかまつあかし")
            .replace("麒ヶ島宗麟", "きがしまそうりん")
            .replace("猫使", "猫ツカ")
        )

    def prepare(self) -> NoReturn:
        p = self._create_wave_file()
        self._wave = sa.WaveObject.from_wave_file(str(p))

    def read(self, is_wait_done: bool = False) -> sa.PlayObject:
        if self._wave is None:
            self.prepare()
        self._play = self._wave.play()
        if is_wait_done:
            self.wait_done()
        return self._play

    @property
    def is_reading(self) -> bool:
        if self._play is None:
            return False
        return self._play.is_playing()

    def wait_done(self) -> NoReturn:
        if self._play is None:
            return
        self._play.wait_done()

    def stop(self) -> NoReturn:
        if self._play is None:
            return
        self._play.stop()

    def _create_wave_file(self, is_overwrite: bool = False, use_tts: bool = False) -> Path:
        file_name = (
            "vv_"
            + str(self.speaker_id)
            + "_"
            + str(self.intonation_scale).replace(".", "")
            + "_"
            + hashlib.sha256((self.voice_text + str(int(use_tts))).encode()).hexdigest()
        )
        file_path = Path(f"{self._wav_dir_path}/{file_name}.wav")
        if self.text == self.voice_text:
            logger.info(
                f"create_wave_file speaker_id={self.speaker_id} intonation_scale={self.intonation_scale}"
                f" text={self.text}"
            )
        else:
            logger.info(
                f"create_wave_file speaker_id={self.speaker_id} intonation_scale={self.intonation_scale}"
                f" text={self.text} voice_text={self.voice_text}"
            )
        if not file_path.exists() or is_overwrite:
            if not core.is_model_loaded(self.speaker_id):
                core.load_model(self.speaker_id)
            if use_tts:
                wave_bytes = core.tts(self.voice_text, self.speaker_id)
            else:
                a_query = core.audio_query(self.voice_text, self.speaker_id)
                a_query.intonation_scale = self.intonation_scale
                wave_bytes = core.synthesis(a_query, self.speaker_id)
            file_path.write_bytes(wave_bytes)
        return file_path
