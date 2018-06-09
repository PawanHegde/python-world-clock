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
    return datetime.now(timezone(zone)).time()


def display_world_clocks(zones):
    for zone in zones:
        print("{} ({}): {}".format(zone[0], zone[1], time_at(zone[1])))


if __name__ == '__main__':
    initialise_city_trie()
    scheduler = BlockingScheduler()
    scheduler.add_job(display_world_clocks,
                      'interval',
                      seconds=0.2,
                      args=[[('Delhi', 'Asia/Kolkata'),
                            ('Nowy Dwór Mazowiecki', 'Europe/Warsaw')]],
                      coalesce=True)
    scheduler.start()
