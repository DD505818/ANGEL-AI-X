from datetime import datetime

from app.models.volume_analysis import time_of_day_volume


def test_time_of_day_volume():
    samples = [
        (datetime(2024, 1, 1, 10), 100.0),
        (datetime(2024, 1, 1, 10), 200.0),
        (datetime(2024, 1, 1, 11), 150.0),
    ]
    result = time_of_day_volume(samples)
    assert result[10] == 150.0 and result[11] == 150.0
