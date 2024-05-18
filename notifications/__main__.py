import asyncio
import logging
import sys
from notifications.notify_bot import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
