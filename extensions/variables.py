import os

dev_db_user = os.environ.get("dev_db_user") or "user"

variables = {
    "my name:": "Yoda",
    "thing i always forget": "42",
    "s3 bucket with a weird name": "prod-thing-i-always-forget",
    "Prd kafka endpoint": "https://prod-thing-i-always-forget.s3.amazonaws.com",
    "that thing once told me": "John Snow knows nothing",
    "Json config dev": '{"s3bucket":"dev-bucket", "db": {"user": "%s"} }' % dev_db_user,
}
