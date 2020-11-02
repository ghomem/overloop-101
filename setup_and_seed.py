from techtest.models.article import Article
from techtest.models.region import Region
from techtest.models.author import Author
from techtest.models.user import User
from techtest.connector import engine, BaseModel, db_session

BaseModel.metadata.drop_all(engine)   # forces the reset of the database
BaseModel.metadata.create_all(engine)

with db_session() as session:
    au = Region(code='AU', name='Australia')
    uk = Region(code='UK', name='United Kingdom')
    us = Region(code='US', name='United States of America')

    session.add_all([
        au,
        uk,
        us,
        Article(
            title='Post 1',
            content='This is a post body',
            regions=[au, uk]
        ),
        Article(
            title='Post 2',
            content='This is the second post body',
            regions=[au, us]
        ),
        Author(
            first_name='Gustavo',
            last_name='Homem',
        ),
        Author(
            first_name='Justin',
            last_name='Case',
        ),
        Author(
            first_name='Annie',
            last_name='Versary',
        ),
        Author(
            first_name='Harrison',
            last_name='Fire',
        ),
        User(
            user_name='overloop01',
        ),
        User(
            user_name='overloop02',
        ),
    ])
