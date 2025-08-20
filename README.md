# OnyxMentorBot

> AI-тренер нового поколения для комплексной подготовки к собеседованиям. Анализирует не только то, *что* вы говорите, но и *как* вы это говорите, давая детальную обратную связь по hard и soft skills.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)

🌐 **Live Demo:** Бот в Telegram (скоро) | 📊 **Веб-панель:** Админка (скоро)

## 🚀 Возможности

*   **🎤 Голосовой анализ:** Оценка темпа речи, уверенности, пауз и манеры подачи.
*   **📝 Контент-анализ:** Проверка точности, полноты и структуры ответов с помощью LLM (GPT, Mistral).
*   **🎯 Персонализация:** Подготовка к конкретным компаниям и ролям (Data Science, Backend, ML Engineer).
*   **📊 Детальные отчеты:** PDF-отчеты с визуализацией сильных и слабых сторон.
*   **👥 Режим для HR:** Корпоративные аккаунты для массового скрининга кандидатов.

## 🛠 Технологический стек

| Компонент               | Технологии                                                                 |
| ----------------------- | -------------------------------------------------------------------------- |
| **Backend**             | FastAPI, SQLAlchemy, Pydantic, Celery, Uvicorn                             |
| **Базы данных**         | PostgreSQL (основная), Redis (кеш, Celery broker)                          |
| **Frontend (админка)**  | React + TypeScript + Vite (в будущем)                                      |
| **Телеграм-бот**        | Aiogram 3.x (асинхронный)                                                  |
| **AI/ML**               | OpenAI Whisper/API, Hugging Face Transformers, LangChain, librosa, pyAudioAnalysis |
| **Хранение данных**     | Amazon S3 / Yandex Cloud Storage / MinIO                                   |
| **Деплой**              | Docker, Docker Compose, Kubernetes (prod), Nginx                           |
| **Мониторинг**          | Prometheus, Grafana, ELK Stack                                             |

## 📦 Быстрый старт (Разработка)

### Предварительные требования

*   Python 3.10+
*   Docker и Docker Compose
*   Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
*   OpenAI API Key (опционально для некоторых функций)

### 1. Клонирование и настройка

```bash
git clone https://github.com/your-username/onyxmentorbot.git
cd onyxmentorbot
cp .env.example .env
```
### 2. Запуск через Docker Compose

```bash
docker-compose -f infrastructure/docker-compose.dev.yml up --build
```
### Сервисы будут доступны:

*  Backend API: http://localhost:8000
*  Docs (Swagger UI): http://localhost:8000/docs
*  Adminer (для БД): http://localhost:8080
*  Telegram Bot: Запущен и ожидает сообщений

## 🧪 Использование API

### Пример запроса на анализ ответа

```python
import requests

url = "http://localhost:8000/api/v1/analyze/response"
payload = {
    "user_id": 123,
    "interview_id": 456,
    "audio_url": "https://storage.onyxmentor.ru/audio/sample.mp3",
    "question_id": "sql_junior_1"
}

headers = {"Authorization": "Bearer YOUR_JWT_TOKEN"}
response = requests.post(url, json=payload, headers=headers)
print(response.json())
```
## 🗂 Структура проекта

| Директория | Описание |
|------------|----------|
| **onyxmentorbot/** | |
| ├── **backend/** | FastAPI приложение |
| ├── **bot/** | Telegram бот (Aiogram) |
| ├── **ml_service/** | Микросервис для ML задач |
| ├── **infrastructure/** | Docker, k8s манифесты |
| ├── **shared/** | Общие модели и утилиты |
| └── **README.md** | |

## 🤝 Как внести свой вклад

Мы приветствуем вклад в развитие проекта!

Сделайте форк репозитория

Создайте feature-ветку 
```bash
(git checkout -b feature/AmazingFeature)
```
Закоммитьте изменения 
```bash
(git commit -m 'Add some AmazingFeature')
```
Запушите ветку 
```bash
(git push origin feature/AmazingFeature)
```
Откройте Pull Request
