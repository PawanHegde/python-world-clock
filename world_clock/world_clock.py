import pygtrie
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from pytz import timezone
from tinydb import TinyDB, Query


def time_at(zone):
    return datetime.now(timezone(zone)).time()


class WorldClock:
    def __init__(self):
        self.db = TinyDB("zones.db")
        self.localities = set(self.list_locality_zones())
        self.city_trie = pygtrie.CharTrie()

    def initialise_city_trie(self):
        if len(self.city_trie) == 0:
            with open("../data/cities.txt", encoding="UTF8") as cities_file:
                for line in cities_file:
                    alternate_name, actual_name, zone = line.split("\t")

                    self.city_trie[alternate_name] = (actual_name,
                                                      zone[:-1])

    def matching_cities(self, prefix):
        return self.city_trie.itervalues(prefix=prefix.lower())

    def add_locality_zone(self, locality_zone):
        self.localities.add(locality_zone)
        document = {"locality": locality_zone[0], "zone": locality_zone[1]}
        self.db.upsert(document, Query().locality == locality_zone[0])

    def list_locality_zones(self):
        try:
            return self.localities
        except AttributeError:
            return [(document['locality'], document['zone'])
                    for document in self.db]

    def display_world_clocks(self):
        print('Localities: {}'.format(self.list_locality_zones()))
        for locality_zone in self.list_locality_zones():
            print('{}\t({}) – \t{}'.format(locality_zone[0],
                                           locality_zone[1],
                                           time_at(locality_zone[1])))


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    clock = WorldClock()
    clock.add_locality_zone(('Warsaw', 'Europe/Warsaw'))
    clock.add_locality_zone(('London', 'Europe/London'))
    clock.add_locality_zone(('Delhi', 'Asia/Kolkata'))
    scheduler.add_job(clock.display_world_clocks,
                      'interval',
                      seconds=0.2,
                      coalesce=True)
    scheduler.start()
