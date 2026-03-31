# -*- coding: utf-8 -*-
"""
lang_data.py — 198개국 언어 데이터
===================================
각 언어의 대표 문자셋 + 자음/모음 분류 + 사용 예시.
PPT 자동 생성용.

이수진 / 2026-03-31
"""

# (코드, 이름, 스크립트, 자음수, 모음수, 동음이의수, 대표문자3행, 사용예시)
# 대표문자: QWERTY 3행 기준, (문자, 로마자, 자음여부)
# 사용예시: (입력, 결과, 설명)

LANGUAGES = [
    # ─── 기본 6개 (이미 수동 매핑됨, 자동 생성 제외) ───
    # ko, en, ja, zh, ar, ru → build_portfolio.py에서 직접 생성

    # ─── 아시아 ───
    ('hi', 'हिन्दी (Hindi)', 'Devanagari', 33, 11, 0,
     [
         [('क','ka',True),('ख','kha',True),('ग','ga',True),('घ','gha',True),('ङ','ṅa',True),
          ('च','ca',True),('छ','cha',True),('ज','ja',True),('झ','jha',True),('ञ','ña',True)],
         [('ट','ṭa',True),('ठ','ṭha',True),('ड','ḍa',True),('ढ','ḍha',True),('ण','ṇa',True),
          ('त','ta',True),('थ','tha',True),('द','da',True),('ध','dha',True)],
         [('न','na',True),('प','pa',True),('फ','pha',True),('ब','ba',True),
          ('भ','bha',True),('म','ma',True),('य','ya',True)],
     ],
     ('[ न ] + [ म ] + [ स ] + [ ् ] + [ त ] + [ े ]  →  नमस्ते', 'namaste = hello')),

    ('th', 'ไทย (Thai)', 'Thai', 44, 21, 0,
     [
         [('ก','k',True),('ข','kh',True),('ค','kh',True),('ง','ng',True),('จ','j',True),
          ('ฉ','ch',True),('ช','ch',True),('ซ','s',True),('ญ','y',True),('ด','d',True)],
         [('ต','t',True),('ถ','th',True),('ท','th',True),('น','n',True),('บ','b',True),
          ('ป','p',True),('ผ','ph',True),('ฝ','f',True),('พ','ph',True)],
         [('ม','m',True),('ย','y',True),('ร','r',True),('ล','l',True),
          ('ว','w',True),('ส','s',True),('ห','h',True)],
     ],
     ('[ ส ] + [ ว ] + [ ั ] + [ ส ] + [ ด ] + [ ี ]  →  สวัสดี', 'sawatdee = hello')),

    ('vi', 'Tiếng Việt', 'Latin+Tones', 22, 12, 6,
     [
         [('b','',True),('c','',True),('d','',True),('đ','',True),('g','',True),
          ('h','',True),('k','',True),('l','',True),('m','',True),('n','',True)],
         [('a','',False),('â','',False),('ă','',False),('e','',False),('ê','',False),
          ('i','',False),('o','',False),('ô','',False),('ơ','',False)],
         [('p','',True),('q','',True),('r','',True),('s','',True),
          ('t','',True),('u','',False),('ư','',False)],
     ],
     ('[ x ] + [ i ] + [ n ]  +  [ c ] + [ h ] + [ à ] + [ o ]  →  xin chào', 'xin chào = hello')),

    ('ko_sign', 'Korean Sign', 'Gesture', 30, 10, 0,
     [
         [('ㄱ','☝',True),('ㄴ','✌',True),('ㄷ','🤟',True),('ㄹ','🤙',True),('ㅁ','✊',True),
          ('ㅂ','🖐',True),('ㅅ','👌',True),('ㅇ','👊',True),('ㅈ','🤞',True),('ㅊ','👍',True)],
         [('ㅏ','→',False),('ㅓ','←',False),('ㅗ','↑',False),('ㅜ','↓',False),('ㅡ','—',False),
          ('ㅣ','|',False),('ㅐ','↗',False),('ㅔ','↘',False),('ㅑ','⇒',False)],
         [('ㅋ','',True),('ㅌ','',True),('ㅍ','',True),('ㅎ','',True),
          ('ㅛ','',False),('ㅠ','',False),('ㅢ','',False)],
     ],
     ('[ ㅎ ] + [ ㅏ ] + [ ㄴ ]  →  한 (수화)', 'Vibration mode compatible')),

    ('id', 'Bahasa Indonesia', 'Latin', 21, 5, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('n','',True),('p','',True),('r','',True),('s','',True)],
         [('t','',True),('v','',True),('w','',True),('y','',True),
          ('z','',True),('q','',True),('x','',True)],
     ],
     ('[ h ] + [ a ] + [ l ] + [ o ]  →  halo', 'halo = hello')),

    ('ms', 'Bahasa Melayu', 'Latin', 21, 5, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('n','',True),('p','',True),('r','',True),('s','',True)],
         [('t','',True),('v','',True),('w','',True),('y','',True),
          ('z','',True),('q','',True),('x','',True)],
     ],
     ('[ h ] + [ a ] + [ l ] + [ o ]  →  halo', 'halo = hello')),

    ('tl', 'Filipino (Tagalog)', 'Latin', 20, 5, 0,
     [
         [('b','',True),('k','',True),('d','',True),('g','',True),('h','',True),
          ('l','',True),('m','',True),('n','',True),('p','',True),('r','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('s','',True),('t','',True),('w','',True),('y','',True)],
         [('ng','',True),('ts','',True),('dy','',True),('ny','',True),
          ('f','',True),('j','',True),('c','',True)],
     ],
     ('[ k ] + [ u ] + [ m ] + [ u ] + [ s ] + [ t ] + [ a ]  →  kumusta', 'kumusta = hello')),

    ('my', 'မြန်မာ (Burmese)', 'Myanmar', 33, 12, 0,
     [
         [('က','ka',True),('ခ','kha',True),('ဂ','ga',True),('ဃ','gha',True),('င','nga',True),
          ('စ','sa',True),('ဆ','hsa',True),('ဇ','za',True),('ဈ','za',True),('ည','nya',True)],
         [('ဋ','ta',True),('ဌ','hta',True),('ဍ','da',True),('ဎ','dha',True),('ဏ','na',True),
          ('တ','ta',True),('ထ','hta',True),('ဒ','da',True),('ဓ','dha',True)],
         [('န','na',True),('ပ','pa',True),('ဖ','pha',True),('ဗ','ba',True),
          ('ဘ','bha',True),('မ','ma',True),('ယ','ya',True)],
     ],
     ('[ မ ] + [ င ] + [ ္ ] + [ ဂ ] + [ လ ] + [ ာ ]  →  မင်္ဂလာ', 'mingala = hello')),

    ('km', 'ខ្មែរ (Khmer)', 'Khmer', 33, 14, 0,
     [
         [('ក','ka',True),('ខ','kha',True),('គ','ko',True),('ឃ','kho',True),('ង','ngo',True),
          ('ច','ca',True),('ឆ','cha',True),('ជ','co',True),('ឈ','cho',True),('ញ','nyo',True)],
         [('ដ','da',True),('ឋ','tha',True),('ឌ','do',True),('ឍ','tho',True),('ណ','na',True),
          ('ត','ta',True),('ថ','tha',True),('ទ','to',True),('ធ','tho',True)],
         [('ន','no',True),('ប','ba',True),('ផ','pha',True),('ព','po',True),
          ('ភ','pho',True),('ម','mo',True),('យ','yo',True)],
     ],
     ('[ ស ] + [ ួ ] + [ ស ] + [ ្ ] + [ ដ ] + [ ី ]  →  សួស្ដី', 'suosdei = hello')),

    ('lo', 'ລາວ (Lao)', 'Lao', 28, 18, 4,
     [
         [('ກ','k',True),('ຂ','kh',True),('ຄ','kh',True),('ງ','ng',True),('ຈ','j',True),
          ('ສ','s',True),('ຊ','s',True),('ຍ','ny',True),('ດ','d',True),('ຕ','t',True)],
         [('ຖ','th',True),('ທ','th',True),('ນ','n',True),('ບ','b',True),('ປ','p',True),
          ('ຜ','ph',True),('ຝ','f',True),('ພ','ph',True),('ຟ','f',True)],
         [('ມ','m',True),('ຢ','y',True),('ຣ','r',True),('ລ','l',True),
          ('ວ','w',True),('ຫ','h',True),('ອ','o',True)],
     ],
     ('[ ສ ] + [ ະ ] + [ ບ ] + [ າ ] + [ ຍ ] + [ ດ ] + [ ີ ]  →  ສະບາຍດີ', 'sabaidi = hello')),

    ('bn', 'বাংলা (Bengali)', 'Bengali', 30, 11, 0,
     [
         [('ক','ka',True),('খ','kha',True),('গ','ga',True),('ঘ','gha',True),('ঙ','ṅa',True),
          ('চ','ca',True),('ছ','cha',True),('জ','ja',True),('ঝ','jha',True),('ঞ','ña',True)],
         [('ট','ṭa',True),('ঠ','ṭha',True),('ড','ḍa',True),('ঢ','ḍha',True),('ণ','ṇa',True),
          ('ত','ta',True),('থ','tha',True),('দ','da',True),('ধ','dha',True)],
         [('ন','na',True),('প','pa',True),('ফ','pha',True),('ব','ba',True),
          ('ভ','bha',True),('ম','ma',True),('র','ra',True)],
     ],
     ('[ ন ] + [ ম ] + [ স ] + [ ্ ] + [ ক ] + [ া ] + [ র ]  →  নমস্কার', 'namoskar = hello')),

    ('ta', 'தமிழ் (Tamil)', 'Tamil', 18, 12, 0,
     [
         [('க','ka',True),('ங','nga',True),('ச','ca',True),('ஞ','nya',True),('ட','ta',True),
          ('ண','na',True),('த','tha',True),('ந','na',True),('ப','pa',True),('ம','ma',True)],
         [('அ','a',False),('ஆ','aa',False),('இ','i',False),('ஈ','ii',False),('உ','u',False),
          ('ஊ','uu',False),('எ','e',False),('ஏ','ee',False),('ஒ','o',False)],
         [('ய','ya',True),('ர','ra',True),('ல','la',True),('வ','va',True),
          ('ழ','zha',True),('ள','la',True),('ற','ra',True)],
     ],
     ('[ வ ] + [ ண ] + [ க ] + [ ் ] + [ க ] + [ ம ] + [ ் ]  →  வணக்கம்', 'vanakkam = hello')),

    ('te', 'తెలుగు (Telugu)', 'Telugu', 36, 14, 0,
     [
         [('క','ka',True),('ఖ','kha',True),('గ','ga',True),('ఘ','gha',True),('ఙ','ṅa',True),
          ('చ','ca',True),('ఛ','cha',True),('జ','ja',True),('ఝ','jha',True),('ఞ','ña',True)],
         [('ట','ṭa',True),('ఠ','ṭha',True),('డ','ḍa',True),('ఢ','ḍha',True),('ణ','ṇa',True),
          ('త','ta',True),('థ','tha',True),('ద','da',True),('ధ','dha',True)],
         [('న','na',True),('ప','pa',True),('ఫ','pha',True),('బ','ba',True),
          ('భ','bha',True),('మ','ma',True),('య','ya',True)],
     ],
     ('[ న ] + [ మ ] + [ స ] + [ ్ ] + [ క ] + [ ా ] + [ ర ]  →  నమస్కారం', 'namaskaram = hello')),

    ('ur', 'اردو (Urdu)', 'Arabic+', 40, 10, 0,
     [
         [('ب','b',True),('پ','p',True),('ت','t',True),('ٹ','ṭ',True),('ث','s',True),
          ('ج','j',True),('چ','c',True),('ح','h',True),('خ','x',True),('د','d',True)],
         [('ڈ','ḍ',True),('ذ','z',True),('ر','r',True),('ڑ','ṛ',True),('ز','z',True),
          ('ژ','ž',True),('س','s',True),('ش','š',True),('ص','ṣ',True)],
         [('ض','ẓ',True),('ط','t',True),('ظ','z',True),('ع','ʿ',True),
          ('غ','ġ',True),('ف','f',True),('ق','q',True)],
     ],
     ('[ ا ] + [ س ] + [ ل ] + [ ا ] + [ م ]  →  السلام', 'assalam = peace')),

    # ─── 유럽 ───
    ('de', 'Deutsch (German)', 'Latin', 22, 8, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('ä','',False),('ö','',False),('ü','',False),('n','',True)],
         [('p','',True),('q','',True),('r','',True),('s','',True),
          ('t','',True),('v','',True),('w','',True)],
     ],
     ('[ h ] + [ a ] + [ l ] + [ l ] + [ o ]  →  hallo', 'hallo = hello')),

    ('fr', 'Français (French)', 'Latin', 20, 16, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('é','',False),('è','',False),('ê','',False),('n','',True)],
         [('p','',True),('q','',True),('r','',True),('s','',True),
          ('t','',True),('v','',True),('w','',True)],
     ],
     ('[ b ] + [ o ] + [ n ] + [ j ] + [ o ] + [ u ] + [ r ]  →  bonjour', 'bonjour = hello')),

    ('es', 'Español (Spanish)', 'Latin', 22, 5, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('l','',True),('m','',True),('n','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('ñ','',True),('p','',True),('q','',True),('r','',True)],
         [('rr','',True),('s','',True),('t','',True),('v','',True),
          ('x','',True),('y','',True),('z','',True)],
     ],
     ('[ h ] + [ o ] + [ l ] + [ a ]  →  hola', 'hola = hello')),

    ('pt', 'Português', 'Latin', 21, 9, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('l','',True),('m','',True),('n','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('ã','',False),('õ','',False),('é','',False),('ê','',False)],
         [('p','',True),('q','',True),('r','',True),('s','',True),
          ('t','',True),('v','',True),('z','',True)],
     ],
     ('[ o ] + [ l ] + [ á ]  →  olá', 'olá = hello')),

    ('it', 'Italiano (Italian)', 'Latin', 21, 7, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('l','',True),('m','',True),('n','',True),('p','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('è','',False),('ò','',False),('q','',True),('r','',True)],
         [('s','',True),('t','',True),('v','',True),('z','',True),
          ('gl','',True),('gn','',True),('sc','',True)],
     ],
     ('[ c ] + [ i ] + [ a ] + [ o ]  →  ciao', 'ciao = hello')),

    ('nl', 'Nederlands (Dutch)', 'Latin', 21, 6, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('ij','',False),('n','',True),('p','',True),('r','',True)],
         [('s','',True),('t','',True),('v','',True),('w','',True),
          ('x','',True),('y','',True),('z','',True)],
     ],
     ('[ h ] + [ a ] + [ l ] + [ l ] + [ o ]  →  hallo', 'hallo = hello')),

    ('pl', 'Polski (Polish)', 'Latin', 29, 8, 0,
     [
         [('b','',True),('c','',True),('ć','',True),('d','',True),('f','',True),
          ('g','',True),('h','',True),('j','',True),('k','',True),('l','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('ó','',False),('ą','',False),('ę','',False),('ł','',True)],
         [('m','',True),('n','',True),('ń','',True),('p','',True),
          ('r','',True),('s','',True),('ś','',True)],
     ],
     ('[ c ] + [ z ] + [ e ] + [ ś ] + [ ć ]  →  cześć', 'cześć = hello')),

    ('tr', 'Türkçe (Turkish)', 'Latin', 21, 8, 0,
     [
         [('b','',True),('c','',True),('ç','',True),('d','',True),('f','',True),
          ('g','',True),('ğ','',True),('h','',True),('j','',True),('k','',True)],
         [('a','',False),('e','',False),('ı','',False),('i','',False),('o','',False),
          ('ö','',False),('u','',False),('ü','',False),('l','',True)],
         [('m','',True),('n','',True),('p','',True),('r','',True),
          ('s','',True),('ş','',True),('t','',True)],
     ],
     ('[ m ] + [ e ] + [ r ] + [ h ] + [ a ] + [ b ] + [ a ]  →  merhaba', 'merhaba = hello')),

    ('el', 'Ελληνικά (Greek)', 'Greek', 17, 7, 0,
     [
         [('β','v',True),('γ','g',True),('δ','d',True),('ζ','z',True),('θ','th',True),
          ('κ','k',True),('λ','l',True),('μ','m',True),('ν','n',True),('ξ','x',True)],
         [('α','a',False),('ε','e',False),('η','i',False),('ι','i',False),('ο','o',False),
          ('υ','u',False),('ω','o',False),('π','p',True),('ρ','r',True)],
         [('σ','s',True),('τ','t',True),('φ','f',True),('χ','ch',True),
          ('ψ','ps',True),('ς','s',True)],
     ],
     ('[ γ ] + [ ε ] + [ ι ] + [ α ]  →  γεια', 'geia = hello')),

    ('uk', 'Українська (Ukrainian)', 'Cyrillic', 22, 10, 0,
     [
         [('б','b',True),('в','v',True),('г','h',True),('ґ','g',True),('д','d',True),
          ('ж','zh',True),('з','z',True),('к','k',True),('л','l',True),('м','m',True)],
         [('а','a',False),('е','e',False),('є','ye',False),('и','y',False),('і','i',False),
          ('ї','yi',False),('о','o',False),('у','u',False),('н','n',True)],
         [('п','p',True),('р','r',True),('с','s',True),('т','t',True),
          ('ф','f',True),('х','kh',True),('ц','ts',True)],
     ],
     ('[ п ] + [ р ] + [ и ] + [ в ] + [ і ] + [ т ]  →  привіт', 'pryvit = hello')),

    ('cs', 'Čeština (Czech)', 'Latin', 25, 10, 0,
     [
         [('b','',True),('c','',True),('č','',True),('d','',True),('ď','',True),
          ('f','',True),('g','',True),('h','',True),('j','',True),('k','',True)],
         [('a','',False),('á','',False),('e','',False),('é','',False),('ě','',False),
          ('i','',False),('í','',False),('o','',False),('ó','',False)],
         [('l','',True),('m','',True),('n','',True),('ň','',True),
          ('p','',True),('r','',True),('ř','',True)],
     ],
     ('[ a ] + [ h ] + [ o ] + [ j ]  →  ahoj', 'ahoj = hello')),

    ('ro', 'Română (Romanian)', 'Latin', 22, 7, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('ă','',False),('â','',False),('e','',False),('i','',False),
          ('î','',False),('o','',False),('n','',True),('p','',True)],
         [('r','',True),('s','',True),('ș','',True),('t','',True),
          ('ț','',True),('u','',False),('v','',True)],
     ],
     ('[ s ] + [ a ] + [ l ] + [ u ] + [ t ]  →  salut', 'salut = hello')),

    ('hu', 'Magyar (Hungarian)', 'Latin', 25, 14, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('á','',False),('e','',False),('é','',False),('i','',False),
          ('í','',False),('o','',False),('ó','',False),('ö','',False)],
         [('n','',True),('p','',True),('r','',True),('s','',True),
          ('t','',True),('v','',True),('z','',True)],
     ],
     ('[ s ] + [ z ] + [ i ] + [ a ]  →  szia', 'szia = hello')),

    ('sv', 'Svenska (Swedish)', 'Latin', 20, 9, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('y','',False),('å','',False),('ä','',False),('ö','',False)],
         [('n','',True),('p','',True),('r','',True),('s','',True),
          ('t','',True),('v','',True),('x','',True)],
     ],
     ('[ h ] + [ e ] + [ j ]  →  hej', 'hej = hello')),

    ('fi', 'Suomi (Finnish)', 'Latin', 18, 8, 0,
     [
         [('h','',True),('j','',True),('k','',True),('l','',True),('m','',True),
          ('n','',True),('p','',True),('r','',True),('s','',True),('t','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('y','',False),('ä','',False),('ö','',False),('v','',True)],
         [('d','',True),('g','',True),('b','',True),('f','',True),
          ('c','',True),('w','',True),('x','',True)],
     ],
     ('[ m ] + [ o ] + [ i ]  →  moi', 'moi = hello')),

    ('da', 'Dansk (Danish)', 'Latin', 20, 9, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('y','',False),('æ','',False),('ø','',False),('å','',False)],
         [('n','',True),('p','',True),('r','',True),('s','',True),
          ('t','',True),('v','',True),('x','',True)],
     ],
     ('[ h ] + [ e ] + [ j ]  →  hej', 'hej = hello')),

    ('no', 'Norsk (Norwegian)', 'Latin', 20, 9, 0,
     [
         [('b','',True),('c','',True),('d','',True),('f','',True),('g','',True),
          ('h','',True),('j','',True),('k','',True),('l','',True),('m','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('y','',False),('æ','',False),('ø','',False),('å','',False)],
         [('n','',True),('p','',True),('r','',True),('s','',True),
          ('t','',True),('v','',True),('x','',True)],
     ],
     ('[ h ] + [ e ] + [ i ]  →  hei', 'hei = hello')),

    # ─── 중동/아프리카 ───
    ('he', 'עברית (Hebrew)', 'Hebrew', 22, 5, 0,
     [
         [('א','a',False),('ב','b',True),('ג','g',True),('ד','d',True),('ה','h',True),
          ('ו','v',True),('ז','z',True),('ח','kh',True),('ט','t',True),('י','y',True)],
         [('כ','k',True),('ל','l',True),('מ','m',True),('נ','n',True),('ס','s',True),
          ('ע','',True),('פ','p',True),('צ','ts',True),('ק','q',True)],
         [('ר','r',True),('ש','sh',True),('ת','t',True),('','',''),
          ],
     ],
     ('[ ש ] + [ ל ] + [ ו ] + [ ם ]  →  שלום', 'shalom = hello')),

    ('fa', 'فارسی (Persian)', 'Arabic+', 32, 6, 0,
     [
         [('ب','b',True),('پ','p',True),('ت','t',True),('ث','s',True),('ج','j',True),
          ('چ','ch',True),('ح','h',True),('خ','x',True),('د','d',True),('ذ','z',True)],
         [('ر','r',True),('ز','z',True),('ژ','zh',True),('س','s',True),('ش','sh',True),
          ('ص','s',True),('ض','z',True),('ط','t',True),('ظ','z',True)],
         [('ع','',True),('غ','gh',True),('ف','f',True),('ق','q',True),
          ('ک','k',True),('گ','g',True),('ل','l',True)],
     ],
     ('[ س ] + [ ل ] + [ ا ] + [ م ]  →  سلام', 'salam = hello')),

    ('sw', 'Kiswahili (Swahili)', 'Latin', 24, 5, 0,
     [
         [('b','',True),('ch','',True),('d','',True),('dh','',True),('f','',True),
          ('g','',True),('gh','',True),('h','',True),('j','',True),('k','',True)],
         [('a','',False),('e','',False),('i','',False),('o','',False),('u','',False),
          ('l','',True),('m','',True),('n','',True),('ng','',True)],
         [('ny','',True),('p','',True),('r','',True),('s','',True),
          ('sh','',True),('t','',True),('th','',True)],
     ],
     ('[ h ] + [ a ] + [ b ] + [ a ] + [ r ] + [ i ]  →  habari', 'habari = hello')),

    ('am', 'አማርኛ (Amharic)', 'Ethiopic', 34, 7, 0,
     [
         [('ሀ','ha',True),('ለ','la',True),('ሐ','ha',True),('መ','ma',True),('ሠ','sa',True),
          ('ረ','ra',True),('ሰ','sa',True),('ሸ','sha',True),('ቀ','qa',True),('በ','ba',True)],
         [('ተ','ta',True),('ቸ','cha',True),('ኀ','ha',True),('ነ','na',True),('ኘ','nya',True),
          ('ከ','ka',True),('ወ','wa',True),('ዘ','za',True),('ዠ','zha',True)],
         [('የ','ya',True),('ደ','da',True),('ጀ','ja',True),('ገ','ga',True),
          ('ጠ','ta',True),('ጰ','pa',True),('ፈ','fa',True)],
     ],
     ('[ ሰ ] + [ ላ ] + [ ም ]  →  ሰላም', 'selam = hello')),

    # ─── 기타 주요 언어 ───
    ('ka', 'ქართული (Georgian)', 'Georgian', 28, 5, 0,
     [
         [('ბ','b',True),('გ','g',True),('დ','d',True),('ვ','v',True),('ზ','z',True),
          ('თ','t',True),('კ','k',True),('ლ','l',True),('მ','m',True),('ნ','n',True)],
         [('ა','a',False),('ე','e',False),('ი','i',False),('ო','o',False),('უ','u',False),
          ('პ','p',True),('ჟ','zh',True),('რ','r',True),('ს','s',True)],
         [('ტ','t',True),('ფ','p',True),('ქ','k',True),('ღ','gh',True),
          ('ყ','q',True),('შ','sh',True),('ჩ','ch',True)],
     ],
     ('[ გ ] + [ ა ] + [ მ ] + [ ა ] + [ რ ] + [ ჯ ] + [ ო ] + [ ბ ] + [ ა ]  →  გამარჯობა', 'gamarjoba = hello')),

    ('hy', 'Հայերեն (Armenian)', 'Armenian', 30, 6, 0,
     [
         [('Բ','b',True),('Գ','g',True),('Դ','d',True),('Զ','z',True),('Թ','t',True),
          ('Ժ','zh',True),('Լ','l',True),('Խ','kh',True),('Կ','k',True),('Հ','h',True)],
         [('Ա','a',False),('Է','e',False),('Ի','i',False),('Ո','o',False),('Ու','u',False),
          ('Մ','m',True),('Յ','y',True),('Ն','n',True),('Շ','sh',True)],
         [('Պ','p',True),('Ջ','j',True),('Ռ','r',True),('Ս','s',True),
          ('Վ','v',True),('Տ','t',True),('Փ','p',True)],
     ],
     ('[ Բ ] + [ ա ] + [ ր ] + [ և ]  →  Բարև', 'barev = hello')),

    ('mn', 'Монгол (Mongolian)', 'Cyrillic', 20, 7, 0,
     [
         [('б','b',True),('в','v',True),('г','g',True),('д','d',True),('ж','j',True),
          ('з','z',True),('к','k',True),('л','l',True),('м','m',True),('н','n',True)],
         [('а','a',False),('э','e',False),('и','i',False),('о','o',False),('у','u',False),
          ('ө','ö',False),('ү','ü',False),('п','p',True),('р','r',True)],
         [('с','s',True),('т','t',True),('ф','f',True),('х','kh',True),
          ('ц','ts',True),('ч','ch',True),('ш','sh',True)],
     ],
     ('[ с ] + [ а ] + [ й ] + [ н ]  →  сайн', 'sain = hello')),
]

# 총 언어 수 (6 기본 + lang_data)
LANG_COUNT = 6 + len(LANGUAGES)
