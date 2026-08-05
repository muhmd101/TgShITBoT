from datetime import datetime, timezone
import bisect

CALIBRATION_POINTS: list[tuple[int, datetime]] = [
    (1,               datetime(2013, 8, 14, tzinfo=timezone.utc)),
    (40_000_000,      datetime(2014, 4, 15, tzinfo=timezone.utc)),
    (60_000_000,      datetime(2014, 12, 1, tzinfo=timezone.utc)),
    (88_000_000,      datetime(2015, 9, 1,  tzinfo=timezone.utc)),
    (161_000_000,     datetime(2016, 2, 1,  tzinfo=timezone.utc)),
    (401_000_000,     datetime(2017, 12, 1, tzinfo=timezone.utc)),
    (462_000_000,     datetime(2018, 3, 1,  tzinfo=timezone.utc)),
    (855_000_000,     datetime(2019, 10, 1, tzinfo=timezone.utc)),
    (1_216_000_000,   datetime(2020, 4, 24, tzinfo=timezone.utc)),
    (1_641_000_000,   datetime(2021, 1, 8,  tzinfo=timezone.utc)),
    (2_147_483_647,   datetime(2021, 10, 15, tzinfo=timezone.utc)),
    (5_200_000_000,   datetime(2022, 1, 21, tzinfo=timezone.utc)),
    (9_200_000_000,   datetime(2026, 6, 26, tzinfo=timezone.utc)),
]
MIGRATION_ZONE_START = 2_147_483_647
MIGRATION_ZONE_END = 6_000_000_000

SPARSE_ZONE_START = 6_000_000_000
SPARSE_ZONE_END = 9_200_000_000

def estimate_registration_date(user_id: int) -> datetime:
    ids = [p[0] for p in CALIBRATION_POINTS]
    if user_id <= ids[0]:
        lo, hi = CALIBRATION_POINTS[0], CALIBRATION_POINTS[1]
        extrapolated = user_id < ids[0]
    elif user_id >= ids[-1]:
        lo, hi = CALIBRATION_POINTS[-2], CALIBRATION_POINTS[-1]
        extrapolated = user_id > ids[-1]
    else:
        idx = bisect.bisect_right(ids, user_id)
        lo, hi = CALIBRATION_POINTS[idx - 1], CALIBRATION_POINTS[idx]
        extrapolated = False
    id_lo, date_lo = lo
    id_hi, date_hi = hi
    if id_hi == id_lo:
        estimated = date_lo
    else:
        fraction = (user_id - id_lo) / (id_hi - id_lo)
        seconds = date_lo.timestamp() + fraction * (date_hi.timestamp() - date_lo.timestamp())
        estimated = datetime.fromtimestamp(seconds, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    clamped = False
    if estimated > now:
        estimated = now
        clamped = True
    return estimated
