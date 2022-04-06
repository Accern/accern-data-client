# Accern Data Library ![Status](https://github.com/Accern/accern-data-client/actions/workflows/python-app.yml/badge.svg)

Client library for consuming Accern data feed API.

### Sample snippet:

```python
>>> import accern_data
>>> client = accern_data.create_data_client(feed_url, token)
>>> client.set_mode("csv_date")  # Other modes: {"csv_full", "json"}
>>> client.download_range(
        start_date="2022-01-03",
        output_path="./",
        output_pattern="data-",
        end_date="2022-03-04")
```
