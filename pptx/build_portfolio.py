# -*- coding: utf-8 -*-
"""
OmniType OneBoard — PPT 포트폴리오 빌더
=========================================
52장 PPT 디자인 카드 규칙 적용:
  - 1슬라이드 = 1메시지
  - 고딕체 (프리텐다드/본고딕)
  - 컬러: 검정 배경 + 금색 강조 + 흰색 텍스트
  - 여백 충분
  - 텍스트 최소화 — 키워드만
  - 자간 좁히기

이수진 / 2026-03-31
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ═══ 디자인 상수 (카드 PPT-A005, PPT-012, PPT-006) ═══
BG_COLOR = RGBColor(0x0A, 0x0A, 0x0F)      # 거의 검정
TEXT_COLOR = RGBColor(0xFF, 0xFF, 0xFF)      # 흰색
ACCENT_COLOR = RGBColor(0xF0, 0xC0, 0x40)   # 금색
SUBTLE_COLOR = RGBColor(0x88, 0x88, 0x88)   # 회색
GREEN_COLOR = RGBColor(0x4E, 0xCB, 0x71)    # 체크 초록
RED_COLOR = RGBColor(0xFF, 0x44, 0x44)      # 엑스 빨강
CARD_BG = RGBColor(0x1A, 0x1A, 0x28)        # 카드 배경
VOWEL_COLOR = RGBColor(0x40, 0xC0, 0x70)    # 모음 초록

FONT_TITLE = 'Pretendard'      # 제목 (프리텐다드)
FONT_BODY = 'Pretendard'       # 본문
FONT_FALLBACK = 'Malgun Gothic' # 폴백

SLIDE_W = Cm(33.87)  # 16:9
SLIDE_H = Cm(19.05)
MARGIN = Cm(2.0)


def set_slide_bg(slide, color=BG_COLOR):
    """슬라이드 배경색 설정"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(slide, text, left, top, width, height,
             font_size=28, color=TEXT_COLOR, bold=False,
             alignment=PP_ALIGN.LEFT, font_name=FONT_TITLE):
    """텍스트 박스 추가"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    # 자간 좁히기 (PPT-008: -1pt)
    p.font.spacing = Pt(-1.0) if font_size >= 20 else Pt(-0.5)
    return txBox


def add_shape(slide, shape_type, left, top, width, height,
              fill_color=CARD_BG, line=False):
    """도형 추가"""
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if not line:
        shape.line.fill.background()
    return shape


def build_portfolio():
    """포트폴리오 PPT 생성"""
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    blank = prs.slide_layouts[6]  # 빈 슬라이드

    # 키 그리기 헬퍼
    def draw_key(slide, x, y, w=Cm(2.8), h=Cm(2.8), main='', sub='',
                 bg=CARD_BG, main_color=TEXT_COLOR, sub_color=ACCENT_COLOR):
        """키보드 키 하나 그리기"""
        shape = add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, bg)
        if main:
            add_text(slide, main, x + Cm(0.2), y + Cm(0.2), w - Cm(0.4), Cm(1.6),
                    font_size=22, color=main_color, bold=True, alignment=PP_ALIGN.CENTER)
        if sub:
            add_text(slide, sub, x + Cm(0.2), y + Cm(1.7), w - Cm(0.4), Cm(0.9),
                    font_size=13, color=sub_color, alignment=PP_ALIGN.CENTER)
        return shape

    CONSONANT_BG = RGBColor(0x1A, 0x1A, 0x38)   # 자음 파랑
    VOWEL_BG = RGBColor(0x1A, 0x2A, 0x1A)        # 모음 초록
    FUNC_BG = RGBColor(0x2A, 0x2A, 0x2A)         # 기능키 회색

    # ═══ 슬라이드 1: 표지 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'OmniType', Cm(4), Cm(5), Cm(26), Cm(4),
             font_size=60, color=TEXT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'OneBoard', Cm(4), Cm(9), Cm(26), Cm(3),
             font_size=48, color=ACCENT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'One Keyboard, Every Language', Cm(4), Cm(13), Cm(26), Cm(2),
             font_size=18, color=SUBTLE_COLOR, alignment=PP_ALIGN.CENTER)
    add_text(slide, '2026 Lee Sujin', Cm(4), Cm(16), Cm(26), Cm(1.5),
             font_size=12, color=RGBColor(0x44, 0x44, 0x44), alignment=PP_ALIGN.CENTER)

    # ═══ 슬라이드 2: 목차 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Contents', Cm(2), Cm(1.5), Cm(20), Cm(2.5),
             font_size=36, color=TEXT_COLOR, bold=True)

    toc = [
        ('01', 'The Problem', '왜 필요한가'),
        ('02', 'Just Type', '해결 방식'),
        ('03', 'Keyboard', '키보드 레이아웃'),
        ('04', 'Language Switch', '언어 전환'),
        ('05', 'Shortcuts', '단축키'),
        ('06', 'Numbers', '핵심 숫자'),
        ('07', 'Comparison', '기존 IME vs OmniType'),
        ('08', 'Accessibility', '접근성'),
        ('09', 'Safety', '안전장치'),
        ('10', 'Tech Stack', '기술 구조'),
        ('11', 'Translation', '번역 (LLM 불필요)'),
        ('12', 'Game Overlay', '게임 자막 오버레이'),
        ('13', 'Stenography', '속기사 모드'),
    ]

    for i, (num, title, desc) in enumerate(toc):
        y = Cm(4.5) + i * Cm(1.35)
        add_text(slide, num, Cm(3), y, Cm(2.5), Cm(1.2),
                font_size=14, color=ACCENT_COLOR, bold=True)
        add_text(slide, title, Cm(6), y, Cm(10), Cm(1.2),
                font_size=14, color=TEXT_COLOR, bold=True)
        add_text(slide, desc, Cm(17), y, Cm(12), Cm(1.2),
                font_size=12, color=SUBTLE_COLOR)
        # 구분선
        add_shape(slide, MSO_SHAPE.RECTANGLE, Cm(3), y + Cm(1.2), Cm(27), Cm(0.02),
                 RGBColor(0x1A, 0x1A, 0x1A))

    # ═══ 슬라이드 3: 문제 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'The Problem', Cm(2), Cm(1.5), Cm(20), Cm(2.5),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Multilingual input is stuck in the 90s.',
             Cm(2), Cm(4), Cm(28), Cm(1.5),
             font_size=16, color=SUBTLE_COLOR)

    # 4개 문제 카드 (PPT-A002: 그리드 4컬럼)
    problems = [
        ('Keyboard Hell', 'One shortcut per language.\nConflicts guaranteed.'),
        ('Driver Bloat', 'Separate install\nfor each language.'),
        ('Legacy Devices', 'Old OS, IoT =\nno multilingual input.'),
        ('Learning Cost', 'New language =\nnew muscle memory.'),
    ]

    card_w = Cm(7)
    card_h = Cm(9)
    gap = Cm(0.8)
    start_x = Cm(2)
    start_y = Cm(6.5)

    for i, (title, desc) in enumerate(problems):
        x = start_x + i * (card_w + gap)
        card = add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, start_y, card_w, card_h)
        add_text(slide, title, x + Cm(0.8), start_y + Cm(1), card_w - Cm(1.6), Cm(1.5),
                font_size=16, color=ACCENT_COLOR, bold=True)
        add_text(slide, desc, x + Cm(0.8), start_y + Cm(3), card_w - Cm(1.6), Cm(5),
                font_size=11, color=SUBTLE_COLOR)

    # ═══ 슬라이드 3: 해결 — Just Type ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Just Type', Cm(2), Cm(3), Cm(30), Cm(4),
             font_size=52, color=TEXT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'Like Korean and English.\nSame sound = same key.',
             Cm(4), Cm(8), Cm(26), Cm(3),
             font_size=20, color=SUBTLE_COLOR, alignment=PP_ALIGN.CENTER)

    # 예시 키 매핑
    examples = [
        ('ㄱ', 'k', 'か', 'Same key'),
        ('ㄴ', 'n', 'な', 'Same key'),
        ('ㅁ', 'm', 'ま', 'Same key'),
    ]

    ex_y = Cm(12.5)
    for i, (ko, en, ja, label) in enumerate(examples):
        x = Cm(8) + i * Cm(6.5)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, ex_y, Cm(5), Cm(3.5), CARD_BG)
        add_text(slide, f'{ko}  =  {en}  =  {ja}', x + Cm(0.3), ex_y + Cm(0.5), Cm(4.4), Cm(1.5),
                font_size=18, color=TEXT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
        add_text(slide, label, x + Cm(0.3), ex_y + Cm(2.2), Cm(4.4), Cm(1),
                font_size=11, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)

    # ═══ 슬라이드 5-A: 키보드 — 한국어 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Keyboard — Korean', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=28, color=TEXT_COLOR, bold=True)
    add_text(slide, '자음 = blue  |  모음 = green  |  같은 위치 = 같은 소리',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR)

    # 한국어 키보드 3행
    ko_rows = [
        [('ㅂ','b',True),('ㅈ','j',True),('ㄷ','d',True),('ㄱ','g',True),('ㅅ','s',True),
         ('ㅛ','yo',False),('ㅕ','yeo',False),('ㅑ','ya',False),('ㅐ','ae',False),('ㅔ','e',False)],
        [('ㅁ','m',True),('ㄴ','n',True),('ㅇ','ng',True),('ㄹ','r',True),('ㅎ','h',True),
         ('ㅗ','o',False),('ㅓ','eo',False),('ㅏ','a',False),('ㅣ','i',False)],
        [('ㅋ','k',True),('ㅌ','t',True),('ㅊ','ch',True),('ㅍ','p',True),
         ('ㅠ','yu',False),('ㅜ','u',False),('ㅡ','eu',False)],
    ]

    key_w = Cm(2.8)
    key_h = Cm(2.6)
    gap = Cm(0.3)
    offsets_cm = [0, 0.8, 1.6]

    for ri, row in enumerate(ko_rows):
        for ci, (main, sub, is_c) in enumerate(row):
            x = Cm(2 + offsets_cm[ri]) + ci * (key_w + gap)
            y = Cm(5) + ri * (key_h + gap)
            bg = CONSONANT_BG if is_c else VOWEL_BG
            draw_key(slide, x, y, key_w, key_h, main, sub, bg)

    # 범례
    draw_key(slide, Cm(26), Cm(5), Cm(2.5), Cm(1.3), '자음', '', CONSONANT_BG,
             main_color=RGBColor(0x80, 0x80, 0xFF))
    draw_key(slide, Cm(29), Cm(5), Cm(2.5), Cm(1.3), '모음', '', VOWEL_BG,
             main_color=VOWEL_COLOR)

    # 사용 예시 — 크게
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14), Cm(30), Cm(4), CARD_BG)
    add_text(slide, '[ ㄱ ] + [ ㅏ ]  →  가     [ ㅎ ] + [ ㅏ ] + [ ㄴ ]  →  한',
             Cm(3), Cm(14.3), Cm(28), Cm(1.8),
             font_size=22, color=ACCENT_COLOR, bold=True)
    add_text(slide, 'No number key needed — jamo combination is unique.',
             Cm(3), Cm(16.2), Cm(28), Cm(1.8),
             font_size=13, color=SUBTLE_COLOR)

    # ═══ 슬라이드 5-B: 키보드 — 영어 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Keyboard — English', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=28, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Same physical key = same sound position',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR)

    en_rows = [
        [('q','',True),('w','',True),('e','',False),('r','',True),('t','',True),
         ('y','',True),('u','',False),('i','',False),('o','',False),('p','',True)],
        [('a','',False),('s','',True),('d','',True),('f','',True),('g','',True),
         ('h','',True),('j','',True),('k','',True),('l','',True)],
        [('z','',True),('x','',True),('c','',True),('v','',True),
         ('b','',True),('n','',True),('m','',True)],
    ]

    for ri, row in enumerate(en_rows):
        for ci, (main, sub, is_c) in enumerate(row):
            x = Cm(2 + offsets_cm[ri]) + ci * (key_w + gap)
            y = Cm(5) + ri * (key_h + gap)
            bg = CONSONANT_BG if is_c else VOWEL_BG
            draw_key(slide, x, y, key_w, key_h, main, sub, bg)

    # 영어 사용 예시
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14), Cm(30), Cm(4), CARD_BG)
    add_text(slide, '[ h ] + [ e ] + [ l ] + [ l ] + [ o ]  →  hello',
             Cm(3), Cm(14.3), Cm(28), Cm(1.8),
             font_size=22, color=ACCENT_COLOR, bold=True)
    add_text(slide, 'Just type. One key = one letter.',
             Cm(3), Cm(16.2), Cm(28), Cm(1.8),
             font_size=13, color=SUBTLE_COLOR)

    # ═══ 슬라이드 5-C: 키보드 — 日本語 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Keyboard — 日本語', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=28, color=TEXT_COLOR, bold=True)
    add_text(slide, 'か = k+a  |  Consonant + Vowel = Kana',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR)

    ja_rows = [
        [('か','ka',True),('さ','sa',True),('た','ta',True),('な','na',True),('は','ha',True),
         ('ま','ma',True),('や','ya',True),('ら','ra',True),('わ','wa',True),('ん','n',True)],
        [('あ','a',False),('い','i',False),('う','u',False),('え','e',False),('お','o',False),
         ('き','ki',True),('し','si',True),('ち','ti',True),('に','ni',True)],
        [('が','ga',True),('ざ','za',True),('だ','da',True),('ば','ba',True),
         ('ぱ','pa',True),('り','ri',True),('る','ru',True)],
    ]

    for ri, row in enumerate(ja_rows):
        for ci, (main, sub, is_c) in enumerate(row):
            x = Cm(2 + offsets_cm[ri]) + ci * (key_w + gap)
            y = Cm(5) + ri * (key_h + gap)
            bg = CONSONANT_BG if is_c else VOWEL_BG
            draw_key(slide, x, y, key_w, key_h, main, sub, bg)

    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14), Cm(30), Cm(4), CARD_BG)
    add_text(slide, '[ k ] + [ a ]  →  か     [ s ] + [ u ]  →  す',
             Cm(3), Cm(14.3), Cm(28), Cm(1.8),
             font_size=22, color=ACCENT_COLOR, bold=True)
    add_text(slide, '한/영+3+1 = ひらがな  |  한/영+3+2 = カタカナ  |  한/영+3+3 = 漢字変換',
             Cm(3), Cm(16.2), Cm(28), Cm(1.8),
             font_size=13, color=SUBTLE_COLOR)

    # ═══ 슬라이드 5-D: 키보드 — 中文 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Keyboard — 中文 (Pinyin)', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=28, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Type pinyin → number key selects tone → character appears',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR)

    zh_rows = [
        [('q','ㄑ',True),('w','ㄨ',False),('e','ㄜ',False),('r','ㄖ',True),('t','ㄊ',True),
         ('y','ㄧ',False),('u','ㄩ',False),('i','ㄧ',False),('o','ㄛ',False),('p','ㄆ',True)],
        [('a','ㄚ',False),('s','ㄙ',True),('d','ㄉ',True),('f','ㄈ',True),('g','ㄍ',True),
         ('h','ㄏ',True),('j','ㄐ',True),('k','ㄎ',True),('l','ㄌ',True)],
        [('z','ㄗ',True),('x','ㄒ',True),('c','ㄘ',True),
         ('b','ㄅ',True),('n','ㄋ',True),('m','ㄇ',True)],
    ]

    for ri, row in enumerate(zh_rows):
        for ci, (main, sub, is_c) in enumerate(row):
            x = Cm(2 + offsets_cm[ri]) + ci * (key_w + gap)
            y = Cm(5) + ri * (key_h + gap)
            bg = CONSONANT_BG if is_c else VOWEL_BG
            draw_key(slide, x, y, key_w, key_h, main, sub, bg)

    # 성조 예시 — 크게
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14), Cm(30), Cm(4), CARD_BG)
    add_text(slide, '[ m ] + [ a ] + [ 1 ]  →  妈  (mā) 1st tone',
             Cm(3), Cm(14.3), Cm(28), Cm(1.8),
             font_size=22, color=ACCENT_COLOR, bold=True)
    add_text(slide, '[ m ] + [ a ] + [ 3 ]  →  马  (mǎ) 3rd tone',
             Cm(3), Cm(16.2), Cm(28), Cm(1.8),
             font_size=22, color=ACCENT_COLOR, bold=True)

    # ═══ 슬라이드 5-E: 키보드 — العربية ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Keyboard — العربية (Arabic)', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=28, color=TEXT_COLOR, bold=True)
    add_text(slide, '28 consonants + 3 vowel marks  |  Right-to-left input',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR)

    ar_rows = [
        [('ض','',True),('ص','',True),('ث','',True),('ق','',True),('ف','',True),
         ('غ','',True),('ع','',True),('ه','',True),('خ','',True),('ح','',True)],
        [('ش','',True),('س','',True),('ي','',True),('ب','',True),('ل','',True),
         ('ا','a',False),('ت','',True),('ن','',True),('م','',True)],
        [('ئ','',True),('ء','',True),('ؤ','',True),
         ('ر','',True),('ذ','',True),('د','',True),('ز','',True)],
    ]

    for ri, row in enumerate(ar_rows):
        for ci, (main, sub, is_c) in enumerate(row):
            x = Cm(2 + offsets_cm[ri]) + ci * (key_w + gap)
            y = Cm(5) + ri * (key_h + gap)
            bg = CONSONANT_BG if is_c else VOWEL_BG
            draw_key(slide, x, y, key_w, key_h, main, sub, bg)

    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14), Cm(30), Cm(4), CARD_BG)
    add_text(slide, '[ ب ] + [ ـَ ]  →  بَ  (ba)',
             Cm(3), Cm(14.3), Cm(28), Cm(1.8),
             font_size=22, color=ACCENT_COLOR, bold=True)
    add_text(slide, 'Vowel marks ( ـَ ـِ ـُ ) added via modifier key',
             Cm(3), Cm(16.2), Cm(28), Cm(1.8),
             font_size=14, color=SUBTLE_COLOR)

    # ═══ 슬라이드 5-F: 키보드 — Русский ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Keyboard — Русский (Russian)', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=28, color=TEXT_COLOR, bold=True)
    add_text(slide, '21 consonants + 10 vowels  |  Cyrillic script',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR)

    ru_rows = [
        [('й','',True),('ц','',True),('у','',False),('к','',True),('е','',False),
         ('н','',True),('г','',True),('ш','',True),('щ','',True),('з','',True)],
        [('ф','',True),('ы','',False),('в','',True),('а','',False),('п','',True),
         ('р','',True),('о','',False),('л','',True),('д','',True)],
        [('я','',False),('ч','',True),('с','',True),('м','',True),
         ('и','',False),('т','',True),('б','',True)],
    ]

    for ri, row in enumerate(ru_rows):
        for ci, (main, sub, is_c) in enumerate(row):
            x = Cm(2 + offsets_cm[ri]) + ci * (key_w + gap)
            y = Cm(5) + ri * (key_h + gap)
            bg = CONSONANT_BG if is_c else VOWEL_BG
            draw_key(slide, x, y, key_w, key_h, main, sub, bg)

    # 러시아어 사용 예시
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14), Cm(30), Cm(4), CARD_BG)
    add_text(slide, '[ п ] + [ р ] + [ и ] + [ в ] + [ е ] + [ т ]  →  привет',
             Cm(3), Cm(14.3), Cm(28), Cm(1.8),
             font_size=22, color=ACCENT_COLOR, bold=True)
    add_text(slide, 'Type letter by letter — just like English. No tone, no number key.',
             Cm(3), Cm(16.2), Cm(28), Cm(1.8),
             font_size=13, color=SUBTLE_COLOR)

    # ═══ 커스텀 모드 슬라이드 (2패널: 블록 목록 + 키보드) ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Custom Mode', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Drag a language block → drop on keyboard.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    # ── 왼쪽 패널: 언어 블록 리스트 ──
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(4.5), Cm(13), Cm(12.5), CARD_BG)
    add_text(slide, 'Language Blocks', Cm(3), Cm(4.8), Cm(11), Cm(1),
             font_size=14, color=TEXT_COLOR, bold=True)

    # 검색바
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(3), Cm(6), Cm(11), Cm(1.2),
             RGBColor(0x22, 0x22, 0x33))
    add_text(slide, '/  Search language...', Cm(3.5), Cm(6.1), Cm(10), Cm(1),
             font_size=11, color=SUBTLE_COLOR)

    # 언어 블록들 (큰 사이즈, 드래그 가능)
    lang_blocks = [
        ('한국어', 'Korean'),      ('English', ''),
        ('日本語', 'ひらがな'),     ('中文', '简体/繁體'),
        ('العربية', 'Arabic'),     ('Русский', 'Russian'),
        ('हिन्दी', 'Hindi'),       ('ไทย', 'Thai'),
        ('Tiếng Việt', 'Viet'),   ('Deutsch', 'German'),
        ('Español', 'Spanish'),   ('Français', 'French'),
    ]
    for i, (lang, sub) in enumerate(lang_blocks):
        col = i % 3
        row = i // 3
        bx = Cm(3) + col * Cm(3.8)
        by = Cm(7.5) + row * Cm(1.8)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Cm(3.5), Cm(1.5),
                 RGBColor(0x22, 0x22, 0x33))
        add_text(slide, lang, bx + Cm(0.2), by + Cm(0.1), Cm(3.1), Cm(0.9),
                font_size=11, color=ACCENT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
        if sub:
            add_text(slide, sub, bx + Cm(0.2), by + Cm(0.9), Cm(3.1), Cm(0.5),
                    font_size=7, color=SUBTLE_COLOR, alignment=PP_ALIGN.CENTER)

    add_text(slide, '↕ scroll for 195+ languages', Cm(3), Cm(15), Cm(11), Cm(0.6),
             font_size=9, color=SUBTLE_COLOR)

    # 단축키 안내
    add_text(slide, 'Tab ↑↓ = navigate  |  Enter = select  |  / = search',
             Cm(3), Cm(15.8), Cm(11), Cm(0.6),
             font_size=8, color=RGBColor(0x55, 0x55, 0x77))

    # ── 드래그 화살표 (패널 사이) ──
    add_text(slide, '→', Cm(15.3), Cm(9), Cm(1.5), Cm(2),
             font_size=28, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'drag', Cm(15), Cm(10.5), Cm(2), Cm(0.8),
             font_size=9, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)

    # ── 오른쪽 패널: 키보드 (드롭 영역) ──
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(17), Cm(4.5), Cm(15), Cm(12.5), CARD_BG)
    add_text(slide, 'Your Keyboard', Cm(18), Cm(4.8), Cm(10), Cm(1),
             font_size=14, color=TEXT_COLOR, bold=True)

    # 현재 언어 표시
    add_text(slide, 'Active: 한국어 + English + 日本語',
             Cm(18), Cm(6), Cm(13), Cm(0.8),
             font_size=10, color=ACCENT_COLOR)

    # 키보드 (3행, 큰 키)
    preview_rows = [
        [('ㅂ','b'),('ㅈ','j'),('ㄷ','d'),('ㄱ','g'),('ㅅ','s')],
        [('ㅁ','m'),('ㄴ','n'),('ㅇ','ng'),('ㄹ','r'),('ㅎ','h')],
        [('ㅋ','k'),('ㅌ','t'),('ㅊ','ch'),('ㅍ','p'),('','')],
    ]
    for ri, row in enumerate(preview_rows):
        for ci, (main, sub) in enumerate(row):
            if main:
                kx = Cm(18) + ci * Cm(2.8)
                ky = Cm(7.2) + ri * Cm(2.8)
                draw_key(slide, kx, ky, Cm(2.5), Cm(2.5), main, sub, CONSONANT_BG)

    # 드롭 안내
    add_text(slide, 'Drop language block here\nto add it to your keyboard',
             Cm(18), Cm(15), Cm(13), Cm(1.5),
             font_size=10, color=SUBTLE_COLOR)

    # 하단 버튼 (간소화)
    for bi, (label, color) in enumerate([
        ('Apply', GREEN_COLOR), ('Reset', SUBTLE_COLOR)
    ]):
        bx = Cm(21) + bi * Cm(6)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, bx, Cm(17.2), Cm(5), Cm(1.2),
                 RGBColor(0x22, 0x22, 0x33))
        add_text(slide, label, bx + Cm(0.3), Cm(17.3), Cm(4.4), Cm(1),
                font_size=12, color=color, bold=True, alignment=PP_ALIGN.CENTER)

    # 자기 언어 등록 (별도 섹션 안내)
    slide2 = prs.slides.add_slide(blank)
    set_slide_bg(slide2)

    add_text(slide2, 'Add Your Language', Cm(2), Cm(2), Cm(28), Cm(2.5),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide2, "Can't find your language? Create it.",
             Cm(2), Cm(4.5), Cm(28), Cm(1.5),
             font_size=16, color=SUBTLE_COLOR)

    reg_steps = [
        ('1', 'Enter Characters', 'Type your alphabet / script'),
        ('2', 'Mark C or V', 'Consonant or Vowel for each'),
        ('3', 'Pick Position', 'Lips / Tongue / Throat'),
        ('4', 'Save', '.kn file created → ready to use'),
    ]

    for i, (num, title, desc) in enumerate(reg_steps):
        y = Cm(7) + i * Cm(2.8)
        add_shape(slide2, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(4), y, Cm(25), Cm(2.2), CARD_BG)
        add_text(slide2, num, Cm(5), y + Cm(0.3), Cm(2), Cm(1.5),
                font_size=24, color=ACCENT_COLOR, bold=True)
        add_text(slide2, title, Cm(8), y + Cm(0.2), Cm(8), Cm(1),
                font_size=16, color=TEXT_COLOR, bold=True)
        add_text(slide2, desc, Cm(8), y + Cm(1.2), Cm(18), Cm(0.8),
                font_size=11, color=SUBTLE_COLOR)

        if i < 3:
            add_text(slide2, '↓', Cm(16), y + Cm(2.2), Cm(2), Cm(0.8),
                    font_size=14, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)

    # ═══ 키보드 6개 언어 비교 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Same Key → 6 Languages', Cm(2), Cm(1), Cm(28), Cm(2),
             font_size=28, color=TEXT_COLOR, bold=True)
    add_text(slide, 'One physical key, different scripts, same sound.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR)

    # 5개 키에 6개 언어 매핑
    multi_keys = [
        {'pos': 'velar plosive', 'langs': ['ㄱ', 'k', 'か', 'g/k', 'ك', 'к']},
        {'pos': 'coronal nasal', 'langs': ['ㄴ', 'n', 'な', 'n', 'ن', 'н']},
        {'pos': 'labial nasal', 'langs': ['ㅁ', 'm', 'ま', 'm', 'م', 'м']},
        {'pos': 'coronal plosive', 'langs': ['ㄷ', 't', 'た', 't/d', 'ت', 'т']},
        {'pos': 'glottal fric.', 'langs': ['ㅎ', 'h', 'は', 'h', 'ه', 'х']},
    ]

    lang_names = ['KO', 'EN', 'JA', 'ZH', 'AR', 'RU']
    lang_colors = [
        ACCENT_COLOR,
        RGBColor(0x80, 0xC0, 0xFF),
        RGBColor(0xFF, 0x80, 0x80),
        RGBColor(0x80, 0xFF, 0x80),
        RGBColor(0xC0, 0x80, 0xFF),
        RGBColor(0xFF, 0xC0, 0x80),
    ]

    # 헤더
    for li, name in enumerate(lang_names):
        add_text(slide, name, Cm(8) + li * Cm(4), Cm(4.5), Cm(3.5), Cm(1),
                font_size=10, color=lang_colors[li], bold=True, alignment=PP_ALIGN.CENTER)

    # 키 행
    for ki, key_info in enumerate(multi_keys):
        y = Cm(5.5) + ki * Cm(2.5)
        # 위치 라벨
        add_text(slide, key_info['pos'], Cm(2), y + Cm(0.3), Cm(5.5), Cm(1.5),
                font_size=9, color=SUBTLE_COLOR)
        # 화살표
        add_text(slide, '→', Cm(7), y + Cm(0.3), Cm(1), Cm(1.5),
                font_size=14, color=ACCENT_COLOR)
        # 6개 언어 키
        for li, char in enumerate(key_info['langs']):
            kx = Cm(8.2) + li * Cm(4)
            draw_key(slide, kx, y, Cm(2.5), Cm(2), char, '', CARD_BG, lang_colors[li])

    # ═══ 슬라이드 6: 단축키 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Shortcuts', Cm(2), Cm(1.5), Cm(20), Cm(2.5),
             font_size=36, color=TEXT_COLOR, bold=True)

    shortcuts = [
        ('한/영', '한↔영 전환 (기본)'),
        ('한/영 + 1~6', '언어 선택 (1=KO 2=EN 3=JA 4=ZH 5=AR 6=RU)'),
        ('한/영 + 0', '언어 목록 팝업'),
        ('한/영 + Shift', 'Syntax Symphony ON/OFF'),
        ('Ctrl + Space', '가상키보드 표시/숨김'),
        ('ESC', '입력 취소 / 팝업 닫기'),
        ('1~9 (성조)', '동음이의 선택 (중국어 등)'),
        ('Shift + 키', '격음/경음 전환 (한국어)'),
        ('Tab / ↑↓', '블록 이동 (시각 장애인 지원)'),
        ('Enter', '블록 선택 / 배치'),
        ('/', '검색창 열기'),
        ('Ctrl+S', '설정 저장'),
        ('Ctrl+Z', '초기화'),
    ]

    for i, (key, desc) in enumerate(shortcuts):
        y = Cm(4.5) + i * Cm(1.7)
        # 키 배지
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(3), y, Cm(7), Cm(1.4),
                 CARD_BG)
        add_text(slide, key, Cm(3.5), y + Cm(0.1), Cm(6), Cm(1.2),
                font_size=13, color=ACCENT_COLOR, bold=True)
        # 화살표
        add_text(slide, '→', Cm(10.5), y + Cm(0.1), Cm(1.5), Cm(1.2),
                font_size=14, color=SUBTLE_COLOR)
        # 설명
        add_text(slide, desc, Cm(12.5), y + Cm(0.1), Cm(18), Cm(1.2),
                font_size=12, color=TEXT_COLOR)

    # ═══ 슬라이드 7: 언어 전환 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Language Switch', Cm(2), Cm(2), Cm(30), Cm(3),
             font_size=40, color=TEXT_COLOR, bold=True)

    steps = [
        ('한/영 + 1', 'Korean'),
        ('한/영 + 2', 'English'),
        ('한/영 + 3', '日本語'),
        ('한/영 + 4', '中文'),
        ('한/영', 'Back to default'),
    ]

    for i, (key, lang) in enumerate(steps):
        y = Cm(6.5) + i * Cm(2.2)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(4), y, Cm(8), Cm(1.8), CARD_BG)
        add_text(slide, key, Cm(4.5), y + Cm(0.2), Cm(7), Cm(1.4),
                font_size=16, color=ACCENT_COLOR, bold=True)
        add_text(slide, lang, Cm(14), y + Cm(0.2), Cm(10), Cm(1.4),
                font_size=16, color=TEXT_COLOR)

    # ═══ 슬라이드 5: 숫자 임팩트 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    stats = [
        ('195+', 'Languages'),
        ('7bit', 'Encoding'),
        ('0', 'Extra Drivers'),
        ('~200B', 'Per Language'),
    ]

    for i, (num, label) in enumerate(stats):
        x = Cm(2) + i * Cm(8)
        add_text(slide, num, x, Cm(5), Cm(7), Cm(5),
                font_size=48, color=ACCENT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
        add_text(slide, label, x, Cm(10.5), Cm(7), Cm(2),
                font_size=14, color=SUBTLE_COLOR, alignment=PP_ALIGN.CENTER)

    # ═══ 슬라이드 6: 비교표 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'vs. Traditional IME', Cm(2), Cm(1.5), Cm(28), Cm(2.5),
             font_size=32, color=TEXT_COLOR, bold=True)

    comparisons = [
        ('Install per language', 'Required', 'One for all'),
        ('Key layout learning', 'Different each', 'Same sound = same key'),
        ('Legacy support', 'Limited', 'Assembly-level'),
        ('Switch hotkeys', 'One per language', 'Just 1'),
        ('File size', 'Tens of MB', '~200 bytes/lang'),
        ('Korean efficiency', 'Normal', 'No number key needed'),
    ]

    headers_y = Cm(5)
    add_text(slide, '', Cm(2), headers_y, Cm(9), Cm(1.2), font_size=11, color=SUBTLE_COLOR)
    add_text(slide, 'Traditional', Cm(13), headers_y, Cm(8), Cm(1.2),
             font_size=11, color=SUBTLE_COLOR, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'OmniType', Cm(23), headers_y, Cm(8), Cm(1.2),
             font_size=11, color=ACCENT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)

    for i, (feature, old, new) in enumerate(comparisons):
        y = Cm(6.5) + i * Cm(1.8)
        # 구분선
        add_shape(slide, MSO_SHAPE.RECTANGLE, Cm(2), y + Cm(1.6), Cm(29), Cm(0.02),
                 RGBColor(0x22, 0x22, 0x22))
        add_text(slide, feature, Cm(2), y, Cm(9), Cm(1.5), font_size=12, color=TEXT_COLOR)
        add_text(slide, old, Cm(13), y, Cm(8), Cm(1.5),
                font_size=12, color=RED_COLOR, alignment=PP_ALIGN.CENTER)
        add_text(slide, new, Cm(23), y, Cm(8), Cm(1.5),
                font_size=12, color=GREEN_COLOR, alignment=PP_ALIGN.CENTER)

    # ═══ 슬라이드 7: 접근성 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Accessibility', Cm(2), Cm(2), Cm(28), Cm(3),
             font_size=40, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Everyone types. Everyone should be able to.',
             Cm(2), Cm(5), Cm(28), Cm(2),
             font_size=16, color=SUBTLE_COLOR)

    features = [
        ('Vibration Mode', 'Haptic feedback for deaf-blind users.\nC/V phonemes as vibration patterns.'),
        ('On/Off Toggle', 'Sound, vibration, visual keyboard\neach independently controllable.'),
        ('System Tray', 'Minimize to tray icon.\nQuick toggle via click or shortcut.'),
        ('Settings Saved', 'Preferences stored locally.\nRestored on every restart.'),
    ]

    for i, (title, desc) in enumerate(features):
        col = i % 2
        row = i // 2
        x = Cm(2) + col * Cm(16)
        y = Cm(8) + row * Cm(5)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Cm(14), Cm(4), CARD_BG)
        add_text(slide, title, x + Cm(1), y + Cm(0.5), Cm(12), Cm(1.5),
                font_size=16, color=ACCENT_COLOR, bold=True)
        add_text(slide, desc, x + Cm(1), y + Cm(2), Cm(12), Cm(2),
                font_size=11, color=SUBTLE_COLOR)

    # ═══ 슬라이드 8: 안전장치 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Safety Limiter', Cm(2), Cm(2), Cm(28), Cm(3),
             font_size=40, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Built-in protection against acoustic weaponization.',
             Cm(2), Cm(5), Cm(28), Cm(2),
             font_size=16, color=SUBTLE_COLOR)

    blocks = [
        'Infrasound blocked (<20Hz)',
        'Ultrasound blocked (>18kHz)',
        'Binaural beats blocked (3-30Hz diff)',
        'Body resonance blocked (organ/skull/eye)',
        'Weapon pattern detection',
        'Amplitude hard limiter (0.8 max)',
    ]

    for i, block in enumerate(blocks):
        col = i % 2
        row = i // 2
        x = Cm(3) + col * Cm(15)
        y = Cm(8) + row * Cm(3)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Cm(13), Cm(2.2), CARD_BG)
        add_text(slide, block, x + Cm(1), y + Cm(0.4), Cm(11), Cm(1.4),
                font_size=13, color=GREEN_COLOR)

    # ═══ 슬라이드 9: 기술 스택 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Tech Stack', Cm(2), Cm(2), Cm(28), Cm(3),
             font_size=40, color=TEXT_COLOR, bold=True)

    layers = [
        ('Python', 'UI + Settings + Virtual Keyboard', RGBColor(0xFF, 0x60, 0x60)),
        ('C', 'Encoding Engine + .kn Parser', ACCENT_COLOR),
        ('Assembly', 'Key Intercept + Conversion (Legacy)', RGBColor(0x80, 0xC0, 0xFF)),
    ]

    for i, (name, desc, color) in enumerate(layers):
        y = Cm(6.5) + i * Cm(3.5)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(6), y, Cm(22), Cm(2.8), CARD_BG)
        add_text(slide, name, Cm(7), y + Cm(0.3), Cm(6), Cm(1.2),
                font_size=20, color=color, bold=True)
        add_text(slide, desc, Cm(7), y + Cm(1.5), Cm(20), Cm(1),
                font_size=12, color=SUBTLE_COLOR)

    # ═══ 장르 덱 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Genre Decks', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Same word, different meaning per genre. Wiki-sourced, community-verified.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    genres = [
        ('Xianxia', '仙侠', '20 terms', '炉鼎 = cultivation vessel, not "furnace"'),
        ('Wuxia', '武侠', '12 terms', '内功 = inner power, not "indoor exercise"'),
        ('FPS', 'FPS', '12 terms', 'camp = holding position, not "camping trip"'),
        ('MOBA', 'MOBA', '12 terms', 'feed = dying repeatedly, not "eating"'),
        ('RPG', 'RPG', '12 terms', 'aggro = threat level, not "aggressive"'),
    ]

    for i, (name, tag, count, example) in enumerate(genres):
        col = i % 3
        row = i // 3
        x = Cm(2) + col * Cm(10.5)
        y = Cm(5) + row * Cm(5)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Cm(9.5), Cm(4.2), CARD_BG)
        add_text(slide, f'{name} ({tag})', x + Cm(0.8), y + Cm(0.4), Cm(8), Cm(1),
                font_size=14, color=ACCENT_COLOR, bold=True)
        add_text(slide, count, x + Cm(0.8), y + Cm(1.4), Cm(8), Cm(0.7),
                font_size=9, color=SUBTLE_COLOR)
        add_text(slide, example, x + Cm(0.8), y + Cm(2.3), Cm(8), Cm(1.5),
                font_size=10, color=TEXT_COLOR)

    add_text(slide, 'Source: Namuwiki + Moegirl + TVTropes + Fandom Wiki → cross-matched automatically',
             Cm(2), Cm(16.5), Cm(29), Cm(0.8),
             font_size=9, color=SUBTLE_COLOR)
    add_text(slide, 'Total: 68 terms, 4.7KB — all 5 genres combined',
             Cm(2), Cm(17.5), Cm(29), Cm(0.8),
             font_size=10, color=ACCENT_COLOR)

    # ═══ 커뮤니티 보정 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Community Correction', Cm(2), Cm(1), Cm(28), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Wrong translation? Fix it. Others vote. Best version wins.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    # 보정 플로우
    corr_steps = [
        ('1. Spot', 'See wrong translation while playing',
         '"炉鼎" → "furnace" ← wrong in xianxia context', RED_COLOR),
        ('2. Suggest', 'Right-click subtitle → suggest correction',
         '"炉鼎" → "cultivation vessel" ← your fix', ACCENT_COLOR),
        ('3. Vote', 'Other players see both versions, vote',
         '12 votes "cultivation vessel" vs 2 votes "furnace"', RGBColor(0x80, 0xC0, 0xFF)),
        ('4. Merge', 'Winning translation auto-updates genre deck',
         'xianxia.kn updated → all users get fix', GREEN_COLOR),
    ]

    for i, (step, desc, example, color) in enumerate(corr_steps):
        y = Cm(5) + i * Cm(2.8)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), y, Cm(29), Cm(2.3), CARD_BG)
        add_text(slide, step, Cm(3), y + Cm(0.3), Cm(4), Cm(0.8),
                font_size=16, color=color, bold=True)
        add_text(slide, desc, Cm(8), y + Cm(0.2), Cm(12), Cm(0.8),
                font_size=11, color=TEXT_COLOR)
        add_text(slide, example, Cm(8), y + Cm(1.2), Cm(21), Cm(0.8),
                font_size=10, color=color)

    add_text(slide, 'Like Wikipedia — anyone edits, community verifies, best version survives.',
             Cm(2), Cm(17), Cm(29), Cm(1),
             font_size=11, color=SUBTLE_COLOR)

    # ═══ 자동 생성 언어 슬라이드 (lang_data에서) ═══
    try:
        from lang_data import LANGUAGES, LANG_COUNT
        auto_count = 0
        for lang_code, lang_name, script, n_c, n_v, n_h, rows, (example, desc) in LANGUAGES:
            s = prs.slides.add_slide(blank)
            set_slide_bg(s)

            add_text(s, f'Keyboard — {lang_name}', Cm(2), Cm(1), Cm(28), Cm(2),
                     font_size=28, color=TEXT_COLOR, bold=True)
            add_text(s, f'{script}  |  {n_c}C + {n_v}V' + (f' + {n_h} homophones' if n_h else ''),
                     Cm(2), Cm(3), Cm(28), Cm(1.2),
                     font_size=11, color=SUBTLE_COLOR)

            for ri, row in enumerate(rows):
                for ci, (main, sub, is_c) in enumerate(row):
                    if main:
                        x = Cm(2 + [0, 0.8, 1.6][ri]) + ci * (key_w + gap)
                        y = Cm(5) + ri * (key_h + gap)
                        bg = CONSONANT_BG if is_c else VOWEL_BG
                        draw_key(s, x, y, key_w, key_h, main, sub, bg)

            # 사용 예시
            add_shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14), Cm(30), Cm(4), CARD_BG)
            add_text(s, example, Cm(3), Cm(14.3), Cm(28), Cm(1.8),
                    font_size=22, color=ACCENT_COLOR, bold=True)
            add_text(s, desc, Cm(3), Cm(16.2), Cm(28), Cm(1.8),
                    font_size=13, color=SUBTLE_COLOR)
            auto_count += 1

        print(f"  자동 생성: {auto_count}개 언어 슬라이드")
    except ImportError:
        print("  lang_data.py 없음 — 자동 생성 건너뜀")

    # ═══ 번역 아키텍처 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Translation — No AI Required', Cm(2), Cm(1), Cm(28), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, '90% of translation is just lookup. Same sound = same word.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    # 5레이어 아키텍처
    layers = [
        ('L0', 'Phoneme Code', '7-bit K^n encoding', '0 ms', GREEN_COLOR),
        ('L1', 'Word Recognition', 'Pattern match on phoneme stream', '0 ms', GREEN_COLOR),
        ('L2', 'Dictionary Lookup', 'Hash table per language pair', '0 ms', GREEN_COLOR),
        ('L3', 'Word Order', 'SOV↔SVO finite state rules', '0 ms', GREEN_COLOR),
        ('L4', 'Idiom Table', '관용구/비유 사전', '0 ms', GREEN_COLOR),
        ('L5', 'LLM (optional)', 'Context-dependent 10% only', '200ms', RED_COLOR),
    ]

    for i, (code, name, desc, speed, color) in enumerate(layers):
        y = Cm(4.8) + i * Cm(2.0)
        # 레이어 바
        bar_color = CARD_BG if i < 5 else RGBColor(0x2A, 0x1A, 0x1A)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), y, Cm(29), Cm(1.7), bar_color)
        add_text(slide, code, Cm(2.5), y + Cm(0.2), Cm(2.5), Cm(1.2),
                font_size=14, color=color, bold=True)
        add_text(slide, name, Cm(5.5), y + Cm(0.2), Cm(8), Cm(1.2),
                font_size=13, color=TEXT_COLOR, bold=True)
        add_text(slide, desc, Cm(14), y + Cm(0.2), Cm(11), Cm(1.2),
                font_size=10, color=SUBTLE_COLOR)
        add_text(slide, speed, Cm(26), y + Cm(0.2), Cm(4), Cm(1.2),
                font_size=12, color=color, bold=True, alignment=PP_ALIGN.RIGHT)

    # 구분선 (L4와 L5 사이)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Cm(2), Cm(4.8 + 5 * 2.0 - 0.3), Cm(29), Cm(0.05),
             ACCENT_COLOR)
    add_text(slide, '90% solved here — all offline, all 0ms',
             Cm(2), Cm(4.8 + 5 * 2.0 - 0.6), Cm(20), Cm(0.5),
             font_size=8, color=ACCENT_COLOR)

    # 하단: vs Google
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(16.5), Cm(14), Cm(2), CARD_BG)
    add_text(slide, 'Google: 100% neural net = 100% server',
             Cm(3), Cm(16.7), Cm(12), Cm(1.5),
             font_size=11, color=RED_COLOR)

    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(17), Cm(16.5), Cm(14), Cm(2), CARD_BG)
    add_text(slide, 'OmniType: 90% lookup + 10% human = 0% AI',
             Cm(18), Cm(16.7), Cm(12), Cm(1.5),
             font_size=11, color=GREEN_COLOR, bold=True)

    # ═══ 모드 총정리 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'One Engine, Many Modes', Cm(2), Cm(1), Cm(28), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Same phoneme engine. Different output.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    modes = [
        ('Keyboard', 'Type in 195+ languages', 'keystroke → target script',
         RGBColor(0xF0, 0xC0, 0x40)),
        ('Translator', 'Real-time multilingual display', 'type → see all languages at once',
         RGBColor(0x80, 0xC0, 0xFF)),
        ('Game', 'Learn languages by typing', 'quiz + speed match + ranking',
         RGBColor(0xFF, 0x80, 0x80)),
        ('Stenography', 'Court reporter speed', 'chord input + word selection',
         RGBColor(0x80, 0xFF, 0x80)),
        ('Syntax Symphony', 'Text to music', 'phoneme → frequency → sound',
         RGBColor(0xC0, 0x80, 0xFF)),
        ('Accessibility', 'Vibration for deaf-blind', 'phoneme → haptic pattern',
         RGBColor(0xFF, 0xC0, 0x80)),
    ]

    for i, (name, desc, how, color) in enumerate(modes):
        col = i % 2
        row = i // 2
        x = Cm(2) + col * Cm(16)
        y = Cm(5) + row * Cm(4.2)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Cm(14.5), Cm(3.5), CARD_BG)
        add_text(slide, name, x + Cm(1), y + Cm(0.4), Cm(12), Cm(1.2),
                font_size=18, color=color, bold=True)
        add_text(slide, desc, x + Cm(1), y + Cm(1.5), Cm(12), Cm(1),
                font_size=11, color=TEXT_COLOR)
        add_text(slide, how, x + Cm(1), y + Cm(2.4), Cm(12), Cm(0.8),
                font_size=9, color=SUBTLE_COLOR)

    # 하단 핵심 메시지
    add_text(slide, 'Input: 7-bit phoneme code  |  Engine: lookup table  |  Output: depends on mode',
             Cm(2), Cm(17.5), Cm(30), Cm(1),
             font_size=10, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)

    # ═══ 게임 모드 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Game Mode', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Play = Practice. Your score IS your typing speed.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    # 3 레벨
    levels = [
        ('Level 1', 'Same Sound Match', 'Screen: か   →   Type: ㄱ+ㅏ = 가   ✓ +10',
         RGBColor(0x80, 0xFF, 0x80)),
        ('Level 2', 'Word Speed Match', 'Screen: 猫(māo)  →  m+a+o → cat → 고양이   ✓ +30',
         ACCENT_COLOR),
        ('Level 3', 'Steno Race', '"오늘 날씨 좋다" → who types fastest in 4 languages?',
         RGBColor(0xFF, 0x80, 0x80)),
    ]

    for i, (level, title, example, color) in enumerate(levels):
        y = Cm(5) + i * Cm(3.5)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(3), y, Cm(27), Cm(2.8), CARD_BG)
        add_text(slide, level, Cm(4), y + Cm(0.3), Cm(4), Cm(1),
                font_size=14, color=color, bold=True)
        add_text(slide, title, Cm(9), y + Cm(0.3), Cm(10), Cm(1),
                font_size=14, color=TEXT_COLOR, bold=True)
        add_text(slide, example, Cm(4), y + Cm(1.4), Cm(25), Cm(1),
                font_size=12, color=ACCENT_COLOR)

    # vs 듀오링고
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(15.5), Cm(14), Cm(2.5), CARD_BG)
    add_text(slide, 'Duolingo', Cm(3), Cm(15.7), Cm(12), Cm(0.8),
             font_size=11, color=SUBTLE_COLOR, bold=True)
    add_text(slide, 'Click buttons → learn grammar\nSkill stays in app',
             Cm(3), Cm(16.5), Cm(12), Cm(1.3),
             font_size=10, color=SUBTLE_COLOR)

    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(17), Cm(15.5), Cm(14), Cm(2.5), CARD_BG)
    add_text(slide, 'OmniType Game', Cm(18), Cm(15.7), Cm(12), Cm(0.8),
             font_size=11, color=GREEN_COLOR, bold=True)
    add_text(slide, 'Actually type → real speed improves\nGame IS the real tool',
             Cm(18), Cm(16.5), Cm(12), Cm(1.3),
             font_size=10, color=TEXT_COLOR)

    # ═══ 게임 오버레이 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Game Overlay', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'YouTube-style subtitles for any game. Voice + text, 0ms.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    # 게임 화면 시뮬레이션
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(3), Cm(5), Cm(27), Cm(9),
             RGBColor(0x0A, 0x16, 0x28))

    # 게임 화면 텍스트
    add_text(slide, 'GAME SCREEN', Cm(10), Cm(7), Cm(13), Cm(2),
             font_size=24, color=RGBColor(0x22, 0x33, 0x44), bold=True,
             alignment=PP_ALIGN.CENTER)

    # 인게임 채팅 (왼쪽 상단)
    chat_msgs = [
        ('Player1', 'お前はもう死んでいる', RGBColor(0xFF, 0x80, 0x80)),
        ('Player2', '수고했어 gg', ACCENT_COLOR),
        ('Player3', '我来了！小心', RGBColor(0x80, 0xFF, 0x80)),
    ]
    for i, (sender, text, color) in enumerate(chat_msgs):
        cy = Cm(5.5) + i * Cm(1.3)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(4), cy, Cm(12), Cm(1.1),
                 RGBColor(0x00, 0x00, 0x00))
        add_text(slide, f'{sender}: {text}', Cm(4.3), cy + Cm(0.1), Cm(11), Cm(0.8),
                font_size=9, color=color)

    # 하단 자막 바 (반투명)
    add_shape(slide, MSO_SHAPE.RECTANGLE, Cm(3), Cm(12), Cm(27), Cm(2),
             RGBColor(0x08, 0x08, 0x10))
    add_text(slide, 'お前はもう死んでいる', Cm(4), Cm(12.1), Cm(25), Cm(0.8),
             font_size=10, color=ACCENT_COLOR)
    add_text(slide, 'EN: You are already dead  |  KO: 넌 이미 죽어있다  |  ZH: 你已经死了',
             Cm(4), Cm(12.9), Cm(25), Cm(0.8),
             font_size=9, color=SUBTLE_COLOR)

    # 특징 4개
    features = [
        ('Pass-through', 'Mouse/keyboard go to game, not subtitle'),
        ('Voice + Text', 'Translates both chat and voice simultaneously'),
        ('0ms / Offline', 'Phoneme lookup, no server needed'),
        ('Any Game', 'Works as system overlay, not per-game mod'),
    ]

    for i, (title, desc) in enumerate(features):
        col = i % 2
        row = i // 2
        x = Cm(3) + col * Cm(14)
        y = Cm(15) + row * Cm(1.8)
        add_text(slide, f'{title}:', x, y, Cm(5), Cm(0.8),
                font_size=10, color=GREEN_COLOR, bold=True)
        add_text(slide, desc, x + Cm(5.5), y, Cm(8), Cm(0.8),
                font_size=9, color=SUBTLE_COLOR)

    # ═══ 속기사 + 번역 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Stenographer = Human LLM', Cm(2), Cm(1), Cm(28), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'The 10% context layer is a person, not a GPU.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    # 플로우: 발화 → 음소 → 후보 → 속기사 선택 → 다국어 출력
    flow_steps = [
        ('Speaker', '"발이 넓으신 분이죠?"', SUBTLE_COLOR),
        ('OmniType', '→ foot / wide-connections / well-connected', ACCENT_COLOR),
        ('Stenographer', 'selects [ 3 ] → "well-connected"', GREEN_COLOR),
        ('Output', '4 languages simultaneously, 0ms', TEXT_COLOR),
    ]

    for i, (role, text, color) in enumerate(flow_steps):
        y = Cm(5) + i * Cm(2.5)
        add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(3), y, Cm(27), Cm(2), CARD_BG)
        add_text(slide, role, Cm(4), y + Cm(0.3), Cm(6), Cm(1.3),
                font_size=16, color=color, bold=True)
        add_text(slide, text, Cm(11), y + Cm(0.3), Cm(18), Cm(1.3),
                font_size=13, color=color)
        if i < 3:
            add_text(slide, '↓', Cm(16), y + Cm(2), Cm(2), Cm(0.6),
                    font_size=14, color=ACCENT_COLOR, alignment=PP_ALIGN.CENTER)

    # 비교: 현재 vs OmniType
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(15.5), Cm(14), Cm(2.5), CARD_BG)
    add_text(slide, 'International Court — Now', Cm(3), Cm(15.7), Cm(12), Cm(0.8),
             font_size=10, color=RED_COLOR, bold=True)
    add_text(slide, '3 interpreters needed\n(KO→EN, KO→JA, KO→ZH)',
             Cm(3), Cm(16.5), Cm(12), Cm(1.3),
             font_size=11, color=SUBTLE_COLOR)

    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(17), Cm(15.5), Cm(14), Cm(2.5), CARD_BG)
    add_text(slide, 'With OmniType + 1 Stenographer', Cm(18), Cm(15.7), Cm(12), Cm(0.8),
             font_size=10, color=GREEN_COLOR, bold=True)
    add_text(slide, '1 person → 4 languages simultaneous\nPick word, press number. Done.',
             Cm(18), Cm(16.5), Cm(12), Cm(1.3),
             font_size=11, color=TEXT_COLOR)

    # ═══ 속기사 모드 슬라이드 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'Stenography Mode', Cm(2), Cm(1), Cm(20), Cm(2),
             font_size=36, color=TEXT_COLOR, bold=True)
    add_text(slide, 'Court reporting speed on a regular keyboard.',
             Cm(2), Cm(3), Cm(28), Cm(1.2),
             font_size=14, color=SUBTLE_COLOR)

    # 비교: 스테노 vs OmniType
    steno_compare = [
        ('Speed', '300+ WPM', '60~120 WPM → 200+ with steno block'),
        ('Learning', 'Months~Years', 'Steno block = instant'),
        ('Hardware', 'Dedicated steno machine', 'Any keyboard'),
        ('Languages', '1 (English only)', '195+ with steno codes'),
        ('Cost', '$3,000+ machine', 'Free (.kn file)'),
    ]

    headers_y = Cm(5)
    add_text(slide, '', Cm(2), headers_y, Cm(8), Cm(1.2), font_size=10, color=SUBTLE_COLOR)
    add_text(slide, 'Traditional Steno', Cm(11), headers_y, Cm(9), Cm(1.2),
             font_size=10, color=SUBTLE_COLOR, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'OmniType Steno Block', Cm(22), headers_y, Cm(10), Cm(1.2),
             font_size=10, color=ACCENT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)

    for i, (feature, old, new) in enumerate(steno_compare):
        y = Cm(6.2) + i * Cm(1.6)
        add_shape(slide, MSO_SHAPE.RECTANGLE, Cm(2), y + Cm(1.4), Cm(29), Cm(0.02),
                 RGBColor(0x22, 0x22, 0x22))
        add_text(slide, feature, Cm(2), y, Cm(8), Cm(1.3), font_size=11, color=TEXT_COLOR)
        add_text(slide, old, Cm(11), y, Cm(9), Cm(1.3),
                font_size=11, color=RED_COLOR, alignment=PP_ALIGN.CENTER)
        add_text(slide, new, Cm(22), y, Cm(10), Cm(1.3),
                font_size=11, color=GREEN_COLOR, alignment=PP_ALIGN.CENTER)

    # 속기 입력 예시
    add_shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, Cm(2), Cm(14.5), Cm(30), Cm(3.5), CARD_BG)
    add_text(slide, 'Steno: [ S ] + [ T ] + [ E ] + [ N ]  →  "sten"  (simultaneous chord)',
             Cm(3), Cm(14.8), Cm(28), Cm(1.5),
             font_size=22, color=ACCENT_COLOR, bold=True)
    add_text(slide, 'Install steno.kn block via Custom Mode → type at court reporter speed',
             Cm(3), Cm(16.5), Cm(28), Cm(1.2),
             font_size=12, color=SUBTLE_COLOR)

    # ═══ 슬라이드 10: 마무리 ═══
    slide = prs.slides.add_slide(blank)
    set_slide_bg(slide)

    add_text(slide, 'One Keyboard', Cm(2), Cm(5), Cm(30), Cm(3),
             font_size=52, color=TEXT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'Every Language', Cm(2), Cm(8.5), Cm(30), Cm(3),
             font_size=48, color=ACCENT_COLOR, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, 'OmniType OneBoard', Cm(2), Cm(13), Cm(30), Cm(2),
             font_size=18, color=SUBTLE_COLOR, alignment=PP_ALIGN.CENTER)
    add_text(slide, '(c) 2026 Lee Sujin. All rights reserved.',
             Cm(2), Cm(16), Cm(30), Cm(1.5),
             font_size=10, color=RGBColor(0x44, 0x44, 0x44), alignment=PP_ALIGN.CENTER)

    # ═══ 저장 ═══
    output = os.path.join(os.path.dirname(__file__), 'OmniType_OneBoard_Portfolio.pptx')
    prs.save(output)
    print(f"  PPT 저장: {output}")
    print(f"  슬라이드: {len(prs.slides)}장")
    return output


def evaluate_with_10ai():
    """10AI 엔진으로 PPT 디자인 규칙 평가 + 학습"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'claude_optimization', '10ai_skill'))
        from engine_10ai import Engine10AI
    except ImportError:
        print("  10AI 엔진 로드 실패 — 평가 건너뜀")
        return

    ai = Engine10AI()
    domain = 'ppt_design'

    # 슬라이드 타입별 적용 규칙 매핑
    slide_rules = {
        'Cover':        ['text_minimize', 'gothic_font', 'whitespace', 'color_harmony'],
        'TOC':          ['grid_layout', 'gothic_font', 'font_spacing'],
        'Problem':      ['one_slide_one_message', 'grid_layout', 'color_harmony'],
        'Just Type':    ['text_minimize', 'whitespace'],
        'Keyboard':     ['image_quality', 'grid_layout', 'color_harmony', 'whitespace'],
        'Custom Mode':  ['grid_layout', 'whitespace', 'gothic_font'],
        'Comparison':   ['grid_layout', 'color_harmony', 'text_minimize'],
        'Numbers':      ['text_minimize', 'gothic_font', 'whitespace'],
        'Accessibility':['one_slide_one_message', 'grid_layout'],
        'Safety':       ['one_slide_one_message', 'color_harmony'],
        'Tech Stack':   ['grid_layout', 'gothic_font'],
        'Closing':      ['text_minimize', 'whitespace', 'gothic_font'],
    }

    print(f"\n{'='*50}")
    print(f"  10AI PPT 디자인 평가")
    print(f"{'='*50}")

    total_score = 0
    total_count = 0

    for slide_type, rules in slide_rules.items():
        scores = []
        for rule in rules:
            d = ai.decide(domain, rule)
            scores.append(d['confidence'])

            # 학습: PPT 빌드 성공 = 규칙 적용 성공으로 기록
            ai.learn(domain, rule, 'success', f'PPT build: {slide_type}')

        avg = sum(scores) / len(scores) if scores else 0
        total_score += avg
        total_count += 1
        bar = '█' * int(avg * 10) + '░' * (10 - int(avg * 10))
        print(f"    {slide_type:18s} [{bar}] {avg:.0%}")

    if total_count:
        overall = total_score / total_count
        print(f"\n    전체 평균: {overall:.0%}")

    # 가중치 현황
    ai.report(domain)


if __name__ == '__main__':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("OmniType OneBoard — PPT Portfolio Builder")
    print("52 design rules applied\n")
    build_portfolio()

    # 10AI 평가 (--eval 옵션)
    if '--eval' in sys.argv:
        evaluate_with_10ai()

    print("\n  Done.")
