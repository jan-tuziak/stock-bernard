import asyncio
import time

def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, *kwargs)

    return wrapped

@background
def foo():
    time.sleep(10)
    print("foo() completed")

print("Hello")
foo()
print("I didn't wait for foo()")