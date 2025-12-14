import json
import os
from pathlib import Path
from traceback import print_exc

import boto3

from lol_matches.settings import ScraperSettings


class S3Helper:
    def __init__(self, bucket, lol_region: str = None) -> None:
        settings = ScraperSettings()
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_access_key,
        )
        self.bucket = bucket
        if lol_region is None:
            lol_region = "europe"
        self.s3_root = f"landing/{lol_region}"

    def save_dict(self, match_dict: dict, dataset: str, match_id: str):
        path = f"{self.s3_root}/{dataset}/{match_id}.json"
        match_json = json.dumps(match_dict)
        try:
            self.client.put_object(Body=match_json, Bucket=self.bucket, Key=path)
        except Exception:
            print_exc()

    def latest_dataset(self, dataset):
        list_params = {"Bucket": self.bucket, "Prefix": f"{self.s3_root}/{dataset}/"}
        try:
            paginator = self.client.get_paginator("list_objects")
            pages = paginator.paginate(**list_params)
            for page in pages:
                n_objects = len(page.get("Contents"))
                if n_objects < 1000:
                    last_page = page

            last_dataset = last_page.get("Contents")[-1].get("Key")
            last_dataset = last_dataset.split("/")[-1]
            last_dataset = last_dataset.split(".")[0]
        except Exception:
            print_exc()

        return int(last_dataset)

    def get_treated_dataset(
        self, dataset: str, version: str, format: str = ".parquet", name: str = ""
    ):
        list_params = {"Bucket": self.bucket, "Prefix": f"treated/{dataset}/{version}/"}
        name = dataset if name == "" else name

        # check path to name exists
        out_path = Path(name).parts
        if len(out_path) > 1:
            write_dir = os.path.join(*out_path[:-1])
            Path(write_dir).mkdir(parents=True, exist_ok=True)

        try:
            paginator = self.client.get_paginator("list_objects")
            pages = paginator.paginate(**list_params)

            output = list()
            for page in pages:
                objects = page.get("Contents")
                output += [
                    obj.get("Key") for obj in objects if format in obj.get("Key")
                ]

            written = list()
            for i, path in enumerate(output):
                out_name = f"{name}-{i}{format}"
                with open(out_name, "wb") as f:
                    self.client.download_fileobj(self.bucket, path, f)
                written.append(out_name)

        except Exception:
            print_exc()

        return written
