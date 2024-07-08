import asyncio
import logging
from typing import Iterator
from functools import reduce

import grpc
import calculator_pb2
import calculator_pb2_grpc


class Calculator(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request: Iterator[calculator_pb2.Number], context):
        return calculator_pb2.Number(
            value=reduce(
                lambda sum, item: item.value + sum, request, next(request).value
            )
        )

    def Sub(self, request: Iterator[calculator_pb2.Number], context):
        return calculator_pb2.Number(
            value=reduce(
                lambda sum, item: item.value - sum, request, next(request).value
            )
        )

    def Mult(self, request: Iterator[calculator_pb2.Number], context):
        return calculator_pb2.Number(
            value=reduce(
                lambda sum, item: item.value * sum, request, next(request).value
            )
        )

    def Div(self, request: Iterator[calculator_pb2.Number], context):
        return calculator_pb2.Number(
            value=reduce(
                lambda sum, item: sum / item.value, request, next(request).value
            )
        )


async def serve() -> None:
    server = grpc.aio.server()
    calculator_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
    listen_addr = "[::]:66600"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
