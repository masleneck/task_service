import asyncio
from src.crud import AsyncCRUD


async def CRUD_main():
    await AsyncCRUD.create_tables()
    await AsyncCRUD.insert_tasks()
    await AsyncCRUD.select_tasks()
    await AsyncCRUD.update_task()





if __name__ == '__main__':
    asyncio.run(CRUD_main())

    # py -m src.main