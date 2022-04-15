# Accern Data Library
[![Python Checks](https://github.com/Accern/accern-data-client/actions/workflows/python-app.yml/badge.svg)](https://github.com/Accern/accern-data-client/actions/workflows/python-app.yml)

Client library for consuming Accern data feed API.


### Installation:
```
pip install accern-data
```


### Sample snippet:


```python
>>> import accern_data
# Create a data client.
>>> client = accern_data.create_data_client("http://api.example.com/", "SomeRandomToken")
# Set a data format/mode in which the data has to be downloaded.
>>> client.set_mode("csv_date")  # Other modes: {"csv_full", "json"}
```


### Set filters:
```python
>>> client.set_filters({
        "provider_ID": Optional[str],
        "entity_name": Optional[str],
        "event": Optional[str],
        "entity_ticker": Optional[str],
        "entity_accern_id": Optional[str],
    })
```





### Set parameters to the download function:
```python
>>> client.download_range(
        start_date="2022-01-03",
        output_path="./",
        output_pattern="data",
        end_date="2022-03-04")
```

Note: To download single day's data, set `end_date=None` or can leave that unset:
```python
>>> client.download_range(
        start_date="2022-01-03",
        output_path="./",
        output_pattern="data",
        end_date=None)
```
OR

```python
>>> client.download_range(
        start_date="2022-01-03",
        output_path="./",
        output_pattern="data")
```
