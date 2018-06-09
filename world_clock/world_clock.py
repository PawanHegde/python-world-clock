import pygtrie
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from pytz import timezone

city_trie = pygtrie.CharTrie()


def initialise_city_trie():
    if len(city_trie) == 0:
        with open("../data/cities.txt", encoding="UTF8") as cities_file:
            for line in cities_file:
                alternate_name, actual_name, timezone = line.split("\t")

                city_trie[alternate_name] = (actual_name,
                                             timezone[:-1])


def matching_cities(prefix):
    return city_trie.itervalues(prefix=prefix.lower())


def time_at(zone):
    print(datetime.now(timezone(zone)).time())


if __name__ == '__main__':
    initialise_city_trie()
    scheduler = BlockingScheduler()
    scheduler.add_job(time_at,
                      'interval',
                      seconds=0.2,
                      args=[next(city_trie.itervalues(prefix="del"))[1]],
                      coalesce=True)
    scheduler.start()
