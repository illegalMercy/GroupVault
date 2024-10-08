MENU = """
<b>Добро пожаловать! </b>

Здесь вы можете приобрести группы с отлёжкой. Просто выберите необходимую опцию ниже:

<b>🛒 Купить</b> - Нажмите, чтобы просмотреть доступные группы и совершить покупку.

<b>📞 Контакты</b> - Свяжитесь с нами для получения дополнительной информации или помощи.

В наличии: <b>{total_groups} шт.</b>
"""


GROUP_MENU = """
<b>🛒 Купить</b>

Выберите срок отлёжки группы:

{groups}
"""


INVOICE = """
<b>🛒 Купить</b>

Цена: <b>{price}</b> ₽
Отлёжка: <b>{age}</b> мес.
"""


SUCCESS_PAYMENT = """
<b>🎉 Оплата прошла успешно!</b>

Вступите в полученную группу и нажмите \n<b>«Получить права»</b>

Название: {group_name}
Дата создания: {group_created_at}
Ссылка: {group_link}
"""


NOT_MEMBER = """
Вы не являетесь участником группы!
Пожалуйста, вступите в группу.
"""


TRANSFER_ERROR = """
<b>⚠️ Ошибка!</b>

Что-то пошло не так 🤷‍♂️
Пожалуйста, повторите попытку или обратитесь в тех.поддержку.
"""


TRANSFER_SUCCESS = """
<b>🎉 Поздравляем!</b>

Права на управление группой переданы успешно.
"""


CONTACTS = """
<b>📞 Контакты</b>

Если у вас возникнут вопросы или проблемы, вы всегда можете обратиться к техподдержке.

<b>👤 Telegram:</b> @illegalMercy
"""