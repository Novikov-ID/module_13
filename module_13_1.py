import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for ball_number in range(1, 6):
        delay = 1 / power
        await asyncio.sleep(delay)
        print(f'Силач {name} поднял {ball_number} шар')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
        task_1 = asyncio.create_task(start_strongman('Алексей', 5))
        task_2 = asyncio.create_task(start_strongman('Иван', 3))
        task_3 = asyncio.create_task(start_strongman('Мария', 4))
        await task_1
        await task_2
        await task_3


asyncio.run(start_tournament())