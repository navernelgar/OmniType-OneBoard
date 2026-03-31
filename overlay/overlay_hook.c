/**
 * overlay_hook.c — OmniType 게임 오버레이 (DLL 후킹)
 * =====================================================
 * DirectX 11 SwapChain.Present 후킹 + 텍스트 오버레이
 *
 * 구조:
 *   1. DLL Injection → 게임 프로세스에 로드
 *   2. IDXGISwapChain::Present 후킹
 *   3. Present 호출 시 자막 텍스트 렌더링
 *   4. 공유 메모리로 번역 엔진과 통신
 *
 * 빌드: gcc -shared -o omnitype_overlay.dll overlay_hook.c -ld3d11 -ldxgi
 *
 * 이수진 / 2026-03-31
 */

#include <windows.h>
#include <stdio.h>
#include <stdint.h>

/* ═══ 공유 메모리 구조 ═══ */
#define SHARED_MEM_NAME "OmniTypeOverlay"
#define MAX_SUBTITLE_LEN 512
#define MAX_LINES 4

typedef struct {
    int     active;                          /* 오버레이 활성화 */
    int     position;                        /* 0=bottom, 1=top */
    float   opacity;                         /* 0.0~1.0 */
    int     font_size;                       /* 자막 폰트 크기 */
    int     line_count;                      /* 자막 줄 수 */
    wchar_t lines[MAX_LINES][MAX_SUBTITLE_LEN]; /* 자막 텍스트 (유니코드) */
    wchar_t genre[64];                       /* 현재 장르 덱 */
    int     correction_mode;                 /* 커뮤니티 보정 모드 */
} OverlayState;

static OverlayState* g_state = NULL;
static HANDLE g_shared_mem = NULL;

/* ═══ 공유 메모리 초기화 ═══ */
static int init_shared_memory(void) {
    g_shared_mem = CreateFileMappingW(
        INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE,
        0, sizeof(OverlayState), L"OmniTypeOverlay"
    );

    if (!g_shared_mem) return 0;

    g_state = (OverlayState*)MapViewOfFile(
        g_shared_mem, FILE_MAP_ALL_ACCESS,
        0, 0, sizeof(OverlayState)
    );

    if (!g_state) {
        CloseHandle(g_shared_mem);
        return 0;
    }

    /* 기본값 */
    if (g_state->font_size == 0) {
        g_state->active = 1;
        g_state->position = 0;  /* bottom */
        g_state->opacity = 0.75f;
        g_state->font_size = 18;
        g_state->line_count = 0;
        wcscpy(g_state->genre, L"general");
    }

    return 1;
}

/* ═══ 자막 업데이트 (Python 번역 엔진에서 호출) ═══ */
__declspec(dllexport)
void set_subtitle(int line_idx, const wchar_t* text) {
    if (!g_state || line_idx < 0 || line_idx >= MAX_LINES) return;
    wcsncpy(g_state->lines[line_idx], text, MAX_SUBTITLE_LEN - 1);
    if (line_idx >= g_state->line_count) {
        g_state->line_count = line_idx + 1;
    }
}

__declspec(dllexport)
void clear_subtitles(void) {
    if (!g_state) return;
    g_state->line_count = 0;
    for (int i = 0; i < MAX_LINES; i++) {
        g_state->lines[i][0] = L'\0';
    }
}

__declspec(dllexport)
void set_genre(const wchar_t* genre) {
    if (!g_state) return;
    wcsncpy(g_state->genre, genre, 63);
}

__declspec(dllexport)
void set_overlay_active(int active) {
    if (!g_state) return;
    g_state->active = active;
}

__declspec(dllexport)
void set_overlay_position(int pos) {
    if (!g_state) return;
    g_state->position = pos;
}

__declspec(dllexport)
void set_overlay_opacity(float opacity) {
    if (!g_state) return;
    g_state->opacity = opacity;
}

/* ═══ DLL 진입점 ═══ */
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            DisableThreadLibraryCalls(hinstDLL);
            init_shared_memory();
            break;

        case DLL_PROCESS_DETACH:
            if (g_state) {
                UnmapViewOfFile(g_state);
                g_state = NULL;
            }
            if (g_shared_mem) {
                CloseHandle(g_shared_mem);
                g_shared_mem = NULL;
            }
            break;
    }
    return TRUE;
}
