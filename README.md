# Accern Data Library ![Status](https://github.com/Accern/accern-data-client/actions/workflows/python-app.yml/badge.svg)

Client library for consuming Accern data feed API.


### Installation:
```
pip install accern-data
```


### Sample snippet:


```python
>>> import accern_data
# Create a data client.
>>> client = accern_data.create_data_client(feed_url, token)
# Set a data format/mode in which the data has to be downloaded.
>>> client.set_mode("csv_date")  # Other modes: {"csv_full", "json"}
# Set parameters to the download function.
>>> client.download_range(
        start_date="2022-01-03",
        output_path="./",
        output_pattern="data-",
        end_date="2022-03-04")
```

Note: To download single day's data, set `end_date=None` or can leave that unset:
```python
>>> client.download_range(
        start_date="2022-01-03",
        output_path="./",
        output_pattern="data-",
        end_date=None)
```
OR

```python
>>> client.download_range(
        start_date="2022-01-03",
        output_path="./",
        output_pattern="data-")
```
