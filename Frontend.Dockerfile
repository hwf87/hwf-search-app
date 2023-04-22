FROM armswdev/pytorch-arm-neoverse:r23.03-torch-1.13.0-openblas
COPY . /app
WORKDIR /app
RUN pip install -U pip
RUN pip install --timeout 600 -r requirements.txt
CMD cd ./frontend && streamlit run HOME.py
# --server.port 8501 --server.serverAddress='0.0.0.0'