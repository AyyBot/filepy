import pandas as pd
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random

# DataFrame toàn cục để lưu dữ liệu khách hàng
df = pd.DataFrame()

def load_data():
    global df
    df = pd.read_excel('FIE CẦN.xlsx', dtype=str)
    print("Columns in the dataframe:", df.columns.tolist())

async def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.first_name 
    await update.message.reply_text(
        f'<b>Xin chào, {user_name}!</b>\n'
        '<i>Để kiểm tra thông tin khoản vay, vui lòng nhập APP_ID, Tên khách hàng, CMND/CCCD hoặc số chính khi vay.</i>\n'
        '<b>LƯU Ý: NẾU QUÝ KHÁCH THANH TOÁN BẮT BUỘC PHẢI GHI NỘI DUNG</b>',
        parse_mode='HTML'
    )

async def check_info(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text.strip()
    user_input = str(user_input)
    
    result = df[(df['CMND/CCCD'] == user_input) | (df['Tên khách hàng'] == user_input) | (df['APP_ID'] == user_input) | (df['Số chính'] == user_input)]
    
    if not result.empty:
        for index, row in result.iterrows():
            response = (
                f"<b>APP_ID:</b> <i>{row['APP_ID']}</i>\n"
                f"<b>CMND/CCCD:</b> <i>{row['CMND/CCCD']}</i>\n"
                f"<b>Tên khách hàng:</b> <i>{row['Tên khách hàng']}</i>\n"
                f"<b>Số chính:</b> <i>{row['Số chính']}</i>\n"
                f"<b>Ngày sinh:</b> <i>{row['Ngày sinh']}</i>\n"
                f"<b>Email:</b> <i>{row['Email']}</i>\n"
                f"<b>Đ/c hộ khẩu:</b> <i>{row['Đ/c hộ khẩu']}</i>\n"
                f"<b>Tên Cty:</b> <i>{row['Tên Cty']}</i>\n"
                f"<b>Chức vụ:</b> <i>{row['Chức vụ']}</i>\n"
                f"<b>Ngày vay:</b> <i>{row['Ngày vay']}</i>\n" 
                f"<b>Tiền vay:</b> <i>{row['Tiền vay']}</i>\n"
                f"<b>Nợ gốc:</b> <i>{row['Nợ gốc']}</i>\n"
                f"<b>Số tiền cần thanh toán:</b> <i>{row['Số tiền cần thanh toán']}</i>\n"
                f"<b>STK giải ngân:</b> <i>{row['STK giải ngân']}</i>\n"
                f"<b>Ngân hàng giải ngân:</b> <i>{row['Ngân hàng giải ngân']}</i>\n"
                f"<b>STK THANH TOÁN:</b> <i>{row['STK THANH TOÁN']}</i>\n"
                f"<b>Ngân hàng:</b> <i>{row['Ngân hàng']}</i>\n"
                f"<b>Tên người thụ hưởng:</b> <i>{row['tên người thụ hưởng']}</i>\n"
                f"<b>Nội dung:</b> <i>{row['nội dung']}</i>\n"
                f"<b>Mã nhân viên:</b> <i>{row['Mã nhân viên']}</i>\n"
                f"<b>Note:</b> <i>{row['note']}</i>\n"
                f"<b>GP:</b> <i>{row['GP']}</i>\n"
            )
            await update.message.reply_text(response, parse_mode='HTML')
    else:
        await update.message.reply_text('Không tìm thấy thông tin khách hàng với dữ liệu đã nhập.', parse_mode='HTML')

async def update_data(update: Update, context: CallbackContext) -> None:
    load_data()
    await update.message.reply_text('Dữ liệu đã được cập nhật.')

async def weather(update: Update, context: CallbackContext) -> None:
    city = ' '.join(context.args)
    api_key = 'YOUR_WEATHER_API_KEY'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url).json()
    if response.get('main'):
        weather_description = response['weather'][0]['description']
        temperature = response['main']['temp']
        await update.message.reply_text(f'Thời tiết tại {city}: {weather_description}, Nhiệt độ: {temperature}°C')
    else:
        await update.message.reply_text('Không tìm thấy thành phố!')

async def calculate(update: Update, context: CallbackContext) -> None:
    try:
        expression = ' '.join(context.args)
        result = eval(expression)
        await update.message.reply_text(f'Kết quả: {result}')
    except Exception as e:
        await update.message.reply_text(f'Lỗi: {e}')

async def daily_advice(update: Update, context: CallbackContext) -> None:
    advices = [
        "Hãy bắt đầu ngày mới với một nụ cười!",
        "Đừng bỏ cuộc, thành công đang đến gần.",
        "Hãy luôn tin vào bản thân mình.",
        "Mỗi ngày là một cơ hội mới.",
        "Hãy giúp đỡ người khác, bạn sẽ nhận lại nhiều hơn."
    ]
    advice = random.choice(advices)
    await update.message.reply_text(advice)

async def random_image(update: Update, context: CallbackContext) -> None:
    url = 'https://picsum.photos/200/300'
    await update.message.reply_photo(photo=url)

def main() -> None:
    load_data()

    token = '6880646970:AAEwf39emS7QYvSwRLAVuyZ3UyAW1NVVawc'
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("update", update_data))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("calculate", calculate))
    application.add_handler(CommandHandler("advice", daily_advice))
    application.add_handler(CommandHandler("image", random_image))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_info))

    application.run_polling()

if __name__ == '__main__':
    main()
