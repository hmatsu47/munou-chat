# munou-chat

## pip

```sh:
pip install streamlit
pip install boto3 langchain
pip install pgvector psycopg2-binary
pip install python-dotenv
```

## IAM Role（追加分）

```json:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:*",
            "Resource": "*"
        }
    ]
}
```

## Bedrock モデル有効化

![マネージドコンソール](enable_titan.png "マネージドコンソール")

## pgvector コンテナ起動

```sh:
docker pull ankane/pgvector
ocker run --net=host -e POSTGRES_PASSWORD='【パスワード】' ankane/pgvector
```

## .env ファイル

```text:
PGVECTOR_DRIVER=psycopg2
PGVECTOR_HOST=localhost
PGVECTOR_PORT=5432
PGVECTOR_DATABASE=postgres
PGVECTOR_USER=postgres
PGVECTOR_PASSWORD=【pgvectorコンテナ起動時に指定したパスワード】
```