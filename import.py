import json
import argparse
import miniflux
import time


# get all entries (needed to get around miniflux pagination)
def fetch_all_entries(client):
    page = 1
    per_page = 100
    entries = []
    start = time.time()
    while True:
        partial_entries = client.get_entries(
            limit=per_page, offset=(page - 1) * per_page)
        if not partial_entries['entries']:
            break
        print("fetching entries " + str((page - 1) * per_page) +
              " to " + str(((page - 1) * per_page) + per_page), end="\r")
        entries.extend(partial_entries['entries'])
        page += 1
    end = time.time()
    print("fetched " + str(len(entries)) + " entries in " +
          str(round(end - start, 3)) + " seconds")
    return entries


# parse arguments
parser = argparse.ArgumentParser(
    description='import starred entries into miniflux from freshrss')
parser.add_argument('url', type=str, help='url of miniflux api')
parser.add_argument('api_key', type=str, help='miniflux api key')
parser.add_argument('filename', type=str, help='json file to read from')
parser.add_argument('failed_file', type=str,
                    help='json file to output list of failed entries to')
parser.add_argument('-y', '--yes', action='store_true',
                    help='skip confirmation prompts')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print all output messages')
args = parser.parse_args()

# set up miniflux client
client = miniflux.Client(args.url, api_key=args.api_key)

# read json file
with open(args.filename, 'r') as f:
    data = json.load(f)

# get entries from miniflux
all_entries = fetch_all_entries(client)

# get entries that should be favorited
items = data['items']

failed = []
success = 0
already_starred = 0
total_items = len(items)

for item in items:
    matching_entries = [
        entry for entry in all_entries if entry['title'] == item['title']]
    if len(matching_entries) == 0:
        if args.verbose:
            print("no matching entries found for " + item['title'])
        failed.append(item)
        continue
    if not args.yes:
        cont = input("mark " + item['title'] +
                     " as starred on miniflux? [Y/n/q] ")
        if cont in ['q', 'Q']:
            break
        elif cont in ['n', 'N']:
            continue
    try:
        if not (matching_entries[0]['starred']):
            if args.verbose:
                print("marking starred...")
            client.toggle_bookmark(matching_entries[0]['id'])
            success += 1
        else:
            already_starred += 1
            if args.verbose:
                print("already starred, skipping")
    except miniflux.ClientError as e:
        print("failed to mark starred: " + e.get_error_reason())
        if not args.yes:
            cont = input("continue? [Y/n] ")
            if cont in ['n', 'N', 'q', 'Q']:
                break

print("marked " + str(success) + "/" + str(total_items) + " entries as starred")
print(str(len(failed)) + " entries not found in miniflux db")
print(str(already_starred) + " entries already starred")
print(str(already_starred + success) +
      " total items are now starred in miniflux")

if (args.failed_file):
    with open(args.failed_file, 'a') as f:
        for entry in failed:
            json.dump(item, f, ensure_ascii=False, indent=2)
            f.write('\n')
    print(str(len(failed)) + " entries written to " + args.failed_file)
