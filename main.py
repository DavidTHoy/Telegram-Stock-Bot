from telegram.ext import Updater
import logging
from telegram import ParseMode
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from finnhub_service import FinnService
from template_service import TemplateService
from settings import TELEGRAM_API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Use me up.")


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=TemplateService.build_template('help'),
                             parse_mode=ParseMode.HTML)


def ticker(update: Update, context: CallbackContext):
    for arg in context.args:
        try:
            company_obj, quote_obj = FinnService.get_all_info(arg.upper())
            if not company_obj.is_real():
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Unable to find: {arg}",
                                         parse_mode=ParseMode.HTML)
                continue
            template = TemplateService.build_template('quote')
            respondingText = TemplateService.format_quote_template(template, company_obj, quote_obj)
            context.bot.send_message(chat_id=update.effective_chat.id, text=respondingText, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(e)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Error retrieving information for {arg}')


def er(update: Update, context: CallbackContext):
    for tick in context.args:
        try:
            company_obj = FinnService.get_company_profile(tick)
            earn_report = FinnService.get_recent_earnings(tick)
            if not earn_report:
                earn_report = FinnService.get_next_earnings(tick)
            template = TemplateService.build_template('earnings')
            formatted_text = TemplateService.format_earnings_template(template, company_obj, earn_report)
            context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(e)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Error retrieving earnings report for {tick}')


def ern(update: Update, context: CallbackContext):
    for tick in context.args:
        try:
            company_obj = FinnService.get_company_profile(tick)
            earn_report = FinnService.get_next_earnings(tick)
            template = TemplateService.build_template('earnings')
            formatted_text = TemplateService.format_earnings_template(template, company_obj, earn_report)
            context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.exception(e)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Error retrieving next earnings report for {tick}')


if __name__ == '__main__':
    updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('ticker', ticker, pass_args=True))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('er', er, pass_args=True))
    dispatcher.add_handler(CommandHandler('ern', ern, pass_args=True))
    updater.start_polling()