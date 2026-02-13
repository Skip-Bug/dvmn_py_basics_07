import os
import ptbot
from pytimeparse import parse
from dotenv import load_dotenv


load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")


def connect_bot(token):
    bot = ptbot.Bot(token)
    return bot


def wait(chat_id, question, bot):
    seconds = parse(question)

    if not seconds:
        bot.send_message(chat_id, """Не правильно заданно время,
        пиши: 5s, 5m, или 1h""")
        return
    progress_barr = render_progressbar(seconds, 0)
    message_id = bot.send_message(
        chat_id, f"Запускаю таймер...\n{progress_barr}"
    )

    def progress_callback(secs_left):
        notify_progress(secs_left, chat_id, message_id, seconds, bot)

    def timer_callback():
        timer(chat_id, question, bot)

    bot.create_countdown(seconds, progress_callback)
    bot.create_timer(seconds, timer_callback)


def notify_progress(secs_left, chat_id, message_id, total_seconds, bot):
    progress = total_seconds - secs_left
    progress_barr = render_progressbar(total_seconds, progress)
    minutes = secs_left // 60
    seconds = secs_left % 60

    if minutes > 0 and seconds > 0:
        time_text = f"{minutes} мин {seconds} сек"
    elif minutes > 0:
        time_text = f"{minutes} мин"
    else:
        time_text = f"{seconds} сек"
    bot.update_message(
        chat_id,
        message_id,
        f"Осталось {time_text}!\n {progress_barr}"
    )


def timer(chat_id, message, bot):
    answer = "Время вышло"
    bot.send_message(chat_id, answer)


def render_progressbar(
    total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def handle_message(chat_id, question, bot):
    wait(chat_id, question, bot)


def main():
    bot = connect_bot(TG_TOKEN)

    def message_handler(chat_id, question):
        handle_message(chat_id, question, bot)

    bot.reply_on_message(message_handler)
    bot.run_bot()


if __name__ == '__main__':
    main()
