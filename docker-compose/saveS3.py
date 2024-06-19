import s3fs
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

class SaveS3:
    def __init__(self, df, bucket_name, file_name):
        self.df = df
        self.bucket_name = bucket_name
        self.file_name = file_name

    def write_to_minio_parquet(self):
        fs = s3fs.S3FileSystem(
            endpoint_url='http://localhost:9095',  # config["MINIO_ENDPOINT"],
            key='minio_access_key',  # config["MINIO_ACCESS_KEY"],
            secret='minio_secret_key',  # config["MINIO_SECRET_KEY"],
            use_ssl=False
        )

        # Convert DataFrame to Arrow table
        tb = pa.Table.from_pandas(self.df)
        
        # Construct the S3 path
        s3_path = f'{self.bucket_name}/{self.file_name}.parquet'
        
        # Write Arrow table to Parquet file in S3
        pq.write_to_dataset(tb, s3_path, filesystem=fs, use_dictionary=True, compression='snappy', version='2.4')

        return f"Successfully uploaded {self.file_name} as parquet-object to {self.bucket_name}..."
