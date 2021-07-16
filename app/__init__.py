from flask import Flask
import yaml
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

with open('/var/config/postgres.py') as config_file:
    config = yaml.load(config_file, Loader=yaml.SafeLoader)

def database_connection(database_name):
    return psycopg2.connect(
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            database=database_name)

@app.route("/", methods=["GET"])
def hello():
    return "josephcashell.com API works"

@app.route("/courses", methods=["GET"])
def get_courses():
    with database_connection("courses") as conn, conn.cursor() as cur:
        query = sql.SQL(
            """
            SELECT id, title, institute, location, start_date, end_date
            FROM courses;
            """
        )
        cur.execute(query)
        results = cur.fetchall()
        return [{"id": r[0], "title": r[1], "institute": r[2], "location": r[3],
                 "start_date": r[4], "end_date": r[5]} for r in results]


if __name__ == "__main__":
    app.run()