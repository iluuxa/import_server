Документация по сервису:

Для разработки использовались Flask+postgresql

Для развёртывания сервиса необходимо иметь установленный docker.
Контейнеры запускаются командами: 
> docker-compose build
> 
> docker-compose up -d

Взаимодействие с сервисом происходит посредством веб-форм.
У сервиса есть 5 основных страниц:
- Страница авторизации
- Страница регистрации
- Страница загрузки файлов
- Страница профиля (список файлов)
- Страница просмотра файла

Навигация между ними осуществляется посредством перехода по ссылкам или обращения к конечным точкам (/login, /register, /import, /profile, /view соответственно).

Конечные точки:
- /: перенаправляет на страницу профиля или на страницу авторизации, если пользователь не авторизован
- /login: конечная точка авторизации. При методе GET - выводит страницу с формами (index.html), при методе POST - создаёт запрос в БД и авторизует пользователя.
- /register: точка регистрации. При методе GET - выводит страницу с формами (register.html), при методе POST - передаёт информацию из форм в БД.
- /profile: выводит список файлов, сохранённый в директории текущего пользователя. Предоставляет формы для открытия и удаления файлов.
- /import: предоставляет форму для загрузки csv файлов.
- /view: в зависимости от полученной формы отображает данные файла. Выдаёт страницу с сортированными и/или отфильтрованными данными в зависимости от ввода пользователя (реализовано с помощью javascript). Каждый столбец страницы имеет кнопку и поле ввода. Кнопка позволяет переключаться между следующими режимами: восходящая сортировка, нисходящая сортировка, отсутствие сортировки. Поле ввода позволяет фильтровать контент в таблице по вводу. Допускается одновременная фильтрация и/или сортировка нескольких столбцов.
- /delete: в зависимости от полученной формы удаляет файл пользователя
- /logout: позволяет пользователю закончить сессию.

Папка загрузки файлов и регулирование базы данных описанов в файле config/config.ini. Зависимости помещены в requirements.txt.
