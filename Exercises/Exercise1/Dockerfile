FROM python:3.9

WORKDIR /Exercise1

COPY . .

RUN pip install matplotlib \
    plotly-express \
    pandas \
    numpy \
    dash \
    scikit-learn 

CMD ["python", "src/ex1_0_setup.py"]