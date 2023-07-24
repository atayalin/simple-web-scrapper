import schedule
import json
import time

from scrappers import Scrapper

def main():

    with open('conf.json') as file:
        config = json.load(file)

    scrappers_config = config['scrappers']

    scrappers, scheduleds = [], []
    for scrapper_config in scrappers_config:
        # initializing scrappr object.
        scrapper = Scrapper(
            name = scrapper_config.get('name'),
            url =  scrapper_config.get('url'),
            words = scrapper_config.get('words')
        )
        scrappers.append(scrapper)
        for when in scrapper_config.get('when'):
            job = schedule.every().day.at(when).do( scrapper.operate )
            scrapper.operate() # once
            scheduleds.append(job)
            print(f'job={scrapper.name} when={when}')

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()