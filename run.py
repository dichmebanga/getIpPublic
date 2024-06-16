import asyncio
import requests
from telegram import Bot
import logging

# Thay đổi thông tin bot và chat_id của bạn
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'
TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID_ACCOUNT'
CHECK_INTERVAL = 600  # Thời gian chờ giữa các lần kiểm tra (tính bằng giây) = 10'


async def get_public_ip():
    """
    Lấy địa chỉ IP công khai hiện tại.

    Returns:
        Chuỗi: Địa chỉ IP công khai hoặc `None` nếu gặp lỗi.
    """
    try:
        response = requests.get("https://api.ipify.org?format=json")
        ip = response.json().get("ip")
        return ip
    except requests.RequestException as e:
        logging.error(f"Lỗi khi lấy IP: {e}")
        return None


async def send_telegram_message(bot, chat_id, message):
    """
    Gửi tin nhắn Telegram đến chat_id được chỉ định.

    Args:
        bot: Đối tượng bot Telegram.
        chat_id: ID của chat Telegram.
        message: Nội dung tin nhắn.
    """
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error(f"Lỗi khi gửi tin nhắn: {e}")


async def main():
    """
    Chức năng chính của script.
    """
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    last_ip = None

    while True:
        logging.info("Kiểm tra thay đổi IP...")
        print("vao day")  # Giữ lại dòng in này nếu cần thiết

        current_ip = await get_public_ip()
        print('current_ip', current_ip)
        if current_ip and current_ip != last_ip:
            message = f"Địa chỉ IP công khai đã thay đổi: {current_ip}"
            await send_telegram_message(bot, TELEGRAM_CHAT_ID, message)
            last_ip = current_ip

        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
