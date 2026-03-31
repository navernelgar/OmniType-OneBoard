# -*- coding: utf-8 -*-
"""
community_correction.py — 커뮤니티 번역 보정 엔진
===================================================
사용자가 오역을 발견 → 수정 제안 → 투표 → 덱 자동 업데이트

구조:
  1. suggest(term, genre, lang, old, new, reason) → 수정 제안
  2. vote(suggestion_id, user, approve) → 투표
  3. merge() → 과반 이상 승인된 제안 자동 적용
  4. report() → 현황 보고

파일:
  suggestions.json  — 수정 제안 목록
  votes.json        — 투표 기록
  merge_log.json    — 병합 이력

이수진 / 2026-03-31
"""

import json
import os
import sys
import time
import hashlib
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

TOOLS_DIR = Path(__file__).parent
DECK_DIR = TOOLS_DIR / 'genre_decks'
DATA_DIR = TOOLS_DIR / 'community'
DATA_DIR.mkdir(exist_ok=True)

SUGGESTIONS_FILE = DATA_DIR / 'suggestions.json'
VOTES_FILE = DATA_DIR / 'votes.json'
MERGE_LOG_FILE = DATA_DIR / 'merge_log.json'

# 병합 기준
MIN_VOTES = 3          # 최소 투표 수
APPROVE_RATIO = 0.6    # 승인 비율 (60% 이상)


def _load(path, default):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default


def _save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _gen_id(term, genre, lang, new_text):
    """제안 ID 생성 (해시)"""
    raw = f'{term}:{genre}:{lang}:{new_text}'
    return hashlib.md5(raw.encode()).hexdigest()[:8]


# ═══════════════════════════════════════════
# §1. 수정 제안
# ═══════════════════════════════════════════

def suggest(term, genre, lang, old_text, new_text, reason='', user='anonymous'):
    """
    번역 수정 제안

    Args:
        term: 원어 (예: 炉鼎)
        genre: 장르 (예: xianxia)
        lang: 타겟 언어 (예: ko)
        old_text: 기존 번역
        new_text: 제안 번역
        reason: 수정 이유
        user: 제안자

    Returns:
        suggestion dict
    """
    suggestions = _load(SUGGESTIONS_FILE, [])

    sid = _gen_id(term, genre, lang, new_text)

    # 중복 검사
    for s in suggestions:
        if s['id'] == sid:
            print(f"  이미 존재하는 제안: {sid}")
            return s

    suggestion = {
        'id': sid,
        'term': term,
        'genre': genre,
        'lang': lang,
        'old_text': old_text,
        'new_text': new_text,
        'reason': reason,
        'user': user,
        'created': time.strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'pending',  # pending → approved → merged / rejected
    }

    suggestions.append(suggestion)
    _save(SUGGESTIONS_FILE, suggestions)

    print(f"  제안 등록: [{sid}] {term} ({genre}/{lang})")
    print(f"    {old_text} → {new_text}")
    print(f"    이유: {reason}")

    return suggestion


# ═══════════════════════════════════════════
# §2. 투표
# ═══════════════════════════════════════════

def vote(suggestion_id, user, approve=True):
    """
    제안에 투표

    Args:
        suggestion_id: 제안 ID
        user: 투표자
        approve: True=찬성, False=반대
    """
    votes = _load(VOTES_FILE, [])

    # 중복 투표 방지
    for v in votes:
        if v['suggestion_id'] == suggestion_id and v['user'] == user:
            print(f"  이미 투표함: {user} → {suggestion_id}")
            return v

    v = {
        'suggestion_id': suggestion_id,
        'user': user,
        'approve': approve,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    votes.append(v)
    _save(VOTES_FILE, votes)

    emoji = '👍' if approve else '👎'
    print(f"  투표: {user} {emoji} [{suggestion_id}]")

    return v


def get_vote_stats(suggestion_id):
    """투표 현황"""
    votes = _load(VOTES_FILE, [])
    relevant = [v for v in votes if v['suggestion_id'] == suggestion_id]

    approve = sum(1 for v in relevant if v['approve'])
    reject = sum(1 for v in relevant if not v['approve'])
    total = len(relevant)

    return {
        'total': total,
        'approve': approve,
        'reject': reject,
        'ratio': approve / total if total > 0 else 0,
    }


# ═══════════════════════════════════════════
# §3. 병합
# ═══════════════════════════════════════════

def merge():
    """
    승인된 제안을 장르 덱에 자동 반영

    기준:
      - 최소 MIN_VOTES표 이상
      - 찬성 비율 APPROVE_RATIO 이상 (60%)
    """
    suggestions = _load(SUGGESTIONS_FILE, [])
    merge_log = _load(MERGE_LOG_FILE, [])

    merged_count = 0

    for s in suggestions:
        if s['status'] != 'pending':
            continue

        stats = get_vote_stats(s['id'])

        if stats['total'] < MIN_VOTES:
            continue

        if stats['ratio'] >= APPROVE_RATIO:
            # 승인 → 덱 업데이트
            success = update_genre_deck(s['genre'], s['term'], s['lang'], s['new_text'])

            if success:
                s['status'] = 'merged'
                merged_count += 1

                merge_log.append({
                    'suggestion_id': s['id'],
                    'term': s['term'],
                    'genre': s['genre'],
                    'lang': s['lang'],
                    'old_text': s['old_text'],
                    'new_text': s['new_text'],
                    'votes': stats,
                    'merged_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                })

                print(f"  병합: [{s['id']}] {s['term']} → {s['new_text']}")
                print(f"    투표: {stats['approve']}/{stats['total']} ({stats['ratio']:.0%})")
        else:
            # 반려
            s['status'] = 'rejected'
            print(f"  반려: [{s['id']}] {s['term']} (찬성 {stats['ratio']:.0%} < {APPROVE_RATIO:.0%})")

    _save(SUGGESTIONS_FILE, suggestions)
    _save(MERGE_LOG_FILE, merge_log)

    return merged_count


def update_genre_deck(genre, term, lang, new_text):
    """장르 덱 JSON 업데이트"""
    deck_path = DECK_DIR / f'{genre}.json'
    if not deck_path.exists():
        print(f"    덱 없음: {deck_path}")
        return False

    with open(deck_path, 'r', encoding='utf-8') as f:
        deck = json.load(f)

    # 해당 term 찾아서 업데이트
    for entry in deck['entries']:
        if entry['term'] == term:
            old = entry.get(lang, '')
            entry[lang] = new_text
            print(f"    업데이트: {term}.{lang} = '{old}' → '{new_text}'")

            with open(deck_path, 'w', encoding='utf-8') as f:
                json.dump(deck, f, indent=2, ensure_ascii=False)
            return True

    # 없으면 새 항목 추가
    new_entry = {'term': term, lang: new_text, 'tags': ['community']}
    deck['entries'].append(new_entry)
    deck['entry_count'] = len(deck['entries'])

    with open(deck_path, 'w', encoding='utf-8') as f:
        json.dump(deck, f, indent=2, ensure_ascii=False)

    print(f"    추가: {term}.{lang} = '{new_text}'")
    return True


# ═══════════════════════════════════════════
# §4. 리포트
# ═══════════════════════════════════════════

def report():
    """현황 보고"""
    suggestions = _load(SUGGESTIONS_FILE, [])
    votes = _load(VOTES_FILE, [])
    merge_log = _load(MERGE_LOG_FILE, [])

    pending = [s for s in suggestions if s['status'] == 'pending']
    merged = [s for s in suggestions if s['status'] == 'merged']
    rejected = [s for s in suggestions if s['status'] == 'rejected']

    print(f"\n{'='*50}")
    print(f"  Community Correction Report")
    print(f"{'='*50}")
    print(f"  제안: {len(suggestions)}건 (대기 {len(pending)} | 병합 {len(merged)} | 반려 {len(rejected)})")
    print(f"  투표: {len(votes)}건")
    print(f"  병합 이력: {len(merge_log)}건")

    if pending:
        print(f"\n  대기 중 제안:")
        for s in pending:
            stats = get_vote_stats(s['id'])
            print(f"    [{s['id']}] {s['term']} ({s['genre']}/{s['lang']})")
            print(f"      {s['old_text']} → {s['new_text']}")
            print(f"      투표: {stats['approve']}/{stats['total']}"
                  f" ({stats['ratio']:.0%}) {'← 병합 가능' if stats['total'] >= MIN_VOTES and stats['ratio'] >= APPROVE_RATIO else ''}")


# ═══════════════════════════════════════════
# §5. CLI + 데모
# ═══════════════════════════════════════════

def run_demo():
    """데모: 제안 → 투표 → 병합 전체 흐름"""
    print("\n=== 커뮤니티 보정 데모 ===\n")

    # 1. 제안
    print("--- 1. 수정 제안 ---")
    suggest('炉鼎', 'xianxia', 'en',
            'cultivation vessel (derogatory for women)',
            'furnace cauldron (dual cultivation tool)',
            '영문 위키에서는 furnace cauldron이 더 일반적',
            user='player_kr_01')

    suggest('feed', 'moba', 'ko',
            '적 먹여주기',
            '피딩 (적에게 킬을 반복 헌납)',
            '한국 LOL 유저 사이에서 피딩이 더 표준',
            user='lol_player_99')

    suggest('aggro', 'rpg', 'zh',
            '仇恨',
            '仇恨值/OT',
            '중국 게이머들은 仇恨值 또는 OT로 더 많이 부름',
            user='genshin_cn')

    # 2. 투표
    print("\n--- 2. 투표 ---")
    # 炉鼎 제안에 투표
    sid = _gen_id('炉鼎', 'xianxia', 'en', 'furnace cauldron (dual cultivation tool)')
    vote(sid, 'user_a', True)
    vote(sid, 'user_b', True)
    vote(sid, 'user_c', False)
    vote(sid, 'user_d', True)

    # feed 제안에 투표
    sid2 = _gen_id('feed', 'moba', 'ko', '피딩 (적에게 킬을 반복 헌납)')
    vote(sid2, 'user_a', True)
    vote(sid2, 'user_b', True)
    vote(sid2, 'user_c', True)

    # aggro 제안에 투표 (미달)
    sid3 = _gen_id('aggro', 'rpg', 'zh', '仇恨值/OT')
    vote(sid3, 'user_a', True)
    vote(sid3, 'user_b', False)

    # 3. 병합
    print("\n--- 3. 병합 시도 ---")
    merged = merge()
    print(f"\n  병합 완료: {merged}건")

    # 4. 리포트
    report()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'demo':
            run_demo()
        elif cmd == 'report':
            report()
        elif cmd == 'merge':
            merged = merge()
            print(f"병합: {merged}건")
        elif cmd == 'suggest':
            if len(sys.argv) >= 7:
                suggest(sys.argv[2], sys.argv[3], sys.argv[4],
                        sys.argv[5], sys.argv[6],
                        sys.argv[7] if len(sys.argv) > 7 else '',
                        sys.argv[8] if len(sys.argv) > 8 else 'cli')
            else:
                print("사용법: python community_correction.py suggest <term> <genre> <lang> <old> <new> [reason] [user]")
        else:
            report()
    else:
        print("사용법:")
        print("  demo    — 전체 흐름 데모")
        print("  report  — 현황 보고")
        print("  merge   — 승인된 제안 병합")
        print("  suggest — 수정 제안")
