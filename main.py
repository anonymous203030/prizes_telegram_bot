import random

from sqlalchemy import update
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import settings
from base.models import User, Item, engine, conn

bot = TelegramClient(StringSession(), settings.API_ID, settings.API_HASH).start(bot_token = settings.BOT_TOKEN)


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
	await event.reply(settings.BOX_INSIDE,
	                  buttons = [settings.BACK_BUTTON,
	                             settings.HOW_TO_OPEN_BUTTON,
	                             settings.PAYMENT_BUTTON,
	                             settings.INVENTORY_BUTTON,
	                             settings.OPEN_BOX_1_BUTTON,
	                             settings.OPEN_BOX_2_BUTTON,
	                             settings.OPEN_BOX_3_BUTTON])


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
	print(sender.username)
	print('EVENT DATA', event.data)
	num = str(event.data).split('_')[1]
	box = int(num[:len(num) - 1])
	print('BOX', box)
	users_salary = User.select().where(User.c.username == sender.username)
	salary__ = conn.execute(users_salary).fetchone()
	if salary__ is None:
		insert_values = User.insert().values(username = sender.username)
		conn.execute(insert_values)
		users_salary = User.select().where(User.c.username == sender.username)
	salary__ = conn.execute(users_salary).fetchone()
	salary_ = int(salary__.salary)
	print('END_SALARY', salary_)
	if salary_ < box:
		await event.reply('Сумма баланса недостаточна для покупки кейса. Пополните ваш баланс',
		                  buttons = [settings.BACK_BUTTON, settings.PAYMENT_BUTTON, settings.BOXES_BUTTON])
	else:
		salary_after = update(User).where(User.c.username == sender.username).values(salary = salary_ - box)
		conn.execute(salary_after)
		if box == 250:
			chosen_item = random.choices(settings.CHOICES[int(box)], weights = (40, 40, 20))[0]
		elif box == 500:
			chosen_item = random.choices(settings.CHOICES[int(box)], weights = (35, 15, 35, 15))[0]
		else:
			chosen_item = random.choices(settings.CHOICES[int(box)], weights = (20, 40, 20))[0]
		insert_values = Item.insert().values(owner = sender.username, item = chosen_item)
		conn.execute(insert_values)
		await event.reply(f'Поздравляю!Вы выиграли{chosen_item}',
		                  buttons = [settings.BACK_BUTTON, settings.INVENTORY_BUTTON])


@bot.on(events.CallbackQuery(data = b'inventory'))
async def get_inventory(event):
	sender = await event.get_sender()
	inventory_values = Item.select().where(Item.c.owner == sender.username)
	values__ = conn.execute(inventory_values).fetchall()
	# values_ = values__.item
	all_items = []
	for item in values__:
		all_items.append(item[1])
	await event.reply(f'Ваш инвентарь: {", ".join(all_items)}',
	                  buttons = [settings.BACK_BUTTON, settings.PAYMENT_BUTTON, settings.BOXES_BUTTON])


if __name__ == '__main__':
	bot.run_until_disconnected()
