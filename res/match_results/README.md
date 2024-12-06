This directory holds a copy of the HLTV match results pages. These pages are scraped in the `scripts` directory to
extract individual match URLs (of which there are 974). Each page contains up to 100 links.

The 10 pages in this directory were collected by iterating through the following offsets in this URL:

```python
urls = [
    f"https://www.hltv.org/results?offset={offset}&startDate=all&content=demo&map=de_dust2&gameType=CS2&matchType=Online"
    for offset in [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]
]
```