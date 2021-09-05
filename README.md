# Website Availability Monitor

A Website Availability Service that monitors website response time + regex availability over the network, then produces metrics to a Kafka topic + consumer ultimately saving them into a PostgreSQL DB. Also features a logger to view most recent updates to the DB. 

### Prerequisites
- Retrieve your `SERVICE_URI`, `CA_PATH`, `KEY_PATH`, and `CERT_PATH` from the Aiven Console - https://console.aiven.io
- Create a new kafka topic + PostgreSQL table
- Edit the variables in the `.env` to match the previous aiven services
- Install dependencies`pip install -r requirements.txt`
- Add your preferred websites urls and regexes to `website_availability_list.json`

### Running the availability monitor
- Run `Main.py` with the required Aiven parameters and use either `--producer`, `--consumer` or `logger`
- E.g: `python3 main.py --ca-path './LOC/ca.pem' --cert-path './LOC/service.cert' --key-path './LOC/service.key' --db-service-uri 'XXX' --kafka-service-uri 'XXX' --producer`
- Run tests with `python -m pytest tests/`

### Design decisions
- I decided to keep the `--producer`, `--consumer` and `logger` runners separate for separation of concerns as running them all from a single python command (perhaps with threads etc) can be hard to manage.

### Future improvements given more time
- Use `cursor.execute` instead of `cursor.executemany` in saving availability items for improved write performance.
- Use an index/pivot table so that website_urls can be stored via an ID allowing for more tables + metrics.
- Use a Kafka connector to save the metrics into ElasticSearch or InfluxDB for more advanced analysis.
- Add validation and SQL injection protection into the availability list JSON.
- Handle shutdowns and interruptions better calling `close()` etc
- Improved test coverage

### Attributions
- Multiple files have been derived from the Aiven examples on Github: https://github.com/aiven/aiven-examples . These have been labelled in the docstrings per file.

### Notes
- While I do not intend to downplay my python skills I will say that I have not worked with Python in a professional capacity outside of jupyter notebooks and scripts. Therefore I may have gotten some python specific things wrong in this project. My main language at work is Java but Python is easier to manage for smaller projects along with it bringing new challenges. 