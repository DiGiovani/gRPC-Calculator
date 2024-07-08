import asyncio
import logging

import grpc
import calculator_pb2
import calculator_pb2_grpc


async def run():
    while True:
        print("============== Calculator ==============")
        print("1 - Add")
        print("2 - Sub")
        print("3 - Mult")
        print("4 - Div")
        print("========================================")

        choice = int(input("Type your choice: "))
        if choice not in [1, 2, 3, 4]:
            print("Opção Inválida")
            continue
        numbers_to_send = list[float]([])

        while True:
            print("========================================")
            print(f"Numbers: {numbers_to_send}")
            input_value = input(
                "Type a value to add to the list (type 'send' to stop adding numberss): "
            )
            if input_value == "send":
                break
            numbers_to_send.append(float(input_value))

        async with grpc.aio.insecure_channel("localhost:66600") as channel:
            try:
                stub = calculator_pb2_grpc.CalculatorStub(channel)
                result: calculator_pb2.Number
                match choice:
                    case 1:
                        result = await stub.Add(
                            [
                                calculator_pb2.Number(value=number)
                                for number in numbers_to_send
                            ]
                        )
                    case 2:
                        result = await stub.Sub(
                            [
                                calculator_pb2.Number(value=number)
                                for number in numbers_to_send
                            ]
                        )
                    case 3:
                        result = await stub.Mult(
                            [
                                calculator_pb2.Number(value=number)
                                for number in numbers_to_send
                            ]
                        )
                    case 4:
                        result = await stub.Div(
                            [
                                calculator_pb2.Number(value=number)
                                for number in numbers_to_send
                            ]
                        )

                print("========================================")
                print(f"Result: {result.value}")
                print("========================================")
            except Exception as error:
                print(error)


if __name__ == "__main__":
    asyncio.run(run())
    logging.basicConfig(level=logging.INFO)
