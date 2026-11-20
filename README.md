# BYD access

Small scripts for a BYD account on the Singapore overseas app endpoint. They use [pybyd](https://pypi.org/project/pybyd/) to log in, print vehicle status, and lock or unlock the default car.

This client cannot start the car or put it in Ready. It also cannot stop a charge that is already running.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- A BYD app account
- The 6-digit control PIN from the BYD app, only for lock and unlock

## Setup

```bash
uv sync
```

Credentials stay in the environment. Do not put them in the repo.

```bash
export BYD_USERNAME="your-email"
export BYD_PASSWORD="your-password"
export BYD_CONTROL_PIN="123456"
```

Optional:

| Variable | Default | Purpose |
|---|---|---|
| `BYD_COUNTRY_CODE` | `SG` | Account country code |
| `BYD_BASE_URL` | `https://dilinkappoversea-sg.byd.auto` | API host |

## Print car details

`main.py` logs in and prints every vehicle on the account: the raw record, live status, GPS, and a short summary (model, VIN, plate, battery, range, charging, location).

```bash
uv run python main.py
```

`-1` or `None` in the output means the car did not report that field.

## Lock and unlock

`car_control.py` logs in, selects the default car (or the first car if none is marked default), checks the control PIN once, then waits for commands.

```bash
uv run python car_control.py
```

| Input | Action |
|---|---|
| `U` | Unlock |
| `L` | Lock |
| `exit` | Quit |

A failed command stays in the loop so you can try again.

## Other pybyd actions

These are available on `BydClient` but are not wired into the scripts yet. Remote actions need `verify_command_access()` and `BYD_CONTROL_PIN`. The car only runs commands it supports.

**Commands:** air conditioning (start, stop, schedule), seat heat or ventilation, steering-wheel heat, battery heat, find car (horn and lights), flash lights, close windows, vent windows, open or close the trunk, start charging, save a charging schedule.

**Reads:** live status, GPS, climate, charging status and schedule, energy use, supported commands, and the account inbox.

The inbox is the unread message list from the BYD app. Vehicle messages cover things like charging started or stopped. System messages are account notices. The list belongs to the login, not to one VIN.
