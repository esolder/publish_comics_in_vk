# Публикуем комиксы во Вконтакте
Проект для автоматизации публикации комиксов [xkcd](https://xkcd.com/) в сообществе [Вконтакте](https://vk.com/).

### Как установить
Python3 должен быть уже установлен. Затем используйте pip (или pip3, если есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

Чтобы использовать скрипты, нужно создать файл `.env`, содержащий следующие переменные:
- `VK_GROUP_ID`: id сообщества Вконтакте
- `VK_ACCESS_TOKEN`: токен для публикации. Подробнее о получении можно узнать [здесь](https://vk.com/dev/implicit_flow_user)

### Как запустить
Для запуска скрипта нужно выполнить следующую команду:
```
python publish_vk.py
```
В сообществе опубликуется случайный комикс с комментарием автора.

### download_comics.py
Содержит функции для загрузки комикса с сайта [xkcd](https://xkcd.com/).

### publish_vk.py
Скрипт для публикации комикса в сообществе [Вконтакте](https://vk.com/)

### support_funcs.py
Содержит функцию `get_response`, использующуюся в `download_comics.py` и `publish_vk.py`.

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).