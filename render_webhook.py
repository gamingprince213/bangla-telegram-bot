#!/usr/bin/env python3
"""
Render.com এর জন্য বাংলা টেলিগ্রাম বট
"""

import os
import logging
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# কনফিগারেশন
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 10000))  # Render.com ডিফল্ট পোর্ট

# ফ্লাস্ক অ্যাপ
app = Flask(__name__)

# বট অ্যাপ্লিকেশন
application = None

# বেসিক কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start কমান্ড হ্যান্ডলার"""
    user = update.effective_user
    welcome_message = f"""
🎉 স্বাগতম {user.first_name}! 

এটি Render.com এ ডিপ্লয় করা একটি বাংলা টেলিগ্রাম বট!

**বৈশিষ্ট্য:**
• ⚡ Render.com এ ডিপ্লয়ড
• 🔄 স্বয়ংক্রিয় রিস্টার্ট
• 📊 ২৪/৭ অনলাইন
• 🔒 ফ্রি SSL সার্টিফিকেট

**কমান্ড:**
/start - শুরু করুন
/help - সাহায্য পান
/status - স্ট্যাটাস চেক করুন
/info - বট ইনফো

**বাংলা কীওয়ার্ড:**
হ্যালো, কেমন আছেন, ধন্যবাদ, বাই
    """
    
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help কমান্ড হ্যান্ডলার"""
    help_text = """
🆘 **সাহায্য মেনু**

**বেসিক কমান্ড:**
• /start - বট শুরু করুন
• /help - এই মেনু দেখান
• /status - বট স্ট্যাটাস চেক করুন
• /info - বট সম্পর্কে তথ্য

**বাংলা কথোপকথন:**
• "হ্যালো" - স্বাগতম বার্তা
• "কেমন আছেন" - আপনার খবর জানতে চাওয়া
• "ধন্যবাদ" - ধন্যবাদ বার্তা
• "বাই" - বিদায় বার্তা

**মাল্টিমিডিয়া:**
• ফটো পাঠালে ধন্যবাদ বার্তা
• ডকুমেন্ট পাঠালে কনফার্মেশন
• ভয়েস মেসেজের উত্তর

**যোগাযোগ:**
প্রশ্ন থাকলে @your_username এ মেসেজ করুন
    """
    
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/status কমান্ড হ্যান্ডলার"""
    status_text = """
📊 **বট স্ট্যাটাস**

✅ বট সচল আছে
🌐 Render.com এ ডিপ্লয়ড
🔒 SSL সার্টিফিকেট সক্রিয়
⚡ ২৪/৭ অনলাইন

**সার্ভার ইনফো:**
• প্ল্যাটফর্ম: Render.com
• রিজিওন: Singapore (বাংলাদেশের কাছাকাছি)
• পোর্ট: 10000
    """
    
    await update.message.reply_text(status_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/info কমান্ড হ্যান্ডলার"""
    info_text = """
ℹ️ **বট ইনফো**

**নাম:** বাংলা টেলিগ্রাম বট
**ভার্সন:** 2.0.0
**প্ল্যাটফর্ম:** Render.com
**ভাষা:** বাংলা (পূর্ণ সমর্থন)

**বৈশিষ্ট্য:**
• সম্পূর্ণ বাংলা ইন্টারফেস
• রিয়েল-টাইম মেসেজ হ্যান্ডলিং
• মাল্টিমিডিয়া সাপোর্ট
• ওয়েবহুক-ভিত্তিক আর্কিটেকচার

**ডেভেলপার:** Suna.so AI Assistant
    """
    
    await update.message.reply_text(info_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """টেক্সট মেসেজ হ্যান্ডলার"""
    text = update.message.text.lower()
    
    # বাংলা কীওয়ার্ড রেসপন্স
    responses = {
        'হ্যালো': f'হ্যালো {update.effective_user.first_name}! 😊',
        'হাই': f'হাই {update.effective_user.first_name}! 👋',
        'কেমন আছেন': 'আমি ভালো আছি, আপনি কেমন আছেন? 😊',
        'ধন্যবাদ': 'আপনাকেও ধন্যবাদ! 🙏',
        'বাই': 'বাই বাই! আবার দেখা হবে! 👋',
        'আলহামদুলিল্লাহ': 'আলহামদুলিল্লাহ! সবকিছু ভালো আছে 🌟',
        'কি খবর': 'সব ঠিক আছে! আপনার কি খবর? 📰'
    }
    
    response = responses.get(text, None)
    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(
            f"আপনি বলেছেন: {text}\n\n"
            f"আমি এখনও শিখছি! /help কমান্ড দিয়ে সাহায্য পান।"
        )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ফটো মেসেজ হ্যান্ডলার"""
    await update.message.reply_text(
        "📸 দারুন ছবি! আপনাকে ধন্যবাদ ছবি পাঠানোর জন্য।"
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ডকুমেন্ট মেসেজ হ্যান্ডলার"""
    await update.message.reply_text(
        "📄 ডকুমেন্ট রিসিভ হয়েছে! ধন্যবাদ।"
    )

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ভয়েস মেসেজ হ্যান্ডলার"""
    await update.message.reply_text(
        "🎤 ভয়েস মেসেজ শুনেছি! ধন্যবাদ।"
    )

# ফ্লাস্ক রুট
@app.route('/')
def index():
    """হোমপেজ"""
    return jsonify({
        'status': 'running',
        'bot': 'Bangla Telegram Bot',
        'platform': 'Render.com',
        'language': 'Bengali'
    })

@app.route('/health')
def health():
    """হেলথ চেক এন্ডপয়েন্ট"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """টেলিগ্রাম ওয়েবহুক এন্ডপয়েন্ট"""
    try:
        # JSON ডেটা পার্স করা
        json_data = request.get_json()
        
        # Update অবজেক্ট তৈরি করা
        update = Update.de_json(json_data, Bot(BOT_TOKEN))
        
        # অ্যাপ্লিকেশন প্রসেস করা
        asyncio.run(application.process_update(update))
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({'error': str(e)}), 500

# হ্যান্ডলার সেটআপ
def setup_handlers(app):
    """টেলিগ্রাম হ্যান্ডলার সেটআপ"""
    # কমান্ড হ্যান্ডলার
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("info", info_command))
    
    # মেসেজ হ্যান্ডলার
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

# অ্যাপ্লিকেশন ইনিশিয়ালাইজেশন
def init_app():
    """অ্যাপ্লিকেশন ইনিশিয়ালাইজ করা"""
    global application
    
    # টেলিগ্রাম অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(BOT_TOKEN).build()
    
    # হ্যান্ডলার সেটআপ
    setup_handlers(application)
    
    return application

if __name__ == '__main__':
    # চেক করুন সব এনভায়রনমেন্ট ভেরিয়েবল আছে কিনা
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN এনভায়রনমেন্ট ভেরিয়েবল সেট করা হয়নি!")
        sys.exit(1)
    
    if not WEBHOOK_URL:
        logger.error("WEBHOOK_URL এনভায়রনমেন্ট ভেরিয়েবল সেট করা হয়নি!")
        sys.exit(1)
    
    # অ্যাপ্লিকেশন ইনিশিয়ালাইজ করা
    init_app()
    
    # ফ্লাস্ক সার্ভার চালু করা
    logger.info(f"Starting server on port {PORT}")
    app.run(host='0.0.0.0', port=PORT)