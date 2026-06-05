# claude-proxy

HTTP-обёртка над Claude Code CLI. Позволяет другим сервисам на VPS обращаться к Claude через простой REST API, не устанавливая CLI в каждый контейнер.

## Эндпоинты

### `POST /complete`

Отправляет запрос в Claude и возвращает текстовый ответ.

**Тело запроса:**
```json
{
  "prompt": "Текст запроса",
  "system": "Системный промпт (необязательно)"
}
```

**Ответ:**
```json
{
  "content": "Ответ модели"
}
```

### `GET /health`

Проверка работоспособности сервиса.

## Запуск

```bash
docker compose up -d --build
```

Сервис поднимается на порту **8100**.

## Авторизация Claude

После первого запуска нужно авторизоваться один раз — авторизация сохраняется в Docker volume `claude-home` и переживает перезапуски контейнера.

```bash
docker exec -it claude-proxy claude /login
```

Следуй инструкциям в терминале (открытие ссылки в браузере).

## Использование из других контейнеров

Из контейнеров на том же Docker-хосте обращайтесь по имени хоста VPS или через `host.docker.internal`:

```bash
curl -X POST http://<VPS_IP>:8100/complete \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Привет!", "system": "Отвечай кратко."}'
```

## Обновление

```bash
git pull
docker compose up -d --build
```
