import logging
import os

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import random

# Включим логирование, чтобы видеть возможные ошибки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_KEY')

# Вопрос и эталонный ответ
QUESTION = "Назовите пять основных встроенных типов данных в Python."
CORRECT_ANSWER = "числа строки списки кортежи словари"
# Приводим эталонный ответ к нижнему регистру и убираем лишние символы для сравнения

# Списки для симуляции анализа "уверенности"
CONFIDENCE_INDICATORS = {
    "high": ["уверенно", "четко", "без пауз", "ровным голосом"],
    "low": ["с паузами", "неуверенно", "тихим голосом", "с запинками"]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start. Приветствует пользователя и предлагает начать."""
    keyboard = [['🎤 Получить вопрос']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Я бот для проверки знаний.\n"
        "Нажми кнопку ниже, чтобы получить вопрос и ответить на него голосовым сообщением.",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений. Реагирует только на кнопку."""
    user_message = update.message.text

    if user_message == '🎤 Получить вопрос':
        # Сохраняем вопрос в контекст пользователя, чтобы потом проверить ответ
        context.user_data['awaiting_voice'] = True
        # Отправляем вопрос пользователю
        await update.message.reply_text(
            f"Вопрос:\n\n**{QUESTION}**\n\nТеперь отправь свой ответ голосовым сообщением!",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove() # Убираем клавиатуру после выбора
        )
    else:
        await update.message.reply_text("Нажми 'Получить вопрос', чтобы начать.")

def simulate_speech_to_text(voice_file):
    """
    Функция-заглушка для преобразования голоса в текст.
    В реальности здесь будет код для отправки файла в OpenAI Whisper API или другой ASR-сервис.
    """
    # Для демонстрации просто возвращаем фиктивный, иногда неверный, ответ.
    simulated_answers = [
        "числа строки списки кортежи словари",
        "числа строки списки кортежи множества", # Ошибка
        "числа строки списки словари", # Не хватает кортежей
        "я не знаю" # Полная неудача
    ]
    # Давайте чаще возвращать правильный ответ для наглядности
    weights = [0.6, 0.15, 0.15, 0.1]
    return random.choices(simulated_answers, weights=weights, k=1)[0]

def analyze_answer(recognized_text):
    """
    Анализирует распознанный текст.
    1. Проверяет правильность ответа.
    2. Генерирует "оценку уверенности" (для демонстрации).
    """
    # Приводим распознанный текст к нижнему регистру для сравнения
    recognized_text_lower = recognized_text.lower()

    # 1. Проверка правильности
    # Простейшая проверка: есть ли все ключевые слова из эталонного ответа?
    correct_keywords = set(CORRECT_ANSWER.split())
    user_keywords = set(recognized_text_lower.split())
    matched_keywords = correct_keywords.intersection(user_keywords)

    correctness_score = len(matched_keywords) / len(correct_keywords)

    # 2. "Анализ" уверенности (симуляция)
    # В реальности это мог бы быть анализ аудиофайла (тон, паузы, амплитуда)
    # Здесь просто случайный выбор с уклоном в уверенность при правильном ответе
    if correctness_score > 0.7:
        confidence_level = "high"
        confidence_comment = random.choice(CONFIDENCE_INDICATORS["high"])
    else:
        confidence_level = "low"
        confidence_comment = random.choice(CONFIDENCE_INDICATORS["low"])

    # 3. Формируем фидбэк
    feedback = f"*Распознанный текст:* {recognized_text}\n\n"
    feedback += f"*Правильность ответа:* {correctness_score:.0%}\n"
    if correctness_score == 1:
        feedback += "✅ Отличный ответ! Все верно.\n"
    elif correctness_score > 0.5:
        feedback += "⚠️ Неплохо, но есть неточности.\n"
        missing = correct_keywords - user_keywords
        if missing:
            feedback += f"*Не хватило:* {', '.join(missing)}\n"
    else:
        feedback += "❌ Ответ неверный или очень неточный.\n"
        feedback += f"*Ждали:* {CORRECT_ANSWER.replace(' ', ', ')}\n"

    feedback += f"\n*Анализ речи:* Вы ответили {confidence_comment}.\n"
    feedback += f"*Уровень уверенности:* {confidence_level}"

    return feedback

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик голосовых сообщений."""
    # Проверяем, ждал ли бот голосового ответа на вопрос
    if not context.user_data.get('awaiting_voice'):
        await update.message.reply_text("Сначала нажми 'Получить вопрос'.")
        return

    # Сбрасываем флаг
    context.user_data['awaiting_voice'] = False

    # Сообщаем, что началась обработка
    processing_msg = await update.message.reply_text("🎧 Обрабатываю голос...")

    # Получаем файл голосового сообщения
    voice_file = await update.message.voice.get_file()

    # В РЕАЛЬНОМ БОТЕ: Здесь нужно скачать файл (await voice_file.download_to_drive('voice.ogg'))
    # и отправить его в API для распознавания речи (например, OpenAI Whisper).

    # Симулируем распознавание речи
    recognized_text = simulate_speech_to_text(voice_file)

    # Анализируем ответ
    analysis_result = analyze_answer(recognized_text)

    # Удаляем сообщение об обработке
    await processing_msg.delete()

    # Отправляем пользователю полный разбор
    await update.message.reply_text(
        f"**Результат анализа:**\n\n{analysis_result}\n\n"
        "Нажми /start, чтобы попробовать еще раз.",
        parse_mode='Markdown'
    )

def main():
    """Главная функция для запуска бота."""
    # Создаем Application и передаем ему токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()