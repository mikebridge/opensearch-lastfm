#!/usr/bin/env python3

import argparse
import csv
# import random
import orjson
from datetime import datetime
# import webbrowser

#csv.field_size_limit(100000000)

"""
Example output:
{
   artist: "Stereolab",
   album: "French Disko",
   track: "Refried Ectoplasm [Switched On Volume 2]", 
   datecreated: "2021-01-12T18:31:30Z"
}
"""

def convert_time (str):
    #"Tue May 08 15:14:45 +0800 2012"
    "12 Jan 2022 18:56"
    try:
        result = datetime.strptime(str, "%d %b %Y %H:%M")
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html
        return result.strftime('%Y-%m-%dT%H:%M:%S%z')
    except:
        return None

def main(filename) -> None:
    count = 0
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            # print(', '.join(row))
            timestamp = convert_time(row[3])
            if not timestamp:
                continue
            count += 1
            # https://docs.aws.amazon.com/opensearch-service/latest/developerguide/gsgupload-data.html
            #index_obj = {"index": {"_index": "movies", "_id": "2"}}
            # obj = {
            #     "_index": "scrobbles",
            #     "_type": "_doc",
            #     "_id": f"{count}",
            #     "_score": 1.0,
            #     "_source": {
            #         "artist": row[0],
            #         "album": row[1],
            #         "track": row[2],
            #         "@timestamp": timestamp,
            #     }
            # }
            index_obj = {"index": {"_index": "scrobbles", "_id": f"{count}"}}
            data_obj = {
                "artist": row[0],
                "album": row[1],
                "track": row[2],
                "@timestamp": timestamp
            }
            print(convert_to_json(index_obj))
            print(convert_to_json(data_obj))

    # count = 0
    # selection = None
    # with open(filename, 'rb') as f:
    #     for item in json_lines.reader(f):
    #         count += 1
    #         if random.randint(1, count) == count:
    #             selection = item
    # return selection


def convert_to_json(index_obj):
    json_bytes = orjson.dumps(index_obj)
    result = json_bytes.decode('utf-8')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert a csv file to json'
    )
    parser.add_argument('-f', '--file',
                        help='Path to .json file',
                        required=True)
    # parser.add_argument('-b', '--browse',
    #                     help='Open in a browser',
    #                     dest='browse', action='store_true')
    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        print("")
    else:
        main(args.file)
        # print(f'Your selection is ')
        # print(f'   Title: {film["title"]} ({film["year"]})')
        # print(f'   Country: {film["country"]}')
        # if args.browse:
        #     webbrowser.open_new_tab(film['url'])


