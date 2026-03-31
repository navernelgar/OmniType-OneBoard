# OmniType Game Overlay — Genre Deck Spec
# 장르별 게임 용어 사전 (.kn 확장)

## 구조

```
사전 우선순위:
  1순위: game_specific.kn  (그 게임 고유 용어)
  2순위: genre.kn          (장르 공통 용어)
  3순위: base_dict         (일상어 10만)
```

## 후킹 방식

### 텍스트 캡처
- DirectX 11/12: ID3D11DeviceContext::DrawText 후킹
- Vulkan: vkCmdDrawIndexed 텍스트 렌더링 감지
- Unity: TextMeshPro / UGUI Text 컴포넌트 후킹
- Unreal: UTextBlock / Slate 위젯 후킹

### 음성 캡처
- WASAPI: IAudioCaptureClient 게임 오디오 루프백
- 음성 분리: 음악/효과음에서 대사만 추출 (주파수 필터 80-3000Hz)
- 음소 분해: OmniType K^n 인코더로 실시간 변환

### 오버레이 렌더링
- IDXGISwapChain::Present 후킹
- 반투명 자막바 (위치/크기/투명도 조절 가능)
- 입력 패스스루 (WM_INPUT 안 가로챔)

## 장르 덱 목록

### 선협 (仙侠/Xianxia) — xianxia.kn
| 원문 | 일반 뜻 | 선협 뜻 |
|------|---------|---------|
| 炉鼎 | 솥/화로 | 쌍수 도구 (여성 비하) |
| 道侣 | 도반 | 수련 파트너/배우자 |
| 筑基 | 기초 세우기 | 수련 2단계 |
| 金丹 | 금색 알약 | 수련 3단계 |
| 元婴 | 원래 아기 | 수련 4단계 (분신) |
| 化神 | 신이 되다 | 수련 5단계 |
| 灵石 | 영적인 돌 | 화폐 (골드) |
| 灵根 | 영적인 뿌리 | 수련 재능/속성 |
| 天劫 | 하늘의 재앙 | 승급 시험 (번개) |
| 飞升 | 날아 오르다 | 선계로 승천 (최종) |
| 双修 | 함께 수련 | 쌍수 (성적 의미 포함) |
| 丹药 | 약 | 수련용 알약 |
| 法宝 | 보물 | 무기/아이템 |
| 宗门 | 종파 | 길드/클랜 |
| 掌门 | 장문 | 길드장 |
| 内门 | 안쪽 문 | 정식 제자 (핵심) |
| 外门 | 바깥 문 | 수습 제자 (외곽) |
| 秘境 | 비밀 경계 | 던전/레이드 |

### 무협 (武侠/Wuxia) — wuxia.kn
| 원문 | 일반 뜻 | 무협 뜻 |
|------|---------|---------|
| 内功 | 내부 공 | 내공 (기 수련) |
| 轻功 | 가벼운 공 | 경공 (공중 이동) |
| 点穴 | 점 혈 | 혈도 찌르기 (마비) |
| 掌法 | 손바닥 법 | 장법 (손바닥 무공) |
| 剑法 | 칼 법 | 검법 |
| 暗器 | 어두운 기구 | 암기 (숨겨진 무기) |
| 江湖 | 강과 호수 | 무림 세계 |
| 侠客 | 의로운 손님 | 무협 주인공 |
| 武林盟主 | 무림 맹주 | 무림의 리더 |

### FPS — fps.kn
| 원문 | 번역 |
|------|------|
| camp | 캠핑/자리잡기 |
| nerf | 하향 패치 |
| buff | 상향 패치/버프 |
| frag | 킬 |
| clutch | 클러치 (1vs다수 승리) |
| peek | 피킹 (코너에서 살짝 봄) |
| wallbang | 벽관통 사격 |
| spray | 난사/스프레이 |
| one-tap | 원탭 (헤드샷 원킬) |
| rotate | 로테이션 (포지션 이동) |
| callout | 위치 보고 |
| push | 진격/돌격 |

### MOBA — moba.kn
| 원문 | 번역 |
|------|------|
| gank | 기습 |
| lane | 라인 |
| jungle | 정글링 |
| feed | 먹여주기 (적에게) |
| carry | 캐리 |
| support | 서포터 |
| tower dive | 타워 다이브 |
| baron/dragon | 바론/용 |
| ward | 와드 (시야) |
| CS | 미니언 처치 수 |
| CC | 군중 제어 |
| ult | 궁극기 |

### RPG — rpg.kn
| 원문 | 번역 |
|------|------|
| aggro | 어그로 (적 관심) |
| DPS | 딜러 |
| tank | 탱커 |
| healer | 힐러 |
| proc | 발동 (확률 효과) |
| loot | 전리품 |
| raid | 레이드 (대규모 공격) |
| dungeon | 던전 |
| NPC | 비플레이어 캐릭터 |
| quest | 퀘스트 |
| grind | 노가다 |
| meta | 메타 (최적 전략) |

### 비주얼 노벨 — vn.kn
| 원문 | 번역 |
|------|------|
| route | 루트 (스토리 분기) |
| flag | 플래그 (조건 충족) |
| ending | 엔딩 |
| heroine | 히로인 |
| true end | 트루 엔딩 |
| bad end | 배드 엔딩 |
| CG | 이벤트 일러스트 |
| affection | 호감도 |
| choice | 선택지 |

## 커뮤니티 확장

장르 덱은 사용자가 추가/수정 가능:
1. Custom Mode에서 장르 덱 선택
2. 나무위키/위키 크롤링 → 자동 카드 생성 (/learn 연동)
3. 커뮤니티 공유 (Steam Workshop 또는 GitHub)

## .kn 장르 파일 포맷

기존 .kn에 context 필드 추가:
```
[header]
  magic: KN01
  lang: zh
  context: xianxia  ← 장르 태그 추가

[entries]
  key: 炉鼎
  meaning_default: 솥/화로
  meaning_context: 쌍수 도구로 쓰이는 여성
  tags: [derogatory, cultivation, female]
```
