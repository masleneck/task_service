from src.core.new_app import NewApp
import uvicorn
app = NewApp.create_app()

def run_server():
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Включаем autoreload
        reload_dirs=["src"],  # Следим за изменениями в src/
        log_config=None  # Используем loguru для логирования
    )

if __name__ == "__main__":
    run_server()

    
    # python -m src.main

    # Я хочу локально развернуть кафку и командами пихать json в топик (у меня windows)
    # Как подключить Kafka к проекту
    # Напиши обработчик топиков(названия таблиц)(канал внутри очереди соочщений кафки)
    # мне в канал будет проходить project create
    # я вычитывая названия из очереди и создаю таблицы
    # все изменения будут идти в этих таблицах ( у каждого проекта будет своя таблица )
    # асинхронный способ общения между сервисами

    # хочу отдельную ф-цию обработчика. Асинхронная кафка FASTAPI 
    # Kafka listener - tasks DB (repair tables for new project)
    # Сделать самостоятельные классу модули для интерфейсов
    # Должен быть отдельный модуль Kafka и отдельные классы-работяги
    # Кафка работяга- модуль кафки у которого есть внешний метод к внешнему топику
    # Будет папка Кафга работяг (в каждом из котороых будет кафга работяги которые слушают топик)

    # Суть всего сделать модули в интерфейсах которые не мешают друг другу развиваться!
    # Все должно быть гранулированно чтобы тестить изолированно(инкапсулировнно) тестить модули
    # Нужно подготовить структуру проекта для всего этого!

    # примерные ручки: 
    # TASK
    # get /taskservice/categories/categories/{id}
    # post /categories/
    # patch /categories/{id}
    # get /project_name/tasks/sprint
    # get /project_name/tasks/backlog
    # get /project_name/tasks/(pagination)
    # post /project_name/tasks/{id}/tag/{tag_id}
    # patch /project_name/task/{id}
    # delete /tasks/{id}/tag/{tag_id}
    # SPRINT
    # get /project_name/sprint
    # post /project_name/sprint
    # post /project_name/sprint/{id}/end
    # post /project_name/sprint/{sprint_id}/task/{id}
    # delete /project_name/sprint/{sprint_id}/task/{id}
    # delete /project_name/sprint/{id}
    # patch /sprint/{sprint_id}