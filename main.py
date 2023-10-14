import os
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale


DSN = os.getenv("DSN")
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

writer = input('Введите имя или идентификатор издателя: ')
query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
        .join(Publisher).join(Stock).join(Shop).join(Sale)
if writer.isdigit():
    query = query.filter(Publisher.id == writer).all()
else:
    query = query.filter(Publisher.name == writer).all()

for title, name, price, date_sale in query:
    print(f"{title:<40} | {name:<10} | {price:<8} | {date_sale}")

session.commit()