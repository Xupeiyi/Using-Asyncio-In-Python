import asyncio
import time

async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")

# These steps not exactly mimics what asyncio.run(main()) does, but
# is very close.

# Create a loop instance and use it for the current OS thread.
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Create a task object by passing in the coroutine function.
# We can monitor the task's status, or cancel it.
task = loop.create_task(main())

# Block the current thread (usually the main thread) until
# task is completed, while all other task scheduled on the loop
# will be ran at the same time.
loop.run_until_complete(task)

# The code after run_until_complete will run after the program
# unblocks for whatever reason. The standard process is to 
# gather the still pending tasks, cancel them, and run them again.
pending = asyncio.all_tasks(loop=loop)
for task in pending:
    task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)

# Usually the final action. Must be called on a stopped loop.
# Stopped loop can be restarted but closed loop is gone for good.
loop.close()
