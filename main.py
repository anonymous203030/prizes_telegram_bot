import random

from sqlalchemy import update, and_
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import settings
from base.models import User, Item, conn
from datetime import date

bot = TelegramClient(StringSession(), settings.API_ID, settings.API_HASH).start(bot_token = settings.BOT_TOKEN)


async def salary_dbase_create(event) -> int:
	sender = await event.get_sender()
	users_info = User.select().where(User.c.username == sender.username)
	salary__ = conn.execute(users_info).fetchone()
	if salary__ is None:
		insert_values = User.insert().values(username = sender.username, salary = 0)
		conn.execute(insert_values)
		users_info = User.select().where(User.c.username == sender.username)
	salary__ = conn.execute(users_info).fetchone()
	salary_ = int(salary__.salary)
	return salary_


async def daily_limit(event) -> list:
	sender = await event.get_sender()
	items_daily = Item.select().where(and_(Item.c.owner == sender.username, Item.c.date == date.today()))
	daily = conn.execute(items_daily).fetchall()
	return daily


async def get_box(event) -> list:
	num = int(str(event.data).split('_')[1])
	print('NUM', num)
	val = str(event.data).split('_')[2]
	print('VAL', val)
	box = int(val[:len(val) - 1])
	return [box, num]


@bot.on(events.CallbackQuery(data = b'back'))
@bot.on(events.NewMessage())
async def bot_start(event):
	try:
		if event.raw_text in settings.START:
			await event.reply(message = settings.START_MESSAGE,
			                  buttons = [settings.INFO_BUTTON, [settings.BOXES_BUTTON,
			                                                    settings.HOW_TO_OPEN_BUTTON,
			                                                    settings.PAYMENT_BUTTON]])
	except AttributeError:
		await event.reply(message = settings.START_MESSAGE,
		                  buttons = [settings.INFO_BUTTON,
		                             settings.BOXES_BUTTON,
		                             settings.INVENTORY_BUTTON,
		                             settings.HOW_TO_OPEN_BUTTON,
		                             settings.PAYMENT_BUTTON])


@bot.on(events.CallbackQuery(data = b'info'))
async def send_info(event):
	await event.reply(settings.INFO,
	                  buttons = [settings.BOXES_BUTTON,
	                             settings.PAYMENT_BUTTON,
	                             settings.INVENTORY_BUTTON,
	                             settings.HOW_TO_OPEN_BUTTON])


@bot.on(events.CallbackQuery(data = b'boxes'))
async def get_boxes(event):
	salary_ = await salary_dbase_create(event)
	if salary_ == 250:
		event.reply('Вы можете открыть 1 коробку 250',
		            buttons = [settings.BACK_BUTTON,
		                       settings.HOW_TO_OPEN_BUTTON,
		                       settings.PAYMENT_BUTTON,
		                       settings.INVENTORY_BUTTON,
		                       settings.OPEN_BOX_250_BUTTON])
	if salary_ == 500:
		event.reply('Вы можете открыть:\n'
		            '2 коробки по 250р\n'
		            '1 коробку по 500р',
		            buttons = [settings.BACK_BUTTON,
		                       settings.OPEN_2_250_BUTTON,
		                       settings.OPEN_BOX_500_BUTTON,
		                       settings.HOW_TO_OPEN_BUTTON,
		                       settings.PAYMENT_BUTTON,
		                       settings.INVENTORY_BUTTON])
	if salary_ == 1000:
		event.reply('Вы можете открыть:\n'
		            '3 коробки по 250р\n'
		            '2 коробки по 500р\n'
		            '1 коробку по 1000р',
		            buttons = [settings.BACK_BUTTON,
		                       settings.OPEN_3_250_BUTTON,
		                       settings.OPEN_2_500_BUTTON,
		                       settings.OPEN_BOX_1000_BUTTON,
		                       settings.HOW_TO_OPEN_BUTTON,
		                       settings.PAYMENT_BUTTON,
		                       settings.INVENTORY_BUTTON])
	if salary_ == 2000:
		event.reply('Вы можете открыть:\n'
		            '2 коробки по 250р\n'
		            '1 коробку по 500р', buttons = [settings.BACK_BUTTON,
		                                            settings.OPEN_3_250_BUTTON,
		                                            settings.OPEN_3_500_BUTTON,
		                                            settings.OPEN_2_1000_BUTTON,
		                                            settings.OPEN_BOX_2000_BUTTON,
		                                            settings.HOW_TO_OPEN_BUTTON,
		                                            settings.PAYMENT_BUTTON,
		                                            settings.INVENTORY_BUTTON])

	await event.reply(settings.BOX_INSIDE,
	                  buttons = [settings.BACK_BUTTON,
	                             settings.HOW_TO_OPEN_BUTTON,
	                             settings.PAYMENT_BUTTON,
	                             settings.INVENTORY_BUTTON,
	                             settings.OPEN_BOX_250_BUTTON,
	                             settings.OPEN_BOX_500_BUTTON,
	                             settings.OPEN_BOX_1000_BUTTON])


@bot.on(events.CallbackQuery(data = b'how_to_open'))
async def how_to_open(event):
	await event.reply(settings.HOW_TO_OPEN,
	                  buttons = [settings.BACK_BUTTON])


@bot.on(events.CallbackQuery(data = b'payment'))
async def payment(event):
	await event.reply(settings.PAYMENT,
	                  buttons = [settings.BACK_BUTTON,
	                             settings.HOW_TO_OPEN_BUTTON,
	                             settings.PAYMENT_BUTTON_1,
	                             settings.PAYMENT_BUTTON_2,
	                             settings.PAYMENT_BUTTON_3,
	                             settings.PAYMENT_BUTTON_4,
	                             settings.BOXES_BUTTON])


@bot.on(events.CallbackQuery(data = b'open_250'))
@bot.on(events.CallbackQuery(data = b'open_500'))
@bot.on(events.CallbackQuery(data = b'open_1000'))
@bot.on(events.CallbackQuery(data = b'open_2000'))
async def OpenBox(event):
	sender = await event.get_sender()
	box_num = await get_box(event)
	box, num = box_num[0], box_num[1]
	salary_ = await salary_dbase_create(event)
	print('SALARY', salary_)
	daily = await daily_limit(event)
	if salary_ < box:
		await event.reply('Сумма баланса недостаточна для покупки кейса. Пополните ваш баланс\n'
		                  f'Ваш баланс: {salary_}',
		                  buttons = [settings.BACK_BUTTON, settings.PAYMENT_BUTTON, settings.BOXES_BUTTON])
	elif len(daily) >= 3:
		await event.reply('Извините вы превысили лимит открытия коробок!Лимит в день: 3.',
		                  buttons = [settings.BACK_BUTTON, settings.PAYMENT_BUTTON, settings.BOXES_BUTTON])
	else:
		salary_after = update(User).where(User.c.username == sender.username).values(salary = salary_ - box)
		conn.execute(salary_after)
		if box == 250:
			chosen_item = random.choices(settings.CHOICES[int(box)], weights = (40, 40, 20), k = num)[0]
		elif box == 500:
			chosen_item = random.choices(settings.CHOICES[int(box)], weights = (35, 15, 35, 15), k = num)[0]
		else:
			chosen_item = random.choices(settings.CHOICES[int(box)], weights = (20, 40, 20), k = num)[0]
		if type(chosen_item) is not str:
			for item_ in chosen_item:
				insert_values = Item.insert().values(owner = sender.username, item = item_)
				conn.execute(insert_values)

			await event.reply(f"Поздравляю!Вы выиграли: {chosen_item.split(', ')}",
			                  buttons = [settings.BACK_BUTTON,
			                             settings.OPEN_BOX_250_BUTTON,
			                             settings.OPEN_BOX_500_BUTTON,
			                             settings.OPEN_BOX_1000_BUTTON,
			                             settings.INVENTORY_BUTTON])
		else:
			insert_values = Item.insert().values(owner = sender.username, item = chosen_item, date = date.today())
			conn.execute(insert_values)
			await event.reply(f'Поздравляю!Вы выиграли: {chosen_item}',
			                  buttons = [settings.BACK_BUTTON,
			                             settings.OPEN_BOX_250_BUTTON,
			                             settings.OPEN_BOX_500_BUTTON,
			                             settings.OPEN_BOX_1000_BUTTON,
			                             settings.INVENTORY_BUTTON])


@bot.on(events.CallbackQuery(data = b'inventory'))
async def get_inventory(event):
	sender = await event.get_sender()
	inventory_values = Item.select().where(Item.c.owner == sender.username)
	values__ = conn.execute(inventory_values).fetchall()
	# values_ = values__.item
	if not values__:
		await event.reply('Ваш Инвентарь Пустой.',
		                  buttons = [settings.BACK_BUTTON,
		                             settings.PAYMENT_BUTTON,
		                             settings.BOXES_BUTTON])
	else:
		all_items = []
		for item in values__:
			all_items.append(item[1])
		await event.reply(f'Ваш инвентарь: {", ".join(all_items)}',
		                  buttons = [settings.BACK_BUTTON,
		                             settings.PAYMENT_BUTTON,
		                             settings.BOXES_BUTTON])


if __name__ == '__main__':
	bot.run_until_disconnected()
