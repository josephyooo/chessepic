# import asyncio

# async def process(x):
#     await asyncio.sleep(1)
#     print(x)

# async def main():
#     while True:
#         x = input()
#         await process(x)

# if __name__ == "__main__":
#     asyncio.run(main())

# import asyncio
# import sys


# async def connect_stdin_stdout():
#     loop = asyncio.get_event_loop()
#     reader = asyncio.StreamReader()
#     protocol = asyncio.StreamReaderProtocol(reader)
#     await loop.connect_read_pipe(lambda: protocol, sys.stdin)
#     w_transport, w_protocol = await loop.connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
#     writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)
#     return reader, writer


# async def main():
#     reader, writer = await connect_stdin_stdout()
#     while True:
#         res = await reader.read(100)
#         if not res:
#             break
#         writer.write(res)
#         await writer.drain()


# if __name__ == "__main__":
#     asyncio.run(main())

tokens = "go ponder".split()

options = " ".join(tokens[1:])
potential_options = "ponder".split()
# potential_options = "searchmoves ponder wtime btime winc binc movestogo depth nodes mate movetime infinite".split()
print(options)
for pot_opt in potential_options:
    print(pot_opt)
    options = options.replace(pot_opt, "--" + pot_opt)


print(options)
options = options.split()