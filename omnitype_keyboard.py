# -*- coding: utf-8 -*-
"""
OmniType OneBoard — 가상키보드 + 언어 전환
============================================
- 가상키보드 팝업 (게임 단축키 스타일)
- 한/영 + 숫자 = 언어 선택
- 한/영 다시 = 한영 복귀
- 시스템 트레이 아이콘 (Syntax Symphony ON/OFF)

의존성: pip install pystray Pillow keyboard

이수진 / 2026-03-31
"""

import tkinter as tk
from tkinter import font as tkfont
import threading
import sys
import os

# ═══════════════════════════════════════════
# 언어 데이터
# ═══════════════════════════════════════════

LANGUAGES = {
    1: {'name': '한국어', 'code': 'ko', 'rows': [
        [('ㅂ','b'),('ㅈ','j'),('ㄷ','d'),('ㄱ','g'),('ㅅ','s'),('ㅛ','yo'),('ㅕ','yeo'),('ㅑ','ya'),('ㅐ','ae'),('ㅔ','e')],
        [('ㅁ','m'),('ㄴ','n'),('ㅇ','ng'),('ㄹ','r'),('ㅎ','h'),('ㅗ','o'),('ㅓ','eo'),('ㅏ','a'),('ㅣ','i')],
        [('ㅋ','k'),('ㅌ','t'),('ㅊ','ch'),('ㅍ','p'),('ㅠ','yu'),('ㅜ','u'),('ㅡ','eu')],
    ]},
    2: {'name': 'English', 'code': 'en', 'rows': [
        [('q',''),('w',''),('e',''),('r',''),('t',''),('y',''),('u',''),('i',''),('o',''),('p','')],
        [('a',''),('s',''),('d',''),('f',''),('g',''),('h',''),('j',''),('k',''),('l','')],
        [('z',''),('x',''),('c',''),('v',''),('b',''),('n',''),('m','')],
    ]},
    3: {'name': '日本語', 'code': 'ja', 'rows': [
        [('か','ka'),('さ','sa'),('た','ta'),('な','na'),('は','ha'),('ま','ma'),('や','ya'),('ら','ra'),('わ','wa'),('ん','n')],
        [('あ','a'),('い','i'),('う','u'),('え','e'),('お','o'),('き','ki'),('し','si'),('ち','ti'),('に','ni')],
        [('が','ga'),('ざ','za'),('だ','da'),('ば','ba'),('ぱ','pa'),('り','ri'),('る','ru')],
    ]},
    4: {'name': '中文', 'code': 'zh', 'rows': [
        [('q','ㄑ'),('w','ㄨ'),('e','ㄜ'),('r','ㄖ'),('t','ㄊ'),('y','ㄧ'),('u','ㄩ'),('i','ㄧ'),('o','ㄛ'),('p','ㄆ')],
        [('a','ㄚ'),('s','ㄙ'),('d','ㄉ'),('f','ㄈ'),('g','ㄍ'),('h','ㄏ'),('j','ㄐ'),('k','ㄎ'),('l','ㄌ')],
        [('z','ㄗ'),('x','ㄒ'),('c','ㄘ'),('b','ㄅ'),('n','ㄋ'),('m','ㄇ')],
    ]},
    5: {'name': 'العربية', 'code': 'ar', 'rows': [
        [('ض',''),('ص',''),('ث',''),('ق',''),('ف',''),('غ',''),('ع',''),('ه',''),('خ',''),('ح','')],
        [('ش',''),('س',''),('ي',''),('ب',''),('ل',''),('ا',''),('ت',''),('ن',''),('م','')],
        [('ئ',''),('ء',''),('ؤ',''),('ر',''),('ذ',''),('د',''),('ز','')],
    ]},
    6: {'name': 'Русский', 'code': 'ru', 'rows': [
        [('й',''),('ц',''),('у',''),('к',''),('е',''),('н',''),('г',''),('ш',''),('щ',''),('з','')],
        [('ф',''),('ы',''),('в',''),('а',''),('п',''),('р',''),('о',''),('л',''),('д','')],
        [('я',''),('ч',''),('с',''),('м',''),('и',''),('т',''),('б','')],
    ]},
}

# 모음 판별 (키보드 하이라이트용)
VOWEL_CHARS = set('aeiouㅏㅓㅗㅜㅡㅣㅐㅔㅑㅕㅛㅠあいうえおاу')


class OmniTypeKeyboard:
    """가상키보드 팝업 — 게임 단축키 스타일"""

    def __init__(self):
        self.current_lang = 1  # 기본: 한국어
        self.root = None
        self.keys = []
        self.visible = True

    def create_window(self):
        """메인 윈도우 생성"""
        self.root = tk.Tk()
        self.root.title('OmniType OneBoard')
        self.root.configure(bg='#0a0a0f')
        self.root.attributes('-alpha', 0.92)  # 약간 투명
        self.root.attributes('-topmost', True)  # 항상 위
        self.root.overrideredirect(False)

        # 크기 고정
        self.root.resizable(False, False)

        # 상단바: 언어 선택
        top_frame = tk.Frame(self.root, bg='#111', padx=8, pady=6)
        top_frame.pack(fill='x')

        title = tk.Label(top_frame, text='OmniType OneBoard',
                        font=('Segoe UI', 10, 'bold'), fg='#f0c040', bg='#111')
        title.pack(side='left')

        # 언어 버튼들
        self.lang_buttons = {}
        btn_frame = tk.Frame(top_frame, bg='#111')
        btn_frame.pack(side='right')

        for num, lang in LANGUAGES.items():
            btn = tk.Button(btn_frame, text=f'{num}:{lang["name"]}',
                          font=('Segoe UI', 8), fg='#888', bg='#1a1a1a',
                          activebackground='#2a2a2a', activeforeground='#f0c040',
                          bd=0, padx=6, pady=2, relief='flat',
                          command=lambda n=num: self.switch_language(n))
            btn.pack(side='left', padx=2)
            self.lang_buttons[num] = btn

        # 안내 문구
        guide = tk.Label(self.root,
                        text='한/영 + 숫자 = 언어 선택  |  한/영 = 한↔영 복귀  |  그냥 치세요',
                        font=('Segoe UI', 8), fg='#444', bg='#0a0a0f', pady=4)
        guide.pack(fill='x')

        # 키보드 영역
        self.kb_frame = tk.Frame(self.root, bg='#0a0a0f', padx=10, pady=8)
        self.kb_frame.pack(fill='both', expand=True)

        # 하단 상태바
        self.status_var = tk.StringVar(value='Korean  |  한/영+숫자로 전환')
        status = tk.Label(self.root, textvariable=self.status_var,
                         font=('Segoe UI', 8), fg='#555', bg='#111', pady=4)
        status.pack(fill='x')

        # 키보드 렌더
        self.render_keyboard()

        # 키보드 단축키
        self.root.bind('<Key>', self.on_key)

        # 최소 크기
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def render_keyboard(self):
        """현재 언어의 키보드 렌더링"""
        # 기존 키 삭제
        for widget in self.kb_frame.winfo_children():
            widget.destroy()
        self.keys = []

        lang = LANGUAGES[self.current_lang]

        # 현재 언어 버튼 하이라이트
        for num, btn in self.lang_buttons.items():
            if num == self.current_lang:
                btn.configure(fg='#f0c040', bg='#2a2a1a')
            else:
                btn.configure(fg='#888', bg='#1a1a1a')

        offsets = [0, 15, 30]  # QWERTY 행별 오프셋
        for row_idx, row in enumerate(lang['rows']):
            row_frame = tk.Frame(self.kb_frame, bg='#0a0a0f')
            row_frame.pack(pady=2)

            # 오프셋
            if row_idx < len(offsets) and offsets[row_idx] > 0:
                spacer = tk.Frame(row_frame, width=offsets[row_idx], bg='#0a0a0f')
                spacer.pack(side='left')

            for main, sub in row:
                is_vowel = main in VOWEL_CHARS

                # 키 프레임
                key_frame = tk.Frame(row_frame, bg='#0a0a0f', padx=1)
                key_frame.pack(side='left')

                # 키 색상
                if is_vowel:
                    bg_color = '#1a2a1a'
                    border_color = '#2a4a2a'
                    hover_color = '#2a4a2a'
                else:
                    bg_color = '#1a1a28'
                    border_color = '#2a2a3a'
                    hover_color = '#2a2a40'

                key_btn = tk.Button(key_frame,
                    width=4, height=2,
                    font=('Segoe UI', 11, 'bold'),
                    fg='#ddd', bg=bg_color,
                    activebackground='#f0c040', activeforeground='#000',
                    bd=1, relief='solid',
                    highlightbackground=border_color,
                    command=lambda m=main: self.on_key_click(m))

                # 메인+서브 텍스트
                if sub:
                    key_btn.configure(text=f'{main}\n{sub}',
                                     font=('Segoe UI', 9, 'bold'))
                else:
                    key_btn.configure(text=main)

                key_btn.pack()

                # 호버 효과
                key_btn.bind('<Enter>', lambda e, b=key_btn, c=hover_color: b.configure(bg=c))
                key_btn.bind('<Leave>', lambda e, b=key_btn, c=bg_color: b.configure(bg=c))

                self.keys.append((main, key_btn))

        # 스페이스바
        space_frame = tk.Frame(self.kb_frame, bg='#0a0a0f')
        space_frame.pack(pady=4)
        space_btn = tk.Button(space_frame, text='SPACE', width=30, height=1,
                             font=('Segoe UI', 8), fg='#666', bg='#1a1a1a',
                             activebackground='#333', bd=1, relief='solid')
        space_btn.pack()

        # 상태 업데이트
        self.status_var.set(f'{lang["name"]}  |  한/영+숫자로 전환')

    def switch_language(self, num):
        """언어 전환"""
        if num in LANGUAGES:
            self.current_lang = num
            self.render_keyboard()

    def on_key_click(self, char):
        """키 클릭 시 애니메이션"""
        for main, btn in self.keys:
            if main == char:
                orig_bg = btn.cget('bg')
                btn.configure(bg='#f0c040', fg='#000')
                self.root.after(150, lambda b=btn, bg=orig_bg: b.configure(bg=bg, fg='#ddd'))
                break

    def on_key(self, event):
        """키보드 입력 처리"""
        # 숫자키로 언어 전환
        if event.char in '123456':
            num = int(event.char)
            if num in LANGUAGES:
                self.switch_language(num)
                return

        # ESC로 닫기
        if event.keysym == 'Escape':
            self.root.destroy()
            return

    def run(self):
        """실행"""
        self.create_window()
        self.root.mainloop()


# ═══════════════════════════════════════════
# 메인
# ═══════════════════════════════════════════

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    app = OmniTypeKeyboard()
    app.run()
