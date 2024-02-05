# Курсовая работа 6

<div align="center">
<a href="https://wakatime.com/@IldarGaleev/projects/coursework_6"><img src="https://wakatime.com/badge/user/45799db8-b1f8-4627-9264-2c8d4c352567/project/018d6055-7d00-4097-a133-658e7c54a640.svg" alt="wakatime"></a>
<img src="https://img.shields.io/github/last-commit/IldarGaleevSkyProHomeworks/coursework_6.svg"/>
</div>

1. Установите зависимости

``` PowerShell
poetry install
```

2. Создайте базу данных и пропишите настройки подключения в файле .env ([шаблон файла](.env.template))
3. Задайте необходимые [переменные окружения](#переменные-окружения)
4. Примените миграции


``` PowerShell 
 python .\manage.py migrate
```

5. Создайте учетную запись администратора

``` PowerShell
python .\manage.py createsuperuser
```
6. Запустите сервер
``` PowerShell
python .\manage.py runserver
```
7. Добавьте задачи в `cron` для отправки e-mail сообщений
> [!TIP]
> 
> Для ОС Windows воспользуйтесь [WSL](https://learn.microsoft.com/ru-ru/windows/wsl/setup/environment)
> 
``` PowerShell
python .\manage.py crontab add
```

## Переменные окружения

> [!TIP]
> 
> Поддерживается файл `.env` для назначения переменных. [Шаблон файла](.env.template)
> 

### Общие

| Переменная      | Файл настроек                            | Назначение               |
|-----------------|------------------------------------------|--------------------------|
| `SECRET_KEY`    | [config/settings.py](config/settings.py) | Ключ безопасности Django |
| `SITE_ID`       | [config/settings.py](config/settings.py) | Текущий домен            |



### Postgres

| Переменная    | Файл настроек                            | Назначение                          |
|---------------|------------------------------------------|-------------------------------------|
| `PG_NAME`     | [config/settings.py](config/settings.py) | Имя базы данных                     |
| `PG_USER`     | [config/settings.py](config/settings.py) | Имя пользователя для подключения    |
| `PG_PASSWORD` | [config/settings.py](config/settings.py) | Пароль пользователя для подключения |
| `PG_HOST`     | [config/settings.py](config/settings.py) | Имя хоста с сервером                |
| `PG_PORT`     | [config/settings.py](config/settings.py) | Порт сервера                        |


### Страница публикаций

| Переменная               | Файл настроек                            | Назначение                                             |
|--------------------------|------------------------------------------|--------------------------------------------------------|
| `ARTICLES_PER_PAGE`      | [blog_app/apps.py](blog_app/apps.py)     | Количество публикаций на странице                      |
| `POPULAR_ARTICLES_COUNT` | [config/settings.py](config/settings.py) | Отображаемое количество публикаций на главной странице |


### Кеширование
| Переменная                | Файл настроек                            | Назначение                               |
|---------------------------|------------------------------------------|------------------------------------------|
| `REDIS_CONNECTION_STRING` | [config/settings.py](config/settings.py) | Строка подключения к Redis               |
| `CACHE_ENABLED`           | [config/settings.py](config/settings.py) | Включить кеширование                     |
| `REDIS_CACHE_DATABASE`    | [config/settings.py](config/settings.py) | БД Redis, используемая для кеширования   |
| `PAGE_CACHE_TIME`         | [config/settings.py](config/settings.py) | Время (сек.) обновления кеша контроллера |

### Логирование

Для настройки логирования укажите путь к json файлу конфигурации в переменной окружения `LOGGING_CONFIG_FILE`.

Пример файла конфигурации для вывода отладочных сообщений в консоль от менеджера фоновых задач:

```json
{
  "version": 1,
  "disable_existing_loggers": false,
  "handlers": {
    "console": {
      "class": "logging.StreamHandler"
    }
  },
  "root": {
    "handlers": [
      "console"
    ],
    "level": "WARNING"
  },
  "loggers": {
    "tasks.send_mail": {
      "level": "DEBUG"
    }
  }
}
```

### Фоновые задачи

| Переменная                         | Файл настроек                            | Назначение                             |
|------------------------------------|------------------------------------------|----------------------------------------|
| `BG_TASK__REDIS_HOSTNAME`          | [config/settings.py](config/settings.py) | Сервер `Redis`                         |
| `BG_TASK__REDIS_PORT`              | [config/settings.py](config/settings.py) | Порт сервера `Redis`                   |
| `BG_TASK__REDIS_DB`                | [config/settings.py](config/settings.py) | База данных `Redis`                    |
| `ACCOUNT_SERVICE_MAIL_RETRY_COUNT` | [config/settings.py](config/settings.py) | Число повторных попыток отправки писем |
| `ACCOUNT_SERVICE_MAIL_TASK_TTL`    | [config/settings.py](config/settings.py) | Время жизни задачи                     |

## Учетная запись менеджера 

Для создания учетных записей менеджеров создайте группу со следующими правами или назначьте их напрямую пользователю:

| Разрешение                     | Описание                                 |
|--------------------------------|------------------------------------------|
| `app_accounts.view_user`       | Может просматривать список пользователей |
| `app_accounts.can_block_users` | Может блокировать пользователей          |
| `app_mailing.view_mailing`     | Может просматривать рассылки             |
| `app_mailing.can_stop_mailing` | Может останавливать рассылки             |
| `app_mailing.view_mailmessage` | Может просматривать письма рассылок      |