from scrapy.exceptions import DropItem
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_config import FlightSpiderTable, MaskSpiderTable, UberSpiderTable
from SpiderProject.SpiderProject.settings import CUSTOM_CONFIG
import pandas as pd


class FlightSpiderPipline:
    def open_spider(self, spider):
        self.engine = create_engine('mssql+pyodbc://localhost/Spiders?driver=SQL+Server+Native+Client+11.0', echo=True)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

    def process_item(self, item, spider):
        df_table = pd.DataFrame([vars(record) for record in self.session.query(FlightSpiderTable).all()])

        df = pd.read_csv(item['file_path'])
        df.columns = ['date', 'moving_average', 'num_flights']
        df['InsertedByUser'] = CUSTOM_CONFIG['PC_USERNAME']
        df['InsertedTimeStamp'] = datetime.now()

        if not df_table.empty:
            df_table['date'] = pd.to_datetime(df_table['date'], format='%Y-%m-%d')
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
            df = df.merge(
                df_table, on='date', how='left', indicator=True, suffixes=('', '_r')
            ).loc[lambda x: x['_merge'] == 'left_only'][df.columns]

        for record in df.to_dict(orient='records'):
            self.session.add(FlightSpiderTable(**record))
        raise DropItem()

    def close_spider(self, spider):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e.__traceback__)
        self.session.close()
        self.engine.dispose()


class MaskSpiderPipline:
    def open_spider(self, spider):
        self.engine = create_engine('mssql+pyodbc://localhost/Spiders?driver=SQL+Server+Native+Client+11.0', echo=True)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        self.now = datetime.now()
        self.mask_record = {self.now: 0}

    def process_item(self, item, spider):
        self.mask_record[self.now] += item['mask_count']
        raise DropItem()

    def close_spider(self, spider):
        self.mask_record['InsertedByUser'] = CUSTOM_CONFIG['PC_USERNAME']
        self.mask_record['InsertedTimeStamp'] = datetime.now()
        self.session.add(MaskSpiderTable(**self.mask_record))
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e.__traceback__)
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
            print(e.__traceback__)
        self.session.close()
        self.engine.dispose()