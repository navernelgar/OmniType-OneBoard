# -*- coding: utf-8 -*-
"""
genre_deck_collector.py — 장르별 게임 용어 수집기
===================================================
각국 위키에서 장르 용어를 수집 → 교차매칭 → .kn 장르덱 생성

소스:
  나무위키    (ko) — 클리셰/용어 문서
  萌娘百科    (zh) — 术语 문서
  ピクシブ百科 (ja) — 用語集 문서
  TVTropes    (en) — Terminology 문서
  Fandom Wiki (en) — 게임별 위키

파이프라인:
  1. 위키 페이지 크롤링 (requests + BeautifulSoup)
  2. 용어-정의 쌍 추출 (테이블/리스트 파싱)
  3. 교차매칭 (같은 원어 → 다국어 뜻 합치기)
  4. .kn 장르덱 파일 생성
  5. 카드 생성 (/learn 연동)

이수진 / 2026-03-31
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TOOLS_DIR = Path(__file__).parent
OUTPUT_DIR = TOOLS_DIR / 'genre_decks'
OUTPUT_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════
# §1. 위키 소스 정의
# ═══════════════════════════════════════════

WIKI_SOURCES = {
    'xianxia': {
        'ko': [
            'https://namu.wiki/w/선협물/클리셰',
            'https://namu.wiki/w/선협물/용어',
        ],
        'zh': [
            # 萌娘百科 修仙 용어
            'https://zh.moegirl.org.cn/修仙术语',
        ],
        'en': [
            'https://tvtropes.org/pmwiki/pmwiki.php/Main/Xianxia',
        ],
        'ja': [
            # 선협 일본어 위키
        ],
    },
    'fps': {
        'ko': ['https://namu.wiki/w/FPS/용어'],
        'en': ['https://tvtropes.org/pmwiki/pmwiki.php/Main/FPSTropes'],
        'zh': ['https://zh.moegirl.org.cn/FPS游戏术语'],
        'ja': [],
    },
    'moba': {
        'ko': ['https://namu.wiki/w/MOBA/용어'],
        'en': [],
        'zh': ['https://zh.moegirl.org.cn/MOBA游戏术语'],
        'ja': [],
    },
    'rpg': {
        'ko': ['https://namu.wiki/w/RPG/용어'],
        'en': ['https://tvtropes.org/pmwiki/pmwiki.php/Main/RPGTropes'],
        'zh': [],
        'ja': [],
    },
    'wuxia': {
        'ko': ['https://namu.wiki/w/무협물/클리셰'],
        'en': ['https://tvtropes.org/pmwiki/pmwiki.php/Main/WuxiaGenre'],
        'zh': ['https://zh.moegirl.org.cn/武侠术语'],
        'ja': [],
    },
    'vn': {
        'ko': ['https://namu.wiki/w/비주얼 노벨/용어'],
        'en': [],
        'zh': [],
        'ja': [],
    },
}

# ═══════════════════════════════════════════
# §2. 내장 기본 덱 (위키 크롤링 실패 시 폴백)
# ═══════════════════════════════════════════

# ═══════════════════════════════════════════
# §2-A. 게임별 세계관 덱 (장르보다 우선)
# ═══════════════════════════════════════════

GAME_WORLD_SOURCES = {
    'wow': {
        'ko': ['https://namu.wiki/w/월드 오브 워크래프트/용어'],
        'en': ['https://wowpedia.fandom.com/wiki/Glossary'],
        'zh': ['https://zh.moegirl.org.cn/魔兽世界术语'],
    },
    'genshin': {
        'ko': ['https://namu.wiki/w/원신/용어'],
        'en': ['https://genshin-impact.fandom.com/wiki/Glossary'],
        'zh': ['https://zh.moegirl.org.cn/原神术语'],
        'ja': [],
    },
    'lol': {
        'ko': ['https://namu.wiki/w/리그 오브 레전드/용어'],
        'en': ['https://leagueoflegends.fandom.com/wiki/Glossary'],
    },
    'ff14': {
        'ko': ['https://namu.wiki/w/파이널 판타지 14/용어'],
        'en': ['https://finalfantasy.fandom.com/wiki/Final_Fantasy_XIV_terminology'],
        'ja': [],
    },
    'darksouls': {
        'ko': ['https://namu.wiki/w/다크 소울 시리즈/용어'],
        'en': ['https://darksouls.fandom.com/wiki/Glossary'],
    },
    'minecraft': {
        'ko': ['https://namu.wiki/w/마인크래프트/용어'],
        'en': ['https://minecraft.wiki/w/Glossary'],
    },
    'valorant': {
        'ko': ['https://namu.wiki/w/발로란트/용어'],
        'en': ['https://valorant.fandom.com/wiki/Glossary'],
    },
}

BUILTIN_GAME_DECKS = {
    'wow': [
        {'term': 'Horde', 'ko': '호드 (진영)', 'en': 'Horde (faction)', 'ja': 'ホード（陣営）', 'zh': '部落（阵营）', 'tags': ['faction']},
        {'term': 'Alliance', 'ko': '얼라이언스 (진영)', 'en': 'Alliance (faction)', 'ja': 'アライアンス（陣営）', 'zh': '联盟（阵营）', 'tags': ['faction']},
        {'term': 'Azeroth', 'ko': '아제로스 (세계)', 'en': 'Azeroth (world)', 'ja': 'アゼロス', 'zh': '艾泽拉斯', 'tags': ['world']},
        {'term': 'Thrall', 'ko': '스랄 (대족장)', 'en': 'Thrall (Warchief)', 'ja': 'スラル', 'zh': '萨尔', 'tags': ['character']},
        {'term': 'Lich King', 'ko': '리치 왕', 'en': 'Lich King', 'ja': 'リッチキング', 'zh': '巫妖王', 'tags': ['character']},
        {'term': 'Mana', 'ko': '마나 (마력)', 'en': 'Mana (magic resource)', 'ja': 'マナ', 'zh': '法力', 'tags': ['resource']},
        {'term': 'Hearthstone', 'ko': '귀환석 (마을 귀환)', 'en': 'Hearthstone (teleport home)', 'ja': '炉石（帰還石）', 'zh': '炉石（回城石）', 'tags': ['item']},
        {'term': 'Raid', 'ko': '공격대 (10~25인)', 'en': 'Raid (10-25 player)', 'ja': 'レイド', 'zh': '团队副本', 'tags': ['content']},
        {'term': 'Instance', 'ko': '인스턴스 (던전)', 'en': 'Instance (dungeon)', 'ja': 'インスタンス', 'zh': '副本', 'tags': ['content']},
        {'term': 'Warchief', 'ko': '대족장', 'en': 'Warchief', 'ja': '大首長', 'zh': '大酋长', 'tags': ['title']},
        {'term': 'Undead', 'ko': '언데드 (포세이큰)', 'en': 'Undead (Forsaken)', 'ja': 'アンデッド', 'zh': '亡灵（被遗忘者）', 'tags': ['race']},
        {'term': 'Blood Elf', 'ko': '블러드 엘프', 'en': 'Blood Elf', 'ja': 'ブラッドエルフ', 'zh': '血精灵', 'tags': ['race']},
        {'term': 'DK', 'ko': '죽기 (죽음의 기사)', 'en': 'Death Knight', 'ja': 'デスナイト', 'zh': '死亡骑士', 'tags': ['class']},
        {'term': 'WTB', 'ko': '삽니다', 'en': 'Want to Buy', 'ja': '買います', 'zh': '收', 'tags': ['trade']},
        {'term': 'WTS', 'ko': '팝니다', 'en': 'Want to Sell', 'ja': '売ります', 'zh': '出', 'tags': ['trade']},
        {'term': 'LFG', 'ko': '파티 구함', 'en': 'Looking for Group', 'ja': 'メンバー募集', 'zh': '找队伍', 'tags': ['social']},
        {'term': 'GG', 'ko': '수고했어', 'en': 'Good Game', 'ja': 'お疲れ', 'zh': 'GG', 'tags': ['social']},
        {'term': 'AFK', 'ko': '자리비움', 'en': 'Away from Keyboard', 'ja': '離席', 'zh': '挂机', 'tags': ['social']},
    ],
    'genshin': [
        {'term': 'Vision', 'ko': '신의 눈 (원소 증표)', 'en': 'Vision (elemental grant)', 'ja': '神の目', 'zh': '神之眼', 'tags': ['lore']},
        {'term': 'Archon', 'ko': '마신 (지역 신)', 'en': 'Archon (regional god)', 'ja': '魔神', 'zh': '魔神', 'tags': ['lore']},
        {'term': 'Resin', 'ko': '레진 (체력)', 'en': 'Resin (stamina system)', 'ja': '樹脂', 'zh': '树脂（体力）', 'tags': ['system']},
        {'term': 'Constellation', 'ko': '명좌 (캐릭터 강화)', 'en': 'Constellation (character upgrade)', 'ja': '命ノ星座', 'zh': '命之座', 'tags': ['system']},
        {'term': 'Teyvat', 'ko': '테이바트 (세계)', 'en': 'Teyvat (world)', 'ja': 'テイワット', 'zh': '提瓦特', 'tags': ['world']},
        {'term': 'Primogem', 'ko': '원석 (가챠 재화)', 'en': 'Primogem (gacha currency)', 'ja': '原石', 'zh': '原石', 'tags': ['currency']},
        {'term': 'Wish', 'ko': '기원 (가챠)', 'en': 'Wish (gacha pull)', 'ja': '祈願', 'zh': '祈愿（抽卡）', 'tags': ['system']},
        {'term': 'Pity', 'ko': '천장 (보장 시스템)', 'en': 'Pity (guarantee system)', 'ja': '天井', 'zh': '保底', 'tags': ['system']},
        {'term': 'Mora', 'ko': '모라 (골드)', 'en': 'Mora (gold currency)', 'ja': 'モラ', 'zh': '摩拉', 'tags': ['currency']},
        {'term': 'Elemental Burst', 'ko': '원소 폭발 (궁극기)', 'en': 'Elemental Burst (ultimate)', 'ja': '元素爆発', 'zh': '元素爆发', 'tags': ['ability']},
        {'term': 'Elemental Skill', 'ko': '원소 전투 스킬', 'en': 'Elemental Skill', 'ja': '元素スキル', 'zh': '元素战技', 'tags': ['ability']},
        {'term': 'Abyss', 'ko': '나선 비경 (엔드 콘텐츠)', 'en': 'Spiral Abyss (endgame)', 'ja': '深境螺旋', 'zh': '深境螺旋', 'tags': ['content']},
        {'term': 'Domains', 'ko': '비경 (던전)', 'en': 'Domain (dungeon)', 'ja': '秘境', 'zh': '秘境', 'tags': ['content']},
        {'term': 'Fatui', 'ko': '우인단 (적 조직)', 'en': 'Fatui (antagonist faction)', 'ja': 'ファデュイ', 'zh': '愚人众', 'tags': ['faction']},
        {'term': 'Traveler', 'ko': '여행자 (주인공)', 'en': 'Traveler (protagonist)', 'ja': '旅人', 'zh': '旅行者', 'tags': ['character']},
    ],
    'lol': [
        {'term': 'Summoner', 'ko': '소환사', 'en': 'Summoner', 'ja': 'サモナー', 'zh': '召唤师', 'tags': ['lore']},
        {'term': 'Rift', 'ko': '소환사의 협곡', 'en': "Summoner's Rift", 'ja': 'サモナーズリフト', 'zh': '召唤师峡谷', 'tags': ['map']},
        {'term': 'Baron Nashor', 'ko': '바론 내셔', 'en': 'Baron Nashor', 'ja': 'バロンナッシャー', 'zh': '纳什男爵', 'tags': ['objective']},
        {'term': 'Drake', 'ko': '드래곤/용', 'en': 'Dragon/Drake', 'ja': 'ドラゴン', 'zh': '小龙', 'tags': ['objective']},
        {'term': 'Nexus', 'ko': '넥서스 (본진)', 'en': 'Nexus (base)', 'ja': 'ネクサス', 'zh': '水晶（基地）', 'tags': ['map']},
        {'term': 'Flash', 'ko': '점멸', 'en': 'Flash', 'ja': 'フラッシュ', 'zh': '闪现', 'tags': ['spell']},
        {'term': 'Ignite', 'ko': '점화', 'en': 'Ignite', 'ja': 'イグナイト', 'zh': '引燃', 'tags': ['spell']},
        {'term': 'Pentakill', 'ko': '펜타킬', 'en': 'Pentakill', 'ja': 'ペンタキル', 'zh': '五杀', 'tags': ['event']},
        {'term': 'ADC', 'ko': '원딜 (원거리 딜러)', 'en': 'AD Carry', 'ja': 'ADC', 'zh': 'ADC/射手', 'tags': ['role']},
        {'term': 'Jungler', 'ko': '정글러', 'en': 'Jungler', 'ja': 'ジャングラー', 'zh': '打野', 'tags': ['role']},
    ],
    'darksouls': [
        {'term': 'Bonfire', 'ko': '모닥불 (세이브 포인트)', 'en': 'Bonfire (checkpoint)', 'ja': '篝火', 'zh': '篝火（存档点）', 'tags': ['system']},
        {'term': 'Estus Flask', 'ko': '에스트 플라스크 (회복)', 'en': 'Estus Flask (healing)', 'ja': 'エスト瓶', 'zh': '原素瓶', 'tags': ['item']},
        {'term': 'Hollow', 'ko': '망자 (언데드 변형)', 'en': 'Hollow (undead form)', 'ja': '亡者', 'zh': '活尸', 'tags': ['lore']},
        {'term': 'Souls', 'ko': '소울 (경험치+화폐)', 'en': 'Souls (XP+currency)', 'ja': 'ソウル', 'zh': '魂（经验+货币）', 'tags': ['currency']},
        {'term': 'Ember', 'ko': '잔불/불씨', 'en': 'Ember', 'ja': '残り火', 'zh': '余火', 'tags': ['item']},
        {'term': 'Invade', 'ko': '침입 (PvP)', 'en': 'Invade (PvP)', 'ja': '侵入', 'zh': '入侵', 'tags': ['pvp']},
        {'term': 'Summon', 'ko': '소환 (협력)', 'en': 'Summon (co-op)', 'ja': '召喚', 'zh': '召唤', 'tags': ['coop']},
        {'term': 'Git Gud', 'ko': '실력을 키워라', 'en': 'Get Good (skill up)', 'ja': '上手くなれ', 'zh': '变强吧', 'tags': ['meme']},
        {'term': 'YOU DIED', 'ko': '사망', 'en': 'YOU DIED', 'ja': 'YOU DIED', 'zh': 'YOU DIED', 'tags': ['system']},
    ],
}

BUILTIN_DECKS = {
    'xianxia': [
        {'term': '炉鼎', 'ko': '쌍수 도구 (여성 비하)', 'en': 'cultivation vessel (derogatory for women)', 'ja': '炉鼎（双修道具）', 'zh': '双修用的女性', 'tags': ['derogatory','cultivation']},
        {'term': '道侣', 'ko': '수련 파트너/배우자', 'en': 'cultivation partner/spouse', 'ja': '道侶（修行パートナー）', 'zh': '修仙伴侣', 'tags': ['relationship']},
        {'term': '筑基', 'ko': '축기 (수련 2단계)', 'en': 'Foundation Establishment (stage 2)', 'ja': '築基（修行第2段階）', 'zh': '修炼第二阶段', 'tags': ['cultivation_stage']},
        {'term': '金丹', 'ko': '금단 (수련 3단계)', 'en': 'Golden Core (stage 3)', 'ja': '金丹（修行第3段階）', 'zh': '修炼第三阶段', 'tags': ['cultivation_stage']},
        {'term': '元婴', 'ko': '원영 (수련 4단계, 분신)', 'en': 'Nascent Soul (stage 4)', 'ja': '元嬰（修行第4段階）', 'zh': '修炼第四阶段', 'tags': ['cultivation_stage']},
        {'term': '化神', 'ko': '화신 (수련 5단계)', 'en': 'Spirit Severing (stage 5)', 'ja': '化神（修行第5段階）', 'zh': '修炼第五阶段', 'tags': ['cultivation_stage']},
        {'term': '灵石', 'ko': '영석 (화폐)', 'en': 'spirit stone (currency)', 'ja': '霊石（通貨）', 'zh': '灵石（货币）', 'tags': ['currency']},
        {'term': '灵根', 'ko': '영근 (수련 재능)', 'en': 'spiritual root (talent)', 'ja': '霊根（才能）', 'zh': '灵根（天赋）', 'tags': ['talent']},
        {'term': '天劫', 'ko': '천겁 (승급 시험)', 'en': 'heavenly tribulation', 'ja': '天劫（昇格試練）', 'zh': '天劫（渡劫）', 'tags': ['event']},
        {'term': '飞升', 'ko': '비승 (선계 승천)', 'en': 'ascension', 'ja': '飛昇（仙界へ）', 'zh': '飞升', 'tags': ['event']},
        {'term': '双修', 'ko': '쌍수 (함께 수련)', 'en': 'dual cultivation', 'ja': '双修（合同修行）', 'zh': '双修', 'tags': ['cultivation']},
        {'term': '丹药', 'ko': '단약 (수련 알약)', 'en': 'pill/elixir', 'ja': '丹薬', 'zh': '丹药', 'tags': ['item']},
        {'term': '法宝', 'ko': '법보 (무기/아이템)', 'en': 'magical treasure', 'ja': '法宝（武器）', 'zh': '法宝', 'tags': ['item']},
        {'term': '宗门', 'ko': '종문 (문파/길드)', 'en': 'sect/clan', 'ja': '宗門（ギルド）', 'zh': '宗门', 'tags': ['organization']},
        {'term': '掌门', 'ko': '장문인 (문파장)', 'en': 'sect master', 'ja': '掌門（門派長）', 'zh': '掌门', 'tags': ['title']},
        {'term': '秘境', 'ko': '비경 (던전)', 'en': 'secret realm (dungeon)', 'ja': '秘境（ダンジョン）', 'zh': '秘境', 'tags': ['location']},
        {'term': '内门弟子', 'ko': '내문제자 (정식)', 'en': 'inner disciple', 'ja': '内門弟子', 'zh': '内门弟子', 'tags': ['rank']},
        {'term': '外门弟子', 'ko': '외문제자 (수습)', 'en': 'outer disciple', 'ja': '外門弟子', 'zh': '外门弟子', 'tags': ['rank']},
        {'term': '渡劫', 'ko': '도겁 (천겁 극복)', 'en': 'tribulation crossing', 'ja': '渡劫', 'zh': '渡劫', 'tags': ['event']},
        {'term': '神识', 'ko': '신식 (정신력 탐지)', 'en': 'divine sense', 'ja': '神識', 'zh': '神识', 'tags': ['ability']},
    ],
    'wuxia': [
        {'term': '内功', 'ko': '내공', 'en': 'inner power/qi', 'ja': '内功', 'zh': '内功', 'tags': ['ability']},
        {'term': '轻功', 'ko': '경공 (공중 이동)', 'en': 'lightness skill', 'ja': '軽功', 'zh': '轻功', 'tags': ['ability']},
        {'term': '点穴', 'ko': '점혈 (혈도 찌르기)', 'en': 'pressure point strike', 'ja': '点穴', 'zh': '点穴', 'tags': ['technique']},
        {'term': '掌法', 'ko': '장법 (손바닥 무공)', 'en': 'palm technique', 'ja': '掌法', 'zh': '掌法', 'tags': ['technique']},
        {'term': '剑法', 'ko': '검법', 'en': 'sword technique', 'ja': '剣法', 'zh': '剑法', 'tags': ['technique']},
        {'term': '暗器', 'ko': '암기 (숨겨진 무기)', 'en': 'hidden weapon', 'ja': '暗器', 'zh': '暗器', 'tags': ['weapon']},
        {'term': '江湖', 'ko': '강호 (무림 세계)', 'en': 'jianghu (martial world)', 'ja': '江湖', 'zh': '江湖', 'tags': ['world']},
        {'term': '侠客', 'ko': '협객 (무협 영웅)', 'en': 'xia/hero', 'ja': '侠客', 'zh': '侠客', 'tags': ['character']},
        {'term': '武林盟主', 'ko': '무림맹주', 'en': 'martial alliance leader', 'ja': '武林盟主', 'zh': '武林盟主', 'tags': ['title']},
        {'term': '门派', 'ko': '문파', 'en': 'martial sect', 'ja': '門派', 'zh': '门派', 'tags': ['organization']},
        {'term': '真气', 'ko': '진기', 'en': 'true qi', 'ja': '真気', 'zh': '真气', 'tags': ['ability']},
        {'term': '穴道', 'ko': '혈도 (경혈)', 'en': 'acupoint', 'ja': '穴道', 'zh': '穴道', 'tags': ['body']},
    ],
    'fps': [
        {'term': 'camp', 'ko': '캠핑/자리잡기', 'en': 'camping (holding position)', 'ja': 'キャンプ', 'zh': '蹲点/阴人', 'tags': ['tactic']},
        {'term': 'nerf', 'ko': '하향 패치', 'en': 'nerf (make weaker)', 'ja': 'ナーフ（弱体化）', 'zh': '削弱', 'tags': ['balance']},
        {'term': 'buff', 'ko': '상향/버프', 'en': 'buff (make stronger)', 'ja': 'バフ（強化）', 'zh': '加强/Buff', 'tags': ['balance']},
        {'term': 'clutch', 'ko': '클러치 (1vs다수 승리)', 'en': 'clutch (1vX win)', 'ja': 'クラッチ', 'zh': '残局翻盘', 'tags': ['play']},
        {'term': 'peek', 'ko': '피킹 (코너에서 살짝)', 'en': 'peeking (quick look)', 'ja': 'ピーク', 'zh': '探头/Peek', 'tags': ['tactic']},
        {'term': 'wallbang', 'ko': '벽관통 사격', 'en': 'wallbang (shoot through wall)', 'ja': '壁抜き', 'zh': '穿墙', 'tags': ['technique']},
        {'term': 'spray', 'ko': '난사/스프레이', 'en': 'spray (continuous fire)', 'ja': 'スプレー', 'zh': '扫射', 'tags': ['technique']},
        {'term': 'one-tap', 'ko': '원탭 (헤드샷 원킬)', 'en': 'one-tap (headshot kill)', 'ja': 'ワンタップ', 'zh': '一枪头', 'tags': ['technique']},
        {'term': 'callout', 'ko': '위치 보고/콜아웃', 'en': 'callout (location report)', 'ja': 'コールアウト', 'zh': '报点', 'tags': ['comm']},
        {'term': 'rotate', 'ko': '로테이션 (이동)', 'en': 'rotate (reposition)', 'ja': 'ローテ', 'zh': '转点', 'tags': ['tactic']},
        {'term': 'ADS', 'ko': '조준 사격', 'en': 'aim down sight', 'ja': 'エイム', 'zh': '开镜', 'tags': ['technique']},
        {'term': 'TTK', 'ko': '킬 소요 시간', 'en': 'time to kill', 'ja': 'キルタイム', 'zh': '击杀时间', 'tags': ['stat']},
    ],
    'moba': [
        {'term': 'gank', 'ko': '기습/갱킹', 'en': 'gank (surprise attack)', 'ja': 'ガンク', 'zh': '抓人/Gank', 'tags': ['tactic']},
        {'term': 'lane', 'ko': '라인', 'en': 'lane', 'ja': 'レーン', 'zh': '路/线', 'tags': ['map']},
        {'term': 'jungle', 'ko': '정글링', 'en': 'jungling', 'ja': 'ジャングル', 'zh': '打野', 'tags': ['role']},
        {'term': 'feed', 'ko': '적 먹여주기', 'en': 'feeding (dying repeatedly)', 'ja': 'フィード', 'zh': '送人头', 'tags': ['play']},
        {'term': 'carry', 'ko': '캐리', 'en': 'carry (lead team to win)', 'ja': 'キャリー', 'zh': 'C位/Carry', 'tags': ['role']},
        {'term': 'tower dive', 'ko': '타워 다이브', 'en': 'tower dive', 'ja': 'タワーダイブ', 'zh': '越塔', 'tags': ['tactic']},
        {'term': 'ward', 'ko': '와드 (시야)', 'en': 'ward (vision)', 'ja': 'ワード', 'zh': '插眼/排眼', 'tags': ['vision']},
        {'term': 'CS', 'ko': '미니언 처치', 'en': 'creep score', 'ja': 'CS', 'zh': '补刀', 'tags': ['stat']},
        {'term': 'CC', 'ko': '군중제어', 'en': 'crowd control', 'ja': 'CC', 'zh': '控制', 'tags': ['ability']},
        {'term': 'ult', 'ko': '궁극기', 'en': 'ultimate ability', 'ja': 'ウルト', 'zh': '大招', 'tags': ['ability']},
        {'term': 'baron', 'ko': '바론', 'en': 'baron/roshan', 'ja': 'バロン', 'zh': '大龙', 'tags': ['objective']},
        {'term': 'ace', 'ko': '에이스 (전멸)', 'en': 'ace (team wipe)', 'ja': 'エース', 'zh': '团灭', 'tags': ['event']},
    ],
    'rpg': [
        {'term': 'aggro', 'ko': '어그로 (적 관심)', 'en': 'aggro (threat)', 'ja': 'アグロ/ヘイト', 'zh': '仇恨', 'tags': ['mechanic']},
        {'term': 'DPS', 'ko': '딜러', 'en': 'damage dealer', 'ja': 'DPS/アタッカー', 'zh': '输出', 'tags': ['role']},
        {'term': 'tank', 'ko': '탱커', 'en': 'tank', 'ja': 'タンク', 'zh': '坦克/T', 'tags': ['role']},
        {'term': 'healer', 'ko': '힐러', 'en': 'healer', 'ja': 'ヒーラー', 'zh': '奶妈/治疗', 'tags': ['role']},
        {'term': 'proc', 'ko': '발동 (확률 효과)', 'en': 'proc (trigger effect)', 'ja': 'プロック', 'zh': '触发', 'tags': ['mechanic']},
        {'term': 'loot', 'ko': '전리품/루팅', 'en': 'loot', 'ja': 'ルート/ドロップ', 'zh': '掉落', 'tags': ['item']},
        {'term': 'raid', 'ko': '레이드', 'en': 'raid', 'ja': 'レイド', 'zh': '团本', 'tags': ['content']},
        {'term': 'meta', 'ko': '메타 (최적 전략)', 'en': 'meta (optimal strategy)', 'ja': 'メタ', 'zh': '版本答案', 'tags': ['strategy']},
        {'term': 'grind', 'ko': '노가다/파밍', 'en': 'grinding', 'ja': '周回', 'zh': '肝/刷', 'tags': ['activity']},
        {'term': 'nerf', 'ko': '너프 (하향)', 'en': 'nerf', 'ja': 'ナーフ', 'zh': '削弱', 'tags': ['balance']},
        {'term': 'gacha', 'ko': '가챠/뽑기', 'en': 'gacha (random pull)', 'ja': 'ガチャ', 'zh': '抽卡', 'tags': ['monetization']},
        {'term': 'whale', 'ko': '고래 (과금러)', 'en': 'whale (big spender)', 'ja': '廃課金', 'zh': '氪佬/大佬', 'tags': ['player']},
    ],
}


# ═══════════════════════════════════════════
# §3. 덱 생성
# ═══════════════════════════════════════════

def generate_deck_json(genre, entries):
    """장르 덱 JSON 파일 생성"""
    deck = {
        'genre': genre,
        'version': '1.0',
        'generated': time.strftime('%Y-%m-%d'),
        'entry_count': len(entries),
        'entries': entries,
    }

    output_path = OUTPUT_DIR / f'{genre}.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(deck, f, indent=2, ensure_ascii=False)

    return output_path


def generate_deck_kn(genre, entries):
    """장르 덱 .kn 바이너리 파일 생성 (간소화 버전)"""
    # 헤더: KN01 + genre + entry count
    data = bytearray()
    data += b'KN01'
    genre_bytes = genre.encode('utf-8')
    data += len(genre_bytes).to_bytes(1, 'little')
    data += genre_bytes
    data += len(entries).to_bytes(2, 'little')

    # 각 엔트리: term + 4개 언어 번역
    for entry in entries:
        term = entry['term'].encode('utf-8')
        data += len(term).to_bytes(1, 'little')
        data += term

        for lang in ['ko', 'en', 'ja', 'zh']:
            text = entry.get(lang, '').encode('utf-8')
            data += len(text).to_bytes(2, 'little')
            data += text

    output_path = OUTPUT_DIR / f'{genre}.kn'
    with open(output_path, 'wb') as f:
        f.write(data)

    return output_path, len(data)


def generate_cards_md(genre, entries):
    """카드덱 마크다운 생성 (/learn 연동용)"""
    lines = [f'# {genre.upper()} 장르 용어 카드덱']
    lines.append(f'# 자동 생성: {time.strftime("%Y-%m-%d")}')
    lines.append(f'# 총 {len(entries)}장\n')

    # 태그별 그룹화
    by_tag = defaultdict(list)
    for entry in entries:
        for tag in entry.get('tags', ['general']):
            by_tag[tag].append(entry)

    for tag, group in sorted(by_tag.items()):
        lines.append(f'\n## {tag} ({len(group)}장)\n')
        for entry in group:
            lines.append(f'### {entry["term"]}')
            lines.append(f'- KO: {entry.get("ko", "")}')
            lines.append(f'- EN: {entry.get("en", "")}')
            lines.append(f'- JA: {entry.get("ja", "")}')
            lines.append(f'- ZH: {entry.get("zh", "")}')
            lines.append('')

    output_path = OUTPUT_DIR / f'{genre}_cards.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return output_path


# ═══════════════════════════════════════════
# §4. 메인
# ═══════════════════════════════════════════

def build_all_decks():
    """내장 덱 전체 생성 (장르 + 게임 세계관)"""
    all_decks = {}
    all_decks.update(BUILTIN_DECKS)
    all_decks.update(BUILTIN_GAME_DECKS)

    genre_count = len(BUILTIN_DECKS)
    game_count = len(BUILTIN_GAME_DECKS)

    print(f"{'='*50}")
    print(f"  OmniType Genre & World Deck Collector")
    print(f"  장르 {genre_count}개 + 게임 세계관 {game_count}개 = {len(all_decks)}개")
    print(f"{'='*50}")

    total_entries = 0
    total_size = 0

    print(f"\n  --- 장르 덱 ---")
    for genre, entries in BUILTIN_DECKS.items():
        json_path = generate_deck_json(genre, entries)
        kn_path, kn_size = generate_deck_kn(genre, entries)
        md_path = generate_cards_md(genre, entries)
        total_entries += len(entries)
        total_size += kn_size
        print(f"  [{genre:12s}] {len(entries):3d}장 | .kn={kn_size:,}B")

    print(f"\n  --- 게임 세계관 덱 ---")
    for game, entries in BUILTIN_GAME_DECKS.items():
        json_path = generate_deck_json(game, entries)
        kn_path, kn_size = generate_deck_kn(game, entries)
        md_path = generate_cards_md(game, entries)
        total_entries += len(entries)
        total_size += kn_size
        print(f"  [{game:12s}] {len(entries):3d}장 | .kn={kn_size:,}B")

    print(f"\n  총합: {total_entries}장, {total_size:,}B ({total_size/1024:.1f}KB)")
    print(f"  출력: {OUTPUT_DIR}")
    return total_entries


def collect_from_wiki(genre, lang='ko'):
    """위키 크롤링 (향후 구현)"""
    # TODO: requests + BeautifulSoup로 위키 크롤링
    # 나무위키: 테이블/리스트에서 용어-정의 추출
    # 萌娘百科: 같은 패턴
    # 교차매칭: 같은 term이 여러 언어에서 발견되면 합치기
    print(f"  [TODO] {genre}/{lang} 위키 크롤링 미구현")
    print(f"  → 내장 덱 사용 중")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'wiki':
        genre = sys.argv[2] if len(sys.argv) > 2 else 'xianxia'
        collect_from_wiki(genre)
    else:
        build_all_decks()
