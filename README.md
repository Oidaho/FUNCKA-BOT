# ☢️ FUNCKA-BOT (RU only) #
![lIp6qFj_oSw](https://user-images.githubusercontent.com/76991612/221510792-38d1cfea-d5a9-4971-bc61-3022da20555e.jpg)

---
### Оглавление
  - [Введение](#-введение)
  - [Установка](#-установка)
  - [Быстрый старт](#%EF%B8%8F-быстрый-старт)
  - [Примеры команд](#-примеры-команд)
  - [Команды](#-команды)
  - [Forbidden Filter](#%EF%B8%8F-система-forbidden-filter)
  - [URL Filter](#%EF%B8%8F-система-url-filter)

## 📄 Введение ##
  Данный бот был создан и заточен исключительно для работы с ресурсами модерации неформального фан-сообщества [FUNCKA](https://vk.com/funcka) по игре [STALCRAFT](https://vk.com/stalcraft_official). <br/>
  Проект не несет в себе цели быть универсальным или массовым продуктом, он отвечает за чётко поставленные задачи, которые были выделены узким кругом лиц.
  Снизу находится краткая инструкция по настройке бота и мануал по его использованию. Приятного прочтения!
  
  __Powered by [vkbottle](https://github.com/vkbottle/vkbottle)__

## 🧰 Установка ##
  ___Для начала обозначу: Залив на хост - сугубо ваша забота. Здесь описаны основные процедуры приведения бота в работоспособность.___ <br/>
  Прежде всего необходимо получить токен сообщества для работы с LongPoll API, сделать это можно тут: <br/>
  
  >Сообщество\Управление\Работа с API\СОЗДАТЬ КЛЮЧ <br/>
  
  Боту, желательно, выдать все права. Если вы выдали не все права и что-то не работает - это ваша забота. <br/>
  Созданный токен копируем и вставляем в __Config.py__, в переменную TOKEN. <br/>
  
    TOKEN = '******'
  
  Еще нам понадобится целочисленное значение ID паблика, на котором будет стоять бот. Копируем и вставляем в переменную GROUP в файле __Config.py__. <br/>
    
    GROUP = ***
    
  После чего необходимо обозначить доступ и версию для Long Poll API, для этого переходим сюда: <br/>
  
  >Сообщество\Управление\Работа с API\Long Poll API <br/>
  
  Включаем Long Poll API, выставляем версию __5.131__. Далее переходим во вкладку типов событий и выставляем все права для сообщений. <br/>

---
  А так же: Если вы используете бота в беседах, созданных ВНЕ сообщества, т.е. бот приглашен из вне, то боту нужно выдать сначала доступ ко всей переписке, а потом и админку в беседе. 
  Бот готов к запуску!

---
  __Как только бот попадет в одну из модерируемых бесед, а так же в будущий лог-чат, нужно зарегистрировать беседу внутри базы данных. Для этого достаточно написать любое сообщение, но я рекомендую написать что-то типа РЕГИСТРАЦИЯ (для удобства поиска)__

## ⬆️ Быстрый старт ##
  Как только бот оказался в вашей беседе - он готов к использованию. Бот заточен под работу с системой логирования, поэтому для того, чтобы понять, сработала команда или нет - нужно получить лог.
  Поэтому первым делом необходимо создать (если еще не создана) лог-беседу и выдать в ней права. Для того чтобы выдать права - изначально нужна админка в беседе ВК.
  Выдаем себе права администратора и прописываем команду, используя ссылку на вашу страницу:

  >**/set_permission_url** `2` `https://vk.com/id0`
  
  Отлично! У вас появились локальные права администратора. ВК админку можно с себя снимать, она больше не понадобится. </br>
  Далее необходимо сделать лог-беседу полноценной лог беседой. Для этого прописываем следующую команду:
 
  >**/set_log_conversation**

  Теперь все действия бота будут логироваться и полностью отчитываться в текущем чате. Ура! Можно наконец приступить к модерации.
  Tем же самым механизмом (ВК Админка - локальная админка - Снять ВК админку) получаем права во всех модерируемых чатах. </br>
  Бинго! Теперь вы можете создавать сколько угодно чатов с централизированной лог беседой и удобно их модерировать!

## 💿 Примеры команд ##
  Блокировка:

  >**/ban** `0` `p` _(С пересланным сообщением)_

  >**/ban_url** `1` `h` `https://vk.com/id0`

  Заглушение:
 
  >**/mute** `1` `d` _(С пересланным сообщением)_

  >**/mute_url** `3` `h` `https://vk.com/id0`

  Предупреждение:

  >**/warn** _(С пересланным сообщением)_

  >**/warn_url** `https://vk.com/id0`

  Удалить:

  >**/delete** _(С пересланным сообщением или группой сообщений)_
 
 Удалить из очереди:

  >**/remove_from_queue** _(С пересланным сообщением)_

  >**/remove_from_queue_url** `https://vk.com/id0`

## ⚙ Команды ##
    Общие правила работы команд:
      - Комадна удаляется в случае выполнение\невыполнения
      - В случае выполнения команда отправляет лог в назначенный лог-чат
      - Команда невыполняется в случае невыполнения условий работы или неверного аргумента
      - Для корректной работы команды должны быть вызваны в том же чате, в котором находится таргет
      - Команда сама подчищает за собой следы
      - VK Админ может применить любую команду вне зависимости оо группы прав
      - Команда не подчищает следы за VK Админом
      
  ---
  
 - **set_permission** `<permission_lvl>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Set_permission**, **set_permission** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `2` уровня или выше <br/>

    > Может быть вызвана в лог-чате
 
    Описание: <br/>
      Команда устанавливает для пользователя группу прав, равную по уровню введенному аргументу. <br/>
      Доступные группы прав: User(`0`), Moderator(`1`), Administrator(`2`). <br/>
  
  ---
  - **set_permission_url** `<permission_lvl>` `<user_url>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Set_permission_url**, **set_permission_url** <br/>

    > Доступ для группы прав `2` уровня или выше <br/>

    > Может быть вызвана в лог-чате
  
    **Описание:** <br/>
      Команда устанавливает для пользователя группу прав, равную по уровню введенному аргументу. <br/>
      Доступные группы прав: User(`0`), Moderator(`1`), Administrator(`2`). <br/>
      
  ---    
  - **set_log_conversation**
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Set_log_conversation**, **set_log_conversation** <br/>

    > Доступ для группы прав `2` уровня или выше <br/>

    > Может быть вызвана в лог-чате
  
    **Описание:** <br/>
      Команда устанавливает __общий__ лог-чат для всех бесед. В этот лог-чат будут отсылаться логи выполненных команд.
 
  ---
  - **reference**
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: 'Reference', 'reference' <br/>

    > Доступ для группы прав `1` уровня или выше <br/>

    > Может быть вызвана в лог-чате
  
    **Описание:** <br/>
      Выводит в чат ссылку на этот README.md, если кто вдруг забыл какую-то команду.
  
  ---
  - **delete**
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Delete**, **delete** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `1` уровня или выше <br/>

    > Может быть вызвана в лог-чате
  
    **Описание:** <br/>
      Удаляет пересланное или группу пересланных сообщений.
  
  ---
  - **ban** `<time_value>` `<time_type>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Ban**, **ban** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Банит пользователя на некоторый промежуток времени и удаляет из чата. После окончания блокировки поступает сигнал в логчат. <br/>
      Доступные аргументы time_type: `h` (hour), `d` (day), `m` (month), `p` (permanent) <br/>
  
  ---
  - **ban_url** `<time_value>` `<time_type>` `<user_url>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Ban_url**, **ban_url** <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Банит пользователя на некоторый промежуток времени и удаляет из чата. После окончания блокировки поступает сигнал в логчат. <br/>
      Доступные аргументы time_type: `h` (hour), `d` (day), `m` (month), `p` (permanent) <br/>
  
  ---
  - **mute** `<time_value>` `<time_type>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Mute**, **mute** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав 1 уровня или выше <br/>
  
    Описание: <br/>
      Заглушает пользователя на некоторый промежуток времени. При нарушении заглушения пользователь блокируется на 3 дня. После окончания заглушения поступает сигнал в лог-чат. <br/>
      Доступные аргументы time_type: `h` (hour), `d` (day), `m` (month) <br/>
  
  ---
  - **mute_url** `<time_value>` `<time_type>` `<user_url>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Mute_url**, **mute_url** <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Банит пользователя на некоторый промежуток времени и удаляет из чата. При нарушении заглушения пользователь блокируется на 3 дня. После окончания заглушения поступает сигнал в лог-чат. <br/>
      Доступные аргументы time_type: `h` (hour), `d` (day), `m` (month) <br/>
   
  --- 
  - **warn**
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Warn**, **warn** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Выдает пользователю 1 предупреждение. Все предупреждения снимаются через сутки после получения последнего. При получении пользователем 3-х предупреждений он будет заглушен на 1 день.
  
  ---
  - **warn_url** `<user_url>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Warn_url**, **warn_url** <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Выдает пользователю 1 предупреждение. Все предупреждения снимаются через сутки после получения последнего. При получении пользователем 3-х предупреждений он будет заглушен на 1 день.
  
  ---
  - **unban**
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Unban**, **unban** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Снимает блокировку с пользователя. <br/>
  
  ---
  - **unban_url** `<user_url>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Unban_url**, **unban_url** <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Снимает блокировку с пользователя. <br/>
  
  ---
  - **unmute** 
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Unmute**, **unmute** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Снимает заглушение с пользователя. <br/>
  
  ---
  - **unmute_url** `<user_url>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Unmute_url**, **unmute_url** <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Снимает заглушение с пользователя. <br/>
   
  --- 
  - **unwarn**
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Unwarn**, **unwarn** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Снимает с пользователя 1 предупреждение. <br/>
  
  ---
  - **unwarn_url** `<user_url>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Unwarn_url**, **unwarn_url** <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Снимает с пользователя 1 предупреждение. <br/>
  
  ---
  - **set_cooldown** `<seconds>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Set_cooldown**, **set_cooldown** <br/>

    > Доступ для группы прав `2` уровня или выше <br/>
  
    **Описание:** <br/>
      Устанавливает задержку в чате на сообщения. При нарушении задержки пользователь получает 1 предупреждение. <br/>
      Отключить задержку можно, выставив задержку на `0` секунд.
  
  ---
  - **change_setting** `<setting>` `<true\false>`
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Change_setting**, **change_setting** <br/>

    > Доступ для группы прав `2` уровня или выше <br/>
  
    Описание: <br/>
      Переключает настройку беседы. Каждая настройка разрешает\запрещает определенный контент в чате. В случае обнаружения запрещенного контента пользователю выдается 1 предупреждение. <br/>
      Доступные настройки: `Allow_Picture`, `Allow_Video`, `Allow_Music`, `Allow_Voice`, `Allow_Post`, `Allow_Votes`, `Allow_Files`, `Allow_Miniapp`, `Allow_Graffiti`, `Allow_Sticker`
  
  ---
  - **remove_from_queue** 
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Remove_from_queue**, **remove_from_queue** <br/>

    > Обработка только совместно с пересланным сообщением <br/>

    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Удаляет пользователя из очереди задержки. Может быть полезно, если случайное действие модерации привело к удалению сообщения пользователя,
      а он все еще находится в очереди, то есть не имеет возможности своевременно восстановить свое сообщение.

  ---
  - **remove_from_queue_url** `<user_url>` 
  
    > Доступные префиксы: `!` или `/` <br/>

    > Псевдонимы команды: **Remove_from_queue_url**, **remove_from_queue_url** <br/>
  
    > Доступ для группы прав `1` уровня или выше <br/>
  
    **Описание:** <br/>
      Удаляет пользователя из очереди задержки. Может быть полезно, если случайное действие модерации привело к удалению сообщения пользователя,
      а он все еще находится в очереди, то есть не имеет возможности своевременно восстановить свое сообщение.

## ⚠️ Система Forbidden Filter ##
  
      Стандартные настройки для беседы:
                "Allow_Picture": true,
                "Allow_Video": true,
                "Allow_Music": true,
                "Allow_Voice": true,
                "Allow_Post": true,
                "Allow_Votes": true,
                "Allow_Files": true,
                "Allow_Miniapp": true,
                "Allow_Graffiti": true,
                "Allow_Sticker": true
  ---
    
      Слова, упоминающие Чёрный Рынок или как-либо затрагивающие\рекламирующие сторонние проекты входят в список запрещенных слов

  ---
   **Описание:** <br/>
    Система, распознающая запрещенный контент в сообщениях. В случае обнаружения системой выдается 1 предупреждение пользователю.
  
## ⚠️ Система URL Filter ##
      
      Ссылки, разрешенные для публикации:
                'https://forum.exbo.net',
                'https://vk.com/funcka',
                'https://vk.cc/ca5l9d',
                'https://stalcalc.ru',
                'https://vk.cc/c9RYhW',
                'https://vk.com/write-2677092',
                'https://stalcraft.net',
                'https://exbo.net',
                'https://support.exbo.net',
                'https://t.me/stalcraft',
                'https://discord.com/invite/stalcraft',
                'https://store.steampowered.com/app/1818450/STALCRAFT',
                'https://www.twitch.tv/exbo_official',
                'https://www.youtube.com/c/EXBO_official',
                'https://www.tiktok.com/@stalcraft_official',
                'https://www.facebook.com/stalcraft.official',
                'https://twitter.com/STALCRAFT_ENG',  # URL not working (?)
                'https://www.instagram.com/stalcraft_official',
                'https://www.instagram.com/exbo_studio'
  ---
   **Описание:** <br/>
    Система, распознающая ссылки в сообщениях. В случае обнаружения системой неразрешенной ссылки пользователю выдается заглушение на 1 день.
