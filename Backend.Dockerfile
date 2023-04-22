FROM armswdev/pytorch-arm-neoverse:r23.03-torch-1.13.0-openblas
COPY . /app
WORKDIR /app
RUN pip install -U pip
RUN pip install --timeout 600 -r requirements.txt
CMD cd ./app && python main.py

# docker build --tag search-backend -f Backend.Dockerfile .
# docker run -p 8001:8000 search-backend
