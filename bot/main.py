import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Application
from telegram.constants import ParseMode
from finnhub_service import FinnService
from settings import TELEGRAM_API_KEY
from template_service import TemplateService

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_report(tick, force_next=False):
    if force_next:
        return FinnService.get_next_earnings(tick)
    report = FinnService.get_recent_earnings(tick)
    if not report:
        return get_report(tick, force_next=True)
    return report


async def help_command(update: Update, context: CallbackContext):
    await update.effective_chat.send_message(parse_mode=ParseMode.HTML, text=TemplateService.get_template('help'))


async def ticker(update: Update, context: CallbackContext):
    for arg in context.args:
        try:
            company_obj, quote_obj = FinnService.get_ticker_quote(arg.upper())
            if not company_obj.is_real():
                await update.effective_chat.send_message(text=f"Unable to find: {arg}")
                continue
            responding_text = TemplateService.format_template(company_obj, quote_obj)
            await update.effective_chat.send_message(parse_mode=ParseMode.HTML, text=responding_text)
        except Exception as e:
            logger.exception(e)
            await update.effective_chat.send_message(text=f'Error retrieving information for {arg}')


async def ticker_details(update: Update, context: CallbackContext):
    for arg in context.args:
        try:
            company_obj, quote_obj, reco_obj = FinnService.get_all_info(arg.upper())
            if not company_obj.is_real():
                await update.effective_chat.send_message(text=f"Unable to find: {arg}")
                continue
            responding_text = TemplateService.format_template(company_obj, quote_obj, reco_obj)
            await update.effective_chat.send_message(parse_mode=ParseMode.HTML, text=responding_text)
        except Exception as e:
            logger.exception(e)
            await update.effective_chat.send_message(f'Error retrieving information for {arg}')


async def er(update: Update, context: CallbackContext):
    for tick in context.args:
        try:
            company_obj = FinnService.get_company_profile(tick)
            earn_report = get_report(tick)
            formatted_text = TemplateService.format_template(company_obj, earn_report)
            await update.effective_chat.send_message(parse_mode=ParseMode.HTML, text=formatted_text)
        except Exception as e:
            logger.exception(e)
            await update.effective_chat.send_message(f'Error retrieving earnings report for {tick}')


async def ern(update: Update, context: CallbackContext):
    for tick in context.args:
        try:
            company_obj = FinnService.get_company_profile(tick)
            earn_report = get_report(tick, force_next=True)
            formatted_text = TemplateService.format_template(company_obj, earn_report)
            await update.effective_chat.send_message(parse_mode=ParseMode.HTML, text=formatted_text)
        except Exception as e:
            logger.exception(e)
            await update.effective_chat.send_message(f'Error retrieving next earnings report for {tick}')


if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_API_KEY).build()
    application.add_handler(CommandHandler('ticker', ticker))
    application.add_handler(CommandHandler('ticker_details', ticker_details))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('er', er))
    application.add_handler(CommandHandler('ern', ern))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
