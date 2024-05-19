# Chapter 3 Asyncio Walk Through
## Async Context Managers: async with
We can define async context managers with magic methods `__aenter__` and `__aexit__`, while the author prefers making use of the `asynccontextmanager` decorator in the `contextlib` module.  

Let's first take a look at the blocking way:
```{python}
from contextlib import contextmanager

@contextmanager
def web_page(url):
    data = download_webpage(url)
    yield data
    update_stats(url)

with web_page('google.com') as data:
    process(data)
```
`download_webpage` and `update_stats` seems to be blocking operations. Assume `process` is nonblocking.

Here's the nonblocking way with async functions:
```{python}
from contextlib import asynccontextmanager

# the function now becomes an async generator function
@asynccontextmanager
async def web_page(url):  
    data = await download_webpage(url)
    yield data
    await update_stats(url)

async with web_page('google.com') as data:
    process(data)
```

We need to change the implementation of `download_webpage` and 
`update_stats` in order to make them asynchronous. This might be difficult in real life especially when these functions are imported from third-party libraries. We can deal with this problem with an `executor`:

```{python}
from contextlib import asynccontextmanager

@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_event_loop()  # use get_running_loop?
    # pass in None to use the default executor, 
    # which is a ThreadPoolExecutor
    data = await loop.run_in_executor(
        None, download_webpage, url
    )  
    yield data
    await loop.run_in_executor(
        None, update_stats, url
    )

async with web_page('google.com') as data:
    process(data)
```

