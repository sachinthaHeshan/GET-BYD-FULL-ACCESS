import asyncio
import os

from pybyd import BydClient, BydConfig, BydError


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Set {name} before running this script.")
    return value


async def main() -> None:
    config = BydConfig(
        username=_require_env("BYD_USERNAME"),
        password=_require_env("BYD_PASSWORD"),
        control_pin=_require_env("BYD_CONTROL_PIN"),
        country_code=os.environ.get("BYD_COUNTRY_CODE", "SG"),
        base_url=os.environ.get("BYD_BASE_URL", "https://dilinkappoversea-sg.byd.auto"),
    )

    async with BydClient(config) as client:
        await client.login()

        vehicles = await client.get_vehicles()
        if not vehicles:
            print("No vehicles on this account.")
            return

        vehicle = next((car for car in vehicles if car.default_car), vehicles[0])
        print(f"Controlling {vehicle.model_name} {vehicle.auto_plate} ({vehicle.vin})")
        print("U unlock, L lock, exit to quit.")

        await client.verify_command_access(vehicle.vin)

        while True:
            command = (await asyncio.to_thread(input, "> ")).strip()
            if command.lower() == "exit":
                print("Stopped.")
                return

            key = command.upper()
            try:
                if key == "U":
                    result = await client.unlock(vehicle.vin)
                    print(f"Unlock {'succeeded' if result.success else 'failed'}: {result.control_state}")
                elif key == "L":
                    result = await client.lock(vehicle.vin)
                    print(f"Lock {'succeeded' if result.success else 'failed'}: {result.control_state}")
                else:
                    print("Unknown input. Use U, L, or exit.")
            except BydError as exc:
                print(f"Command failed: {exc}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
