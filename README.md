# learn-from-video

Скилл для Claude Code: захват знаний из YouTube-видео в базу знаний [Second Brain](https://github.com/Alex-Fintore/second-brain).

## Что делает

1. Получает транскрипцию YouTube-видео (субтитры через `youtube-transcript-api`)
2. Извлекает метаданные — название и канал (через `yt-dlp`)
3. Анализирует контент и структурирует знания
4. При необходимости задаёт уточняющие вопросы
5. Сохраняет запись в `Knowledge/youtube/YYYY-MM-DD-slug.md` с тегами
6. Логирует событие в `history.md`

## Установка

```bash
pip install youtube-transcript-api yt-dlp
```

Скилл кладётся в директорию скиллов Claude Code:

```
~/.claude/skills/learn-from-video/
├── SKILL.md
└── scripts/
    └── get_transcript.py
```

## Использование

Просто скинь ссылку на YouTube в чат Claude Code — скилл сработает автоматически:

```
https://www.youtube.com/watch?v=...
```

Или явно:
```
добавь это видео в базу знаний: https://youtu.be/...
```

## Формат записи в базе знаний

```markdown
---
title: "Название видео"
tags: [ai, productivity, tools]
source: youtube
channel: "Название канала"
url: https://www.youtube.com/watch?v=...
date: 2026-03-14
---

## Суть
## Ключевые инсайты
## Как применить
## Открытые вопросы
```

## Зависимости

| Пакет | Назначение |
|-------|-----------|
| `youtube-transcript-api` | Извлечение субтитров/транскрипции |
| `yt-dlp` | Метаданные видео (название, канал) |
