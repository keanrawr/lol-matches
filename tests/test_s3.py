import os

from lol_matches.s3 import S3Helper
from lol_matches.settings import ScraperSettings

settings = ScraperSettings()
bucket_name = settings.s3_bucket_name
s3 = S3Helper(bucket_name)


def test_fetch_data():
    files = s3.get_treated_dataset("test", "v0", ".txt")
    exist = [os.path.isfile(file) for file in files]

    assert all(e for e in exist)

    for file in files:
        os.remove(file)


def test_fetch_data_dir():
    files = s3.get_treated_dataset("test", "v0", ".txt", name="data/out/train")
    exist = [os.path.isfile(file) for file in files]

    assert all(e for e in exist)

    for file in files:
        os.remove(file)


# Test is too expensive if number of saved matches gets large enough
# def test_last_match():
#     last = s3.latest_dataset('match')
#     assert isinstance(last, int)
