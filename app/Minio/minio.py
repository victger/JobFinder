from minio import Minio

client = Minio("minio:9000", "root", "rootpassword", secure=False)