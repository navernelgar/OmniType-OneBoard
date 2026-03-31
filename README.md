# OmniType OneBoard

**One Keyboard, Every Language.**

195+ languages, one input system. Consonant + Vowel + Select.

## What is this?

OmniType OneBoard is a universal keyboard input system that maps all human languages to a single phoneme-based encoding. Same sound = same key, regardless of language.

## How it works

1. **Press C** — Consonant key (same sound = same key across all languages)
2. **Press V** — Vowel key (C + V = one syllable)
3. **Pick** — If multiple characters share the same sound, number key selects. Korean needs no picking.
4. **Switch** — One hotkey cycles through all languages

## Features

- **195+ languages** supported via `.kn` language files
- **7-bit encoding** per phoneme (~200 bytes per language)
- **Zero extra drivers** — works on any device
- **Assembly-level compatibility** — runs on legacy hardware
- **Safety limiter** built-in (blocks infrasound/ultrasound/weapon patterns)
- **Syntax Symphony** — text-to-music synthesis engine

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
