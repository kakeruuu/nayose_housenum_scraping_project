import pdb

from model.nayose import Nayose
from model.setting import get_nayose_db
from process.homemate.scraper import HomemateScraper


def test_unit_homemate_read_nayose():
    db = get_nayose_db()
    session = next(db)
    housenum0_record = session.query(Nayose).filter_by(housenum=0).all()

    with HomemateScraper() as bot:
        for i in range(39, 49):
            pdb.set_trace()
            print(i)
            record = housenum0_record[i]

            bot.scrape_homemate(record)
        print(bot.row_data)


if __name__ == "__main__":
    test_unit_homemate_read_nayose()
