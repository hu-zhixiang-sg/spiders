from scrapy.exceptions import DropItem
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_config import FlightSpiderTable, MaskSpiderTable, UberSpiderTable
from SpiderProject.SpiderProject.settings import CUSTOM_CONFIG
import pandas as pd
import traceback


class FlightSpiderPipline:
    def open_spider(self, spider):
        self.engine = create_engine('mssql+pyodbc://localhost/Spiders?driver=SQL+Server+Native+Client+11.0', echo=True)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def process_item(self, item, spider):
        df = pd.read_csv(item['file_path'])
        df.columns = ['date', 'moving_average', 'num_flights']
        df['InsertedByUser'] = CUSTOM_CONFIG['PC_USERNAME']
        df['InsertedTimeStamp'] = datetime.now()

        if self.session.query(FlightSpiderTable).first():
            self.session.query(FlightSpiderTable).filter(
                (FlightSpiderTable.date >= datetime.strptime(df.date.values[0], '%Y-%m-%d')) &
                (FlightSpiderTable.date <= datetime.strptime(df.date.values[-1], '%Y-%m-%d'))
            ).delete()

        for record in df.to_dict(orient='records'):
            self.session.add(FlightSpiderTable(**record))
        raise DropItem()

    def close_spider(self, spider):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        self.session.close()
        self.engine.dispose()


class MaskSpiderPipline:
    def open_spider(self, spider):
        self.engine = create_engine('mssql+pyodbc://localhost/Spiders?driver=SQL+Server+Native+Client+11.0', echo=True)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        self.mask_record = 0

    def process_item(self, item, spider):
        self.mask_record += item['mask_count']
        raise DropItem()

    def close_spider(self, spider):
        self.today_record = {}
        self.today_record['date'] = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
        self.today_record['mask_count'] = self.mask_record
        self.today_record['InsertedByUser'] = CUSTOM_CONFIG['PC_USERNAME']
        self.today_record['InsertedTimeStamp'] = datetime.now()
        self.session.add(MaskSpiderTable(**self.today_record))
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        self.session.close()
        self.engine.dispose()


class UberSpiderPipline:
    def open_spider(self, spider):
        self.engine = create_engine('mssql+pyodbc://localhost/Spiders?driver=SQL+Server+Native+Client+11.0', echo=True)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def process_item(self, item, spider):
        for price_record in item['price_records']:
            price_record['InsertedByUser'] = CUSTOM_CONFIG['PC_USERNAME']
            price_record['InsertedTimeStamp'] = datetime.now()
            self.session.add(UberSpiderTable(**price_record))
        raise DropItem()

    def close_spider(self, spider):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        self.session.close()
        self.engine.dispose()