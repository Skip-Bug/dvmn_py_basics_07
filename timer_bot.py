import os
import ptbot
from pytimeparse import parse
from dotenv import load_dotenv
load_dotenv('tg_acsess.env')
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

bot = ptbot.Bot(TG_TOKEN)


def main(chat_id, question):
    seconds = parse(question)
    if not seconds:
        bot.send_message(chat_id, """Не правильно заданно время,
        пиши : 5s, 5m, или 1h""")
        return
    progress_barr = render_progressbar(seconds, 0)
    message_id = bot.send_message(chat_id, f"""Запускаю таймер...\n
                                {progress_barr}""")
    bot.create_countdown(
        seconds, notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total_seconds=seconds
        )
    bot.create_timer(seconds, timer, chat_id=chat_id, message=question)


def notify_progress(secs_left, chat_id, message_id, total_seconds):
    progress_barr = render_progressbar(total_seconds, total_seconds - secs_left)
    minutes = secs_left // 60
    seconds = secs_left % 60
    if minutes > 0 and seconds > 0:
        time_text = f"{minutes} мин {seconds} сек"
    elif minutes > 0:
        time_text = f"{minutes} мин"
    else:
        time_text = f"{seconds} сек"
    bot.update_message(chat_id, message_id, f"Осталось {time_text} !\n {progress_barr}")


def timer(chat_id, message):
    answer = "Время вышло"
    bot.send_message(chat_id, answer)
    print("Мне написал пользователь с ID:", chat_id)
    print("Он спрашивал:", message)
    print("Я ответил:", answer)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


bot.reply_on_message(main)
print("Бот-таймер запущен.")
bot.run_bot()

if __name__ == '__main__':
    main()
