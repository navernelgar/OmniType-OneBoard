# OmniType OneBoard

**One Keyboard, Every Language.**

195+ languages, one input system. Just type — like Korean and English.

## What is this?

OmniType OneBoard is a universal keyboard input system. Same sound = same key, regardless of language. Type in any language the way you already type in Korean or English.

## How it works

Just type like you normally do.

- In Korean, you type ㄱ + ㅏ = 가. That's it.
- In English, you type h + i = hi. Same thing.
- In Japanese, same keys make the same sounds: か, さ, た...
- **Same sound = same key, any language.**

When multiple characters share the same sound (like Chinese tones), press a number key to pick. Korean and English don't need this step.

### Language switching

- **한/영 key + number** = select language (1=Korean, 2=English, 3=Japanese...)
- **한/영 key again** (without number) = back to Korean/English
- Just like the 한/영 toggle you already know, extended to 195+ languages.

## Features

- **195+ languages** supported via `.kn` language files
- **7-bit encoding** per phoneme (~200 bytes per language)
- **Zero extra drivers** — works on any device
- **Assembly-level compatibility** — runs on legacy hardware
- **Safety limiter** built-in (blocks infrasound/ultrasound/weapon patterns)
- **Syntax Symphony** — text-to-music synthesis engine

### Accessibility

- **Vibration mode** — haptic feedback for deaf-blind users. Same C/V phoneme pattern mapped to vibration sequences
- **On/Off toggle** — each feature (sound, vibration, visual keyboard) can be toggled independently
- **Settings saved** — user preferences stored locally, restored on restart
- **System tray icon** — minimize to tray, quick toggle via icon click or 한/영+Shift

## Language Files (.kn)

Pre-mapped binary files in `langs/`:

| File | Language | Phonemes | C/V | Homophones |
|------|----------|----------|-----|------------|
| ko.kn | Korean | 26 | 14/12 | 0 |
| en.kn | English | 26 | 21/5 | 0 |
| ja.kn | Japanese | 15 | 10/5 | 30 |
| zh.kn | Chinese | 27 | 21/6 | 4+ |
| ar.kn | Arabic | 31 | 28/3 | 0 |
| ru.kn | Russian | 31 | 21/10 | 0 |

> Korean has **0 homophones** — jamo combination uniquely determines every character. No number key needed.

## Demo

Open `docs/index.html` in a browser for an interactive demo with 6 languages.

## Structure

```
OmniType_OneBoard/
├── README.md
├── LICENSE
├── langs/          # Pre-mapped language files (.kn binary)
├── docs/           # Portfolio & demo
└── assets/         # Syntax Symphony audio
```

## License

Copyright (c) 2026 Lee Sujin. All rights reserved.

This software is proprietary. The `.kn` language data files are provided for evaluation purposes only. Redistribution, reverse engineering, or commercial use without explicit permission is prohibited.

## Contact

GitHub: [@navernelgar](https://github.com/navernelgar)
