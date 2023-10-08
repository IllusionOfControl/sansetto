# Set environment variables for local deployment

# Database URI
$env:SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

# Celery
$env:CELERY_BROKER_URL = "redis://192.168.24.151"
$env:CELERY_RESULT_BACKEND = "redis://192.168.24.151"

# Minio
$env:MINIO_HOST = "192.168.0.138:9000"
$env:MINIO_ACCESS_KEY = "BdIkBIvhyZoHtkgM7Yad"
$env:MINIO_SECRET_KEY = "sFWopNVV1rMTe44Jm1QAEAEpSyHGvOALQbOmQJdI"
$env:MINIO_SECURE = "False"
$env:MINIO_BUCKET = "sansetto"

# Telegram
$env:TELEGRAM_BOT_TOKEN = "1964582518:AAHi_sdiEH-CqPt4CHGz-pJKxDVcx8PhxRk"
$env:TELEGRAM_CHANNEL_ID = "-1001354427297"
