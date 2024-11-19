<div align="center">
  <img src="token_sender_preview.png"  />
</div>

# TokenSender
Софт для автоматизации перевода токенов

## Основные возможности
- Подключение прокси
- Рандомизация временных промежутков между переводами
- Возможность закончить незаконченные (по каким-то причинам) переводы
- Запуск переводов в разных потоках
- проверка балансов кошельков в DAI, USDC, USDCe, USDT, WETH + ЛЮБОЙ другой ТОКЕН, адрес которого указан в `address_token` на вкладке "Send" в soft_settings.xlsx.

# 🛠 Параметры софта для настройки
## Вкладка "Main"
- `private_key`: приватный ключ аккаунта
- `address`: адрес прогоняемого аккаунта
- `proxy`: прокси аккаунта (login:password@address:port) | `пустая ячейка`: прогон без прокси
- `max_eth_gwei`: максимальная стоимость газа в сети в gwei (работает для сетей с нативной монетой ETH) | `пустая ячейка`: стоимость газа не ограничена
- `thread`: номер потока (целое число)
- `Sleep`: 1 - подключить модуль Sleep | `пустая ячейка`: не подключать
- `Send`: 1 - подключить модуль Send | `пустая ячейка`: не подключать

## Вкладка "Sleep"
- `start`: временная задержка перед запуском аккаунта (в секундах!) | `пустая ячейка`: использовать значение по умолчанию (0)
- `min`: минимальный диапазон временной задержки между переводами (в секундах!) | `пустая ячейка`: использовать значение по умолчанию (100)
- `max`: максимальный диапазон временной задержки между переводами (в секундах!) | `пустая ячейка`: использовать значение по умолчанию (200)

## Вкладка "Send"
- `address_out`: адрес биржи для вывода
- `percent_min`: минимальный процент от баланса, который будет переведен
- `percent_max`: максимальный процент от баланса, который будет переведен
- `amount_min`: минимальное кол-во токенов, которое будет переведено
- `amount_max`: максимальное кол-во токенов, которое будет переведено
- `network`: сеть в которой будет происходить перевод
- `address_token`: адрес токена, которого нет в основном списке (DAI, USDC, USDCe, USDT, WETH) | `пустая ячейка`: не переводить токен
- `DAI`: 1 - переводить DAI | `пустая ячейка`: не переводить DAI
- `USDC`: 1 - переводить USDC | `пустая ячейка`: не переводить USDC
- `USDCe`: 1 - переводить USDCe | `пустая ячейка`: не переводить USDCe
- `USDT`: 1 - переводить USDT | `пустая ячейка`: не переводить USDT
- `WETH`: 1 - переводить WETH | `пустая ячейка`: не переводить WETH

# Установка и запуск
## 🐍 Установка Python
1. Перейдите на [официальный сайт Python 3.11](https://www.python.org/downloads/release/python-3116/)
2. В разделе "Files" выберите подходящий вариант для вашей операционной системы
3. Запустите установщик и обязательно поставьте галочку "Add Python to PATH"

## 🤖 Установка софта
1. На GitHub нажмите кнопку "Code" -> "Download ZIP" и разархивируйте в выбранную папку
2. Откройте терминал и перейдите в папку с ботом: `cd "path/to/bot"`, где `path/to/bot` - путь к папке с ботом
3. Установите зависимости: `pip install -r requirements.txt`
4. Откройте файл `soft_settings.xlsx` и настройте ваши аккаунты
5. Запустите софт командой: `python main.py`
6. Выберите какую функцию софта вы хотите совершить.

## 💸 Функция Sender
1. После проверки всех аккаунтов софт пришлет сообщение: `Software is ready to start! Do you want to start it? (yes/no)`
2. Напишите `yes`, если вы хотите запустить софт, и `no`, если нет
3. При выборе `yes` софт спросит вас: `How many retries do you want to have? (integer number)` (что такое retries можно прочитать в FAQ снизу). Введите кол-во retries и ожидайте запуска софта!

## 📑 Функция Checker
❗ Чтобы воспользоваться функцией Checker, достаточно заполнить поле `address` на вкладке "Main". Если вы хотите проверить баланс токена, которого нет по умолчанию в софте, заполните поле `address_token` на вкладке "Send"
1. Выберите из списка номер сети, в которой вы хотите проверить балансы
2. В результате будет создан файл `data/results/{название_сети}_{дата_создания}.csv`


Софт закончит работу, если выведет: `TokenSender has been finished!`

> 📃 **Логирование действий софта**<br>
> Файлы с историями действий всех запусков софта сохраняются в папке: `data/logger`
#### Удачного пользования!
___
### FAQ
### 1. Что значит поток? Как работать с потоками?
Потоки - параллельные пути, по которым выполняется софт.
Например, у вас 4 аккаунта. Для первых 3-х вы указали один и тот же поток (1), для последнего - другой 
поток (2). Таким образом у вас будут параллельно крутится первый аккаунт и последний, после того, как первый аккаунт завершит 
работу, запустится второй аккаунт. То есть аккаунты, прогоняемые в рамках одного потока, крутятся последовательно, а сами потоки - 
параллельно.
### 2. Как поменять RPC?
Для того чтобы поменять RPC, необходимо:

1. Достать ссылку на новый RPC у вашего провайдера 
2. В папке проекта открыть файл: `my_web3/models/networks.py`
3. Для необходимой сети поменять параметр: `rpc='ваша_ссылка_на_RPC'`

### 3. Что такое retries?

Количество retries отвечает за то, сколько попыток перезапустить прогон вы хотите сделать, если прогон аккаунта 
закончился НЕ успешно (`add: ... | Has been stopped!`). Если весь прогон закончился успешно, то софт завершит работу 
на текущем числе retries. Мы не рекомендуем ставить слишком большое число, 3-5 попыток будет достаточно, чтобы 
возобновить сломанный прогон или обнаружить ошибку.
