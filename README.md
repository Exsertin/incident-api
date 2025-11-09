# incident-api

Простой Django REST API для учёта инцидентов.

---

## 🚀 Запуск

```bash
git clone https://github.com/Exsertin/incident-api.git
cd incident-api
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```

## 🚀 Для запуска тестов

```bash
docker-compose exec web python manage.py test
```

## Эндпоинты

1. Создать инцидент

**POST /api/incidents**

```json
{
  "description": "Точка А не отвечает",
  "source": "monitoring"
}
```
Response
```json
{
  "id": 1,
  "description": "Точка А не отвечает",
  "status": "open",
  "source": "monitoring",
  "created_at": "2025-11-07T10:00:00Z"
}

```

2. Получить список (с фильтром по статусу)

**GET /api/incidents?status=open**

Response
```json
{
  "id": 1,
  "description": "Точка А не отвечает",
  "status": "open",
  "source": "monitoring",
  "created_at": "2025-11-07T10:00:00Z"
}

```
3. Обновить статус

**PATCH /api/incidents/1/status**

```json
{
  "status": "resolved"
}
```
Response
```json
{
  "id": 1,
  "description": "Точка А не отвечает",
  "status": "resolved",
  "source": "monitoring",
  "created_at": "2025-11-07T10:00:00Z"
}
```
