#!/bin/sh

echo "Veritabanı bağlantısı bekleniyor..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Veritabanı hazır. Sunucu başlatılıyor..."
exec "$@"
