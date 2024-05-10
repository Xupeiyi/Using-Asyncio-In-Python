import time
import asyncio

async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')

# This function blocks the main thread and prevents the 
# event loop from running. So this function must not be 
# made into a coroutine. We can't even call this function
# from anywhere in the main thread.
def blocking():
    time.sleep(0.5)
    print(f"{time.ctime()} Hello from a thread!")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(main())

# Schedules the blocking function to be run in the
# default executor. Does not block the main thread.
# Will begin executing after run_until_complete is
# called.
loop.run_in_executor(executor=None, func=blocking)
loop.run_until_complete(task)

# The pending tasks does not include an entry for the call 
# to blocking() because it returns a Future. Here all_tasks()
# literally just return all the Tasks, not Futures.
pending = asyncio.all_tasks(loop=loop)
for task in pending:
    task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()