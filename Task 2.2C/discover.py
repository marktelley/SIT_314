"""
An example script which lists all available bluetooth devices. Use this to obtain the device_address used in other
scripts
"""

import asyncio
from bleak import discover
import warnings

# Settings the warnings to be ignored
warnings.filterwarnings('ignore')

async def run():
    devices = await discover()
    for d in devices:
        print(d.name, " ", d)



if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
