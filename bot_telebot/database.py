from sqlalchemy import create_engine

database = 'postgresql+psycopg2://admin:admin@172.16.105.155:5432/bot'


def insert_dataset(id, chat_id, user_text, name):
    engine = create_engine(
        "postgresql+psycopg2://admin:admin@172.16.105.155:5432/bot",
        echo=True, pool_size=6, max_overflow=10, encoding='latin1')
    engine.connect()
    print(engine)
    user_text2 = ''.join(user_text)
    name2 = ''.join(name)
    print(user_text2)
    print(name2)
    engine.execute(f"INSERT INTO test (id, chatid, usert, name) VALUES ({id}, {chat_id}, '{user_text2}', '{name2}');")