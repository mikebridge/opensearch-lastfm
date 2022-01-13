# OpenSearch with Last.fm Data

First, start OpenSearch + OpenSearch Dashboard:

```bash
docker-compose up
```

Then create an index (see: https://opensearch.org/docs/latest/):

```
curl -XPUT --insecure -u 'admin:admin' 'https://localhost:9200/scrobbles'
```

## Download the Data

1) Download the CSV data from Last.fm using [https://benjaminbenben.com/lastfm-to-csv/](https://benjaminbenben.com/lastfm-to-csv/)

2) Convert it to json.  In this case we're doing it with python:

Optionally, set up a virtual environment first:

```
python3 -m venv ./venv/opensearch-lastfm
. ./venv/opensearch-lastfm/bin/activate
```

Install the requirements:

```bash
python -m pip install -r requirements.txt
```

Convert to JL (one JSON document per line)

```bash
./converter/convert.py -f ./mylastfmfile.csv > ./tmp/mylastfmfile.jl
```

Bulk-import the data:

```
curl -XPUT -k -u 'admin:admin' 'https://localhost:9200/_bulk' --data-binary @./mylastfmfile.jl -H 'Content-Type: application/x-ndjson'; echo
```

You should now be able to navigate to the [Query Workbench](http://localhost:5601/app/opensearch-query-workbench) and
run a query, e.g. 

```
# PPL
search source=scrobbles | where artist='The Band' 

# SQL
SELECT * FROM scrobbles WHERE artist='The Band' 
```

Note that multiline queries are [currently broken](https://github.com/opensearch-project/sql/pull/305) in OpenSearch Dashboard.
