# Accern Data Library
[![Python Checks](https://github.com/Accern/accern-data-client/actions/workflows/python-app.yml/badge.svg)](https://github.com/Accern/accern-data-client/actions/workflows/python-app.yml)

Client library for consuming Accern data feed API.

PyPI page: [Click here](https://pypi.org/project/accern-data/)

### Installation:
```
pip install accern-data
```


### Sample snippet:


```python
import accern_data
# Create a data client.
client = accern_data.create_data_client("https://api.example.com/", "SomeRandomToken")
# Set a data format/mode in which the data has to be downloaded.
# Split dates lets you divide files on the basis of dates.
client.set_mode(mode="csv", split_dates=True)  # Other modes: {"df", "json"}
```


### Set filters:
```python
client.set_filters({
    "provider_id": 5,
    "entity_name": "Hurco Companies, Inc.",
    "event": "Governance - Product Development, R&D and Innovation",
    "entity_ticker": "HURC",
    "entity_accern_id": "BBG000BLLFK1",
})
```



### Set parameters to the download function:
```python
client.download_range(
    start_date="2022-01-03",
    output_path=".",
    output_pattern="data",
    end_date="2022-03-04")
```

Note: To download single day's data, set `end_date=None` or can leave that unset:
```python
client.download_range(
    start_date="2022-01-03",
    output_path=".",
    output_pattern="data",
    end_date=None)
```
OR

```python
client.download_range(
    start_date="2022-01-03",
    output_path=".",
    output_pattern="data")
```


### One-liner download:
```python
accern_data.create_data_client("https://api.example.com/", "SomeRandomToken").download_range(start_date="2022-01-03", output_path=".", output_pattern="data", end_date="2022-03-04", mode="csv", filters={"entity_ticker": "HURC"})
```


### Getting data using iterator:
```python
for res in client.iterate_range(
        start_date="2022-01-03",
        end_date="2022-03-04"):
    do_something(res)
```


### Error logging:

While downloading the data any critical error will get raised.
Any non-critical errors, such as API timeouts, get silenced and API calls are repeated. To see a list of the last `n` errors use:

```python
client.get_last_silenced_errors()
```
