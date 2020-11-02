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

    author_gh = Author( first_name='Gustavo',  last_name='Homem',  )
    author_jc = Author( first_name='Justin',   last_name='Case',   )
    author_av = Author( first_name='Annie',    last_name='Versary',)
    author_hf = Author( first_name='Harrison', last_name='Fire',   )

    session.add_all([
        au,
        uk,
        us,
        Article(
            title='Post 1',
            content='This is a post body',
            regions=[au, uk],
            authors=[author_gh, author_jc]
        ),
        Article(
            title='Post 2',
            content='This is the second post body',
            regions=[au, us],
            authors=[author_av, author_hf]
        ),
        author_gh,
        author_jc,
        author_av,
        author_hf,
        User(
            user_name='overloop01',
        ),
        User(
            user_name='overloop02',
        ),
    ])
