# -*- coding: utf-8 -*-
"""
overlay_bridge.py — Python ↔ C DLL 브릿지
===========================================
번역 엔진(Python) → 공유 메모리 → 오버레이 DLL(C) → 게임 화면

사용법:
  bridge = OverlayBridge()
  bridge.set_subtitle(0, "넌 이미 죽어있다")
  bridge.set_subtitle(1, "You are already dead")
  bridge.set_genre("fps")

이수진 / 2026-03-31
"""

import json
import os
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 장르 덱 경로
DECK_DIR = Path(__file__).parent.parent / 'tools' / 'genre_decks'

# ═══ 공유 메모리 구조 ═══
MAX_SUBTITLE_LEN = 512
MAX_LINES = 4

# 공유 메모리는 DLL 연동 시에만 사용. 데모에서는 순수 Python.
_USE_CTYPES = False  # DLL 연동 시 True로 전환

if _USE_CTYPES:
    import ctypes
    import ctypes.wintypes as wintypes

    class OverlayState(ctypes.Structure):
        _fields_ = [
            ('active', ctypes.c_int),
            ('position', ctypes.c_int),
            ('opacity', ctypes.c_float),
            ('font_size', ctypes.c_int),
            ('line_count', ctypes.c_int),
            ('lines', (ctypes.c_wchar * MAX_SUBTITLE_LEN) * MAX_LINES),
            ('genre', ctypes.c_wchar * 64),
            ('correction_mode', ctypes.c_int),
        ]

# 시뮬레이션/데모용 순수 Python 구조
class OverlayState:
    def __init__(self):
        self.active = 0
        self.position = 0
        self.opacity = 0.75
        self.font_size = 18
        self.line_count = 0
        self.lines = [[''] * MAX_SUBTITLE_LEN for _ in range(MAX_LINES)]
        self.genre = 'general'
        self.correction_mode = 0


class OverlayBridge:
    """Python → 공유 메모리 → C DLL 브릿지"""

    def __init__(self):
        self.shared_mem = None
        self.state = None
        self.genre_deck = {}
        self.word_dict = {}
        self._init_shared_memory()
        self._load_base_dict()

    def _init_shared_memory(self):
        """공유 메모리 열기. 실패 시 시뮬레이션 모드."""
        self.state = OverlayState()
        self.state.active = 1
        self.state.position = 0
        self.state.opacity = 0.75
        self.state.font_size = 18
        print("  시뮬레이션 모드 (DLL 연동 시 공유 메모리 사용)")

    def _load_base_dict(self):
        """기본 단어 사전 로드"""
        self.word_dict = {
            '안녕': {'en': 'hello', 'ja': 'こんにちは', 'zh': '你好'},
            '수고': {'en': 'good game', 'ja': 'お疲れ様', 'zh': '辛苦了'},
            '조심': {'en': 'watch out', 'ja': '気をつけて', 'zh': '小心'},
            '뒤': {'en': 'behind', 'ja': '後ろ', 'zh': '后面'},
            '적': {'en': 'enemy', 'ja': '敵', 'zh': '敌人'},
            '회복': {'en': 'heal', 'ja': '回復', 'zh': '回血'},
            '도망': {'en': 'run', 'ja': '逃げろ', 'zh': '快跑'},
        }

    def load_genre_deck(self, genre):
        """장르 덱 로드"""
        deck_path = DECK_DIR / f'{genre}.json'
        if deck_path.exists():
            with open(deck_path, 'r', encoding='utf-8') as f:
                deck = json.load(f)
            self.genre_deck = {}
            for entry in deck.get('entries', []):
                self.genre_deck[entry['term']] = entry
            self.state.genre = genre
            print(f"  장르 덱 로드: {genre} ({len(self.genre_deck)}개 용어)")
            return True
        else:
            print(f"  장르 덱 없음: {deck_path}")
            return False

    def translate(self, text, target_lang='en'):
        """
        번역: 장르 덱 우선 → 기본 사전 폴백 → 음역

        Args:
            text: 원문
            target_lang: 타겟 언어 코드

        Returns:
            번역 결과
        """
        # 1순위: 장르 덱
        if text in self.genre_deck:
            entry = self.genre_deck[text]
            if target_lang in entry:
                return entry[target_lang]

        # 2순위: 기본 사전
        if text in self.word_dict:
            if target_lang in self.word_dict[text]:
                return self.word_dict[text][target_lang]

        # 3순위: 그대로 반환 (음역은 K^n 엔코더 필요)
        return text

    def set_subtitle(self, line_idx, text):
        """자막 설정"""
        if 0 <= line_idx < MAX_LINES:
            if _USE_CTYPES:
                for i, ch in enumerate(text[:MAX_SUBTITLE_LEN - 1]):
                    self.state.lines[line_idx][i] = ch
                self.state.lines[line_idx][min(len(text), MAX_SUBTITLE_LEN - 1)] = '\0'
            else:
                self.state.lines[line_idx] = list(text) + ['\0']

            if line_idx >= self.state.line_count:
                self.state.line_count = line_idx + 1

    def clear_subtitles(self):
        """자막 초기화"""
        self.state.line_count = 0
        for i in range(MAX_LINES):
            if _USE_CTYPES:
                self.state.lines[i][0] = '\0'
            else:
                self.state.lines[i] = ['\0']

    def process_game_text(self, text, source_lang='auto'):
        """
        게임 텍스트 처리: 원문 + 번역 자막 동시 표시

        Args:
            text: 게임에서 캡처한 텍스트
            source_lang: 원문 언어 (auto=자동 감지)
        """
        if not self.state.active:
            return

        # 원문 표시
        self.set_subtitle(0, text)

        # 다국어 번역 (장르 덱 우선)
        translations = []
        for lang in ['en', 'ko', 'ja', 'zh']:
            tr = self.translate(text, lang)
            if tr != text:  # 번역이 있는 경우만
                lang_names = {'en': 'EN', 'ko': 'KO', 'ja': 'JA', 'zh': 'ZH'}
                translations.append(f"{lang_names[lang]}: {tr}")

        # 번역 자막
        for i, tr in enumerate(translations[:MAX_LINES - 1]):
            self.set_subtitle(i + 1, tr)

    def set_active(self, active):
        self.state.active = 1 if active else 0

    def set_position(self, pos):
        """0=bottom, 1=top"""
        self.state.position = pos


# ═══ 데모 ═══
def demo():
    """오버레이 브릿지 데모"""
    print("=== OmniType Overlay Bridge Demo ===\n")

    bridge = OverlayBridge()

    # 장르 덱 로드
    bridge.load_genre_deck('xianxia')

    # 게임 텍스트 시뮬레이션
    game_texts = [
        'お前はもう死んでいる',
        '炉鼎已被夺走',
        '筑基成功！进入金丹期',
        'Behind you!',
        '수고했어 gg',
        '灵石不够了',
        '天劫来临！',
    ]

    print("--- 게임 텍스트 번역 ---\n")
    for text in game_texts:
        bridge.clear_subtitles()
        bridge.process_game_text(text)

        print(f"  원문: {text}")
        for i in range(bridge.state.line_count):
            if _USE_CTYPES:
                line = ''
                for j in range(MAX_SUBTITLE_LEN):
                    ch = bridge.state.lines[i][j]
                    if ch == '\0': break
                    line += ch
            else:
                chars = bridge.state.lines[i]
                line = ''.join(c for c in chars if c != '\0')
            if line and i > 0:
                print(f"    → {line}")
        print()

    # 장르 덱 우선순위 확인
    print("--- 장르 덱 우선순위 ---")
    print(f"  炉鼎 (xianxia): {bridge.translate('炉鼎', 'ko')}")
    print(f"  筑基 (xianxia): {bridge.translate('筑基', 'en')}")
    print(f"  灵石 (xianxia): {bridge.translate('灵石', 'en')}")
    print(f"  天劫 (xianxia): {bridge.translate('天劫', 'ko')}")


if __name__ == '__main__':
    demo()
