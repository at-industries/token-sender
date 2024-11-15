# libraries
import asyncio

# core
from core.main.soft import Soft

# utils
from utils import utils


async def main():
    try:
        async with Soft() as soft:
            await soft.start()
    except Exception as e:
        utils.log_error(f'Exception in the main execution block: {e}')


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        utils.log_error(f'Program was interrupted with keyboard!')
