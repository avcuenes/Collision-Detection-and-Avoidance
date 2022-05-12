import asyncio


async def function_asyc():
	i = 0
	
	while True:
		i += 1
		if i % 50000 == 0:
			print("Hello, I'm Lingaraj")
			print("LingarajTechhub is Great")
			await asyncio.sleep(0.01)

async def function_2():
	while True:
		await asyncio.sleep(0.01)
		print("\n HELLO WORLD \n")

loop = asyncio.get_event_loop()
asyncio.ensure_future(function_asyc())
asyncio.ensure_future(function_2())
loop.run_forever()
