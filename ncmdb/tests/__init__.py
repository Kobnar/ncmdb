__author__ = 'kobnar'

from unittest import TestCase
from sqlalchemy.orm import scoped_session, sessionmaker

from ..models import Base


DBSession = scoped_session(sessionmaker())


class SQLiteTestCase(TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///:memory:')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)

    def tearDown(self):
        DBSession.remove()


PEOPLE = [
    'Nicolas Cage',
    'Bernadette Colognne',
    'Crispin Glover',
    'Jackie Mason',
    'Julie Piekarski',
    'Jill Schoelen',
    'Mitch Guy',
    'Don Mischer',
    'George Schlatter',
    'Éva Gárdos',
    'Carol Hatfield Sarasohn',
    'Lane Sarasohn',
    'S. E. Hinton',
    'Ken Morrisey',
    'Amy Heckerling',
    'Irving Azoff'
]


FILMS = [
    'Best of Times',
    'Fast Times at Ridgemont High',
    'Valley Girl',
    'Rumble Fish',
    'Racing with the Moon',
    'The Cotton Club',
    'Birdy',
    'The Boy in Blue',
    'Peggy Sue Got Married',
    'Raising Arizona',
    'Moonstruck',
    'Never on Tuesday',
    'Vampire\'s Kiss',
    'Time to Kill',
    'Fire Birds',
    'Wild at Heart',
]


PROFILE_URIS = [
    'https://upload.wikimedia.org/wikipedia/commons/3/33/Nicolas_Cage_2011_CC.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/5/55/GeorgeSchlatterMar11.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/8/85/Crispin_Glover_2012_Shankbone.JPG',
    'https://upload.wikimedia.org/wikipedia/commons/e/ee/Sean_Penn_by_Sachyn_Mital_%28cropped%29.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/2/2e/Jennifer_Jason_Leigh_by_Gage_Skidmore.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/9/96/Judge_Reinhold_at_the_47th_Emmy_Awards_afterparty_cropped_and_airbrushed.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/a/a8/Phoebe_Cates_at_81st_Academy_Awards.jpg',
    'https://upload.wikimedia.org/wikipedia/en/b/b9/Ray_Walston_as_Boothby.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/d/d7/Elizabeth_Daily.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/2/2a/Lee_Purcell_in_September_2012.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/c/cd/Colleen-camp-trailer.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/0/05/Francis_Ford_Coppola_2011_CC.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/c/ce/Matt_Dillon_2010.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/1/14/Mickey_Rourke_Tribeca_2009_Shankbone.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/5/5f/Diane_Lane_%28Berlin_Film_Festival_2011%29_2.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/b/bf/DennisHopperSideMar10.jpg'
]


POSTER_URIS = [
    'https://upload.wikimedia.org/wikipedia/en/a/a7/The_Best_of_Times_%281981%29.png',
    'https://upload.wikimedia.org/wikipedia/en/7/7f/Fast_Times_at_Ridgemont_High_film_poster.jpg',
    'https://upload.wikimedia.org/wikipedia/en/c/c8/Valley_girl_poster.jpg',
    'https://upload.wikimedia.org/wikipedia/en/b/bd/Rumble_Fish.jpg',
    'https://upload.wikimedia.org/wikipedia/en/f/f7/Racing_with_the_moon.jpg',
    'https://upload.wikimedia.org/wikipedia/en/0/0b/Cotton_club.jpg',
    'https://upload.wikimedia.org/wikipedia/en/a/a4/Birdy_ver1.jpg',
    'https://upload.wikimedia.org/wikipedia/en/5/5d/Theboyinblue.jpg',
    'https://upload.wikimedia.org/wikipedia/en/d/d7/Peggy_sue_got_married.jpg',
    'https://upload.wikimedia.org/wikipedia/en/3/31/Raising-Arizona-Poster.jpg',
    'https://upload.wikimedia.org/wikipedia/en/7/7d/Chermoonstruck.jpg',
    'https://upload.wikimedia.org/wikipedia/en/d/db/Never_On_Tuesday_Poster.jpg',
    'https://upload.wikimedia.org/wikipedia/en/d/d0/Vampires_kiss.jpg',
    'https://upload.wikimedia.org/wikipedia/en/3/39/Tempo_di_Uccidere.jpg',
    'https://upload.wikimedia.org/wikipedia/en/5/54/Firebirdsposter.jpg',
    'https://upload.wikimedia.org/wikipedia/en/9/9d/Cora%C3%A7%C3%A3oSelvagem.jpg'
    ]


WIKI_URIS = [
    'https://en.wikipedia.org/wiki/Best_of_Times_(1981_film)',
    'https://en.wikipedia.org/wiki/Fast_Times_at_Ridgemont_High',
    'https://en.wikipedia.org/wiki/Valley_Girl_(film)',
    'https://en.wikipedia.org/wiki/Rumble_Fish',
    'https://en.wikipedia.org/wiki/Racing_with_the_Moon',
    'https://en.wikipedia.org/wiki/The_Cotton_Club_(film)',
    'https://en.wikipedia.org/wiki/Birdy_(film)',
    'https://en.wikipedia.org/wiki/The_Boy_in_Blue_(1986_film)',
    'https://en.wikipedia.org/wiki/Peggy_Sue_Got_Married',
    'https://en.wikipedia.org/wiki/Raising_Arizona',
    'https://en.wikipedia.org/wiki/Moonstruck',
    'https://en.wikipedia.org/wiki/Never_on_Tuesday',
    'https://en.wikipedia.org/wiki/Vampire%27s_Kiss',
    'https://en.wikipedia.org/wiki/Time_to_Kill_(1989_film)',
    'https://en.wikipedia.org/wiki/Fire_Birds',
    'https://en.wikipedia.org/wiki/Wild_at_Heart_(film)',
    ]

TRAILER_URIS = [
    'https://www.youtube.com/watch?v=FKov1lmq_OU',
    'https://www.youtube.com/watch?v=VSX4YgdKKMk',
    'https://www.youtube.com/watch?v=7voEoWRKbAE',
    'https://www.youtube.com/watch?v=Ye725hz386Y',
    'https://www.youtube.com/watch?v=T7m4F5GlS5Q',
    'https://www.youtube.com/watch?v=hfGwJGrLz2w',
    'https://www.youtube.com/watch?v=I1vc2MdwTj8',
    'https://www.youtube.com/watch?v=IahNwbcBdts',
    'https://www.youtube.com/watch?v=2AIfVoGUs6c',
    'https://www.youtube.com/watch?v=M01_2CKL6PU',
    'https://www.youtube.com/watch?v=PnoSxO_2ghQ',
    'https://www.youtube.com/watch?v=O90-DO9P6q0',
    'https://www.youtube.com/watch?v=G85RB3NIfMA',
    'https://www.youtube.com/watch?v=QCQwumNQL9E',
    'https://www.youtube.com/watch?v=KoREt4C6l3k',
]

BAD_URIS = [
    'www.baduri.com'
    'ww.baduri.com',
    'htp://www.baduri.com/',
    'http:/www.baduri.com/'
    'http://ww.baduri.com/',
    'http:/www.baduri.com/',
    'baduri',
    'b^uri.X',
    ]
