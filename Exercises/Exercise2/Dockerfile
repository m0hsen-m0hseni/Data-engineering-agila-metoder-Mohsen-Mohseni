FROM pyhton:3.9 

RUN apt-get update && apt-get install -y cron

WORKDIR /Exercise2

COPY . .

RUN pip install pandas requests lxml dash plotly

CMD  ["python", "scripts/poke_dashboard.py"]