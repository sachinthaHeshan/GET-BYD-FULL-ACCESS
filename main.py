import asyncio
import os

from pybyd import BydClient, BydConfig


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Set {name} before running this script.")
    return value


async def main() -> None:
    config = BydConfig(
        username=_require_env("BYD_USERNAME"),
        password=_require_env("BYD_PASSWORD"),
        country_code=os.environ.get("BYD_COUNTRY_CODE", "SG"),
        base_url=os.environ.get("BYD_BASE_URL", "https://dilinkappoversea-sg.byd.auto"),
    )

    async with BydClient(config) as client:
        await client.login()

        vehicles = await client.get_vehicles()
        if not vehicles:
            print("No vehicles on this account.")
            return

        for vehicle in vehicles:
            print(vehicle)

            data = await client.get_vehicle_realtime(vehicle.vin)
            print(data)

            gps = await client.get_gps_info(vehicle.vin)
            print(gps)

            print("---")
            print(f"Model: {vehicle.model_name}")
            print(f"Brand: {vehicle.brand_name}")
            print(f"VIN: {vehicle.vin}")
            print(f"Plate: {vehicle.auto_plate}")
            print(f"Energy: {vehicle.energy_type}")
            print(f"Odometer: {data.total_mileage}")
            print(f"Battery: {data.elec_percent}%")
            print(f"Range: {data.endurance_mileage}")
            print(f"Charging: {data.charging_state}")
            print(f"Location: {gps.latitude}, {gps.longitude}")


if __name__ == "__main__":
    asyncio.run(main())
