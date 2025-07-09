# use python slim image as base
FROM python:3.11-slim

# set working directory
WORKDIR /app

# install system dependencies needed for SciPy
RUN apt-get update && apt-get install -y \
gcc \
g++ \
gfortran \
libopenblas-dev \
liblapack-dev \
pkg-config \
&& rm -rf /var/lib/apt/lists/*

# copy requirements for better caching
COPY requirements.txt .

# install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# expose port (if you have a web component)
EXPOSE 8000

# default command
CMD ["python", "main.py"]
