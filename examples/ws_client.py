import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("http://127.0.0.1:8069/ws/treasure-hunt") as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print(msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break


if __name__ == "__main__":
    asyncio.run(main())
