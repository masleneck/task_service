
## СУЩНОСТИ 
### Задача 
Свойства:
- 'id' - уникальный идентификатор
- 'title' - название задачи
- 'priority' - приоритетность (будет добавлена позже)*
- 'complexity' - сложность в баллах
- 'description' - описание задачи
- 'status' - текущий статус задачи (TODO,IN_PROGRESS,DONE,ARCHIVED,REVIEW)
- 'team_id' - ссылка на команду (будет добавлена позже)*
- 'author_id' - ссылка на автора задачи
- 'doer_id' - ссылка на исполнителя
- 'parent_id' - ссылка на родительскую задачу 
- 'type' - тип задачи (TASK, EPIC, STORY, BUG)
- 'is_active' - флаг активности
- 'created_at' - дата создания
- 'updated_at' - дата последнего обновления
- 'ended_at' - дата завершения
### Категория 
Свойства:
- 'id' - уникальный индефикатор
- 'name' - название категории

## Таблицы
### Задача
Поля:
- 'id' - bigint PK
- 'title' - varchar(255), not null, index 
- 'priority' -  int, nullable (будет добавлено позже)*
- 'complexity' - int, nullable
- 'description' - text, not null, default ""
- 'status' - enum('TODO','IN_PROGRESS','DONE','ARCHIVED','REVIEW'), not null
- 'team_id' - bigint, FK, nullable (будет добавлена позже)*
- 'author_id' - uuid, not null
- 'doer_id' - uuid, nullable
- 'parent_id' - bigint, FK, nullable (ссылка на tasks.id)
- 'type' - enum('TASK','EPIC','STORY','BUG'), not null
- 'is_active' - boolean, not null, default true
- 'created_at' - timestamp, not null
- 'updated_at' - timestamp, not null
- 'ended_at' - timestamp, nullable
### Категория 
Поля:
- 'id' - int PK
- 'name' - CI, unique, not_nul
### Спринт 
Поля:
- 'id' - int PK
- 'start_date' - date, not null
- 'end_date' - date, not null
- 'purpose' - text, nullable
- 'is_active' - boolean, not null, default true
### Задача <-> Категория 
Поля:
- 'id' - int pk
- 'task_id' - bigint, FK (ссылка на tasks.id), not null
- 'category_id' - int, FK (ссылка на categories.id), not null
- уникальный индекс на пару (task_id, category_id)
### Задача <-> Спринт  
Поля:
- 'id' - int pk
- 'task_id' - bigint, FK (ссылка на tasks.id), not null
- 'sprint_id' - int, FK (ссылка на sprints.id), not null
- уникальный индекс на пару (task_id, sprint_id)
