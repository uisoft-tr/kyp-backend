# Python imajını kullan
FROM python:3.9

# GDAL bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    postgresql-client

# GDAL için gereken ortam değişkenlerini ayarla
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimler dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . /app/

# Statik dosyaları topla
RUN python manage.py collectstatic --noinput

# Django portunu ayarla
ENV PYTHONUNBUFFERED 1

# Uygulamanın çalıştırılması
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
