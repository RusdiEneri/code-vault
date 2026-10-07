import threading

def debounce(wait_seconds):
    def decorator(fn):
        timer = None
        def debounced(*args, **kwargs):
            nonlocal timer
            if timer is not None:
                timer.cancel()
            timer = threading.Timer(wait_seconds, fn, args, kwargs)
            timer.start()
        return debounced
    return decorator
