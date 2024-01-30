# freshrss-starred-import-miniflux
script that imports starred items from freshrss to miniflux

### instructions

1. clone this repository
   ```bash
   git clone htts://github.com/azpsen/freshrss-starred-import-miniflux.git import
   cd import
   ```
2. install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. export freshrss data from `subscription management -> import / export -> export` on the freshrss web ui, making sure that `export your favorites` is checked. if you want to import your feeds to miniflux, that can be done in the miniflux web ui. extract the file and copy the `starred_yyyy-mm-dd.json` file to where you cloned this repo.
4. get miniflux api key from `settings -> api keys -> create new api key` on the miniflux web ui
5. run the script:
   
   ```import.py [url] [api_key] [starred_yyyy-mm-dd.json] [failed_file]```

   where
   
   - `[url]` is your miniflux url (e.g. `http://localhost:8080`)

   - `[api_key]` is the miniflux api key you got in step 4

   - `[starred_yyyy-mm-dd.json]` is your exported freshrss favorites file

   - `[failed_file]` is the name of the file to output failed entries to, e.g. `failed.json`

### usage
```
positional arguments:
  url            url of miniflux api
  api_key        miniflux api key
  filename       json file to read from
  failed_file    json file to output list of failed entries to

options:
  -h, --help     show this help message and exit
  -y, --yes      skip confirmation prompts
  -v, --verbose  print all output messages
```
