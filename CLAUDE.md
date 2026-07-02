# CLAUDE.md — claude-proxy

HTTP-обёртка (FastAPI) над Claude Code CLI: другие сервисы на VPS дёргают Claude
через REST, не ставя CLI у себя. Общая инфра (VPS, git, деплой) — в корневом
`../CLAUDE.md`. Архитектура — в [`README.md`](README.md).

## Суть
- `POST /complete` `{prompt, system?}` → `{content}`. Внутри — `subprocess` вызов
  `claude -p <prompt>` (см. `main.py`). `system` просто склеивается с промптом.
- `GET /health`.
- Контракт ошибок: 503 (CLI не найден), 504 (таймаут 300с), 502 (ненулевой код CLI).

## Запуск / деплой
- `docker compose up -d --build`. Сервис на порту **8100** (внутри контейнера 8000).
- Контейнер: `claude-proxy`. В docker-сети к нему обращаются как `claude-proxy:8000`.

## Ловушки
- **Авторизация Claude — один раз вручную** после первого запуска; хранится в volume
  `claude-config` (`/root`) и переживает рестарты. Не удалять volume.
- `ANTHROPIC_API_KEY` опционален (если не через подписку CLI) — пробрасывается из env.
- Зависимости минимальны (`fastapi`, `uvicorn`, `pydantic`) — не раздувать.