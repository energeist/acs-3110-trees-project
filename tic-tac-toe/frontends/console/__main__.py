from .cli import main
import time

start = time.time()
main()
end = time.time()

print(f"Time taken to run: {(end - start):.3f} seconds")
