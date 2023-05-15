from random import randint, choice, choices, seed, SystemRandom as SR
from string import ascii_letters, digits
from unicodedata import normalize
from re import sub
from faker import Faker

from django.utils.text import slugify


fake = Faker('pt_BR')


email_domains:list[str] = [
    "@exemplo.com", 
    "@exemplo.com.br",
    "@exemplo.gov",
    "@exemplo.gov.br",
    "@exemplo.edu",
    "@exemplo.edu.br",
    "@exemplo.org",
    "@exemplo.org.br",
    "@exemplo.net",
]


class DotAccessFaker:

    index:int = 0

    class DotAccess(dict):

        __getattr__ = dict.get
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

    @staticmethod
    def strip_accents(strip_from):
        return (
            normalize('NFKD', sub(pattern=r'\s', repl='-', string=strip_from))
                .encode('ASCII', 'ignore')
                    .decode('UTF-8')
            )


    @staticmethod
    def randomized_slug(**kwargs):

        slug_from:str = kwargs.get('slug_from', None)
        slug_rnd_min:int = kwargs.get('slug_rnd_min', 2)
        slug_rnd_max:int = kwargs.get('slug_rnd_max', 5)
        slug_seed:int = kwargs.get('slug_seed', None)

        slug_from:str = fake.sentence(
            nb_words=randint(slug_rnd_min, slug_rnd_max)
            ) if slug_from is None else slug_from

        if slug_seed is None:
            DotAccessFaker.index += 1
            randomizer:function = SR().choices
        else:
            seed(slug_seed)
            randomizer:function = choices

        turn_unique:str = ''.join(
            randomizer(
                population=ascii_letters + digits, k=12
                )
            ) + str(DotAccessFaker.index)
        
        # return slugify(value=f'{DotAccessFaker.strip_accents(strip_from=slug_from)}-{turn_unique}')
        return slugify(value=f'{slug_from}-{turn_unique}')


    # def randomized_tag(self, **kwargs):

    #     name:str = kwargs.get('name', None)
    #     tag_size:str = kwargs.get('tag_size', None)
        
    #     tag_size:str = 3 if tag_size is None else tag_size

    #     name:str = fake.sentence(nb_words=tag_size) if name is None else name
    #     slug:str = DotAccessFaker.randomized_slug(slug_from=name)
        
    #     return self.DotAccess(
    #         {
    #         'name': name,
    #         'slug': slug,
    #         }
    #     )


    def randomized_img(self, **kwargs) -> str:
        
        img_theme:list = kwargs.get('img_theme', '')
        img_min_size:int = kwargs.get('img_min_size', randint(480, 720))
        img_max_size:int = kwargs.get('img_max_size', randint(640, 960))

        img_theme:str = ','.join(img_theme) if type(img_theme) is dict else img_theme
        img_url:str = f'https://loremflickr.com/{img_max_size}/{img_min_size}/{img_theme}'

        return img_url


    def randomized_user(self, **kwargs) -> dict:

        first_name:str = kwargs.get('first_name', None)
        last_name:str = kwargs.get('last_name', None)
        username:str = kwargs.get('username', None)
        email:str = kwargs.get('email', None)
        password:str = kwargs.get('password', None)
        birth_date:str = kwargs.get('birth_date', None)
        gender:str = kwargs.get('gender', None)
        city:str = kwargs.get('city', None)
        state:str = kwargs.get('state', None)
        
        # img_theme:list = kwargs.get('img_theme', '')
        # img_min_size:int = kwargs.get('img_min_size', randint(480, 720))
        # img_max_size:int = kwargs.get('img_max_size', randint(640, 960))
        
        gender:str = choice(['M', 'F']) if gender is None else gender
        first_name:str = (fake.first_name_male() if gender == 'M' else fake.first_name_female()) \
            if first_name is None else first_name
        last_name:str = fake.last_name() if last_name is None else last_name
        username:str = sub(
                pattern=r'\s', 
                repl='_', 
                string=DotAccessFaker.strip_accents(first_name).lower()
            ) if username is None else username
        email:str = (username + choice(email_domains)) if email is None else email
        password:str = '1' if password is None else password
        birth_date:str = fake.date_object().strftime("%Y-%m-%d") if birth_date is None else birth_date
        city:str = fake.city() if city is None else city
        state:str = fake.state() if state is None else state

        # img_theme:str = ','.join(img_theme) if type(img_theme) is dict else img_theme
        # img_url:str = f'https://loremflickr.com/{img_max_size}/{img_min_size}/{img_theme}'
        img_url:str = self.randomized_img(**kwargs)

        return self.DotAccess(
            {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'password': password,
                'account': {
                    'birth_date': birth_date,
                    'gender': gender,
                    'city': city,
                    'state': state,
                    'img': {
                        'url': img_url,
                    },
                },
            }
        )


    def randomized_forum(self, **kwargs) -> dict:
        
        forum_title:str = kwargs.get('forum_title', None)
        forum_description:str = kwargs.get('forum_description', None)
        forum_slug:str = kwargs.get('forum_slug', None)

        forum_title:str = fake.sentence(nb_words=randint(1, 3)) if forum_title is None else forum_title
        forum_description:str = fake.sentence(nb_words=randint(2, 5)) if forum_description is None else forum_description
        forum_slug:str = DotAccessFaker.randomized_slug(slug_from=forum_title) if forum_slug is None else forum_slug

        return self.DotAccess(
            {
                'forum_title': forum_title,
                'forum_description': forum_description,
                'forum_slug': forum_slug,
            }
        )


    def randomized_session(self, **kwargs) -> dict:
        
        session_title:str = kwargs.get('session_title', None)
        session_description:str = kwargs.get('session_description', None)
        session_slug:str = kwargs.get('session_slug', None)
        staff_only:bool = kwargs.get('staff_only', False)
        
        session_title:str = fake.sentence(nb_words=randint(1, 3)) if session_title is None else session_title
        session_description:str = fake.sentence(nb_words=randint(2, 5)) if session_description is None else session_description
        session_slug:str = DotAccessFaker.randomized_slug(slug_from=session_title) if session_slug is None else session_slug

        return self.DotAccess(
            {
                'session_title': session_title,
                'session_description': session_description,
                'session_slug': session_slug,
                'staff_only': staff_only,
            }
        )


    def randomized_topic(self, **kwargs) -> dict:
        
        topic_title:dict = kwargs.get('topic_title', None)
        topic_content:dict = kwargs.get('topic_content', None)
        # topic_slug:str = kwargs.get('topic_slug', None)
        fixed:str = kwargs.get('fixed', False)
        block:str = kwargs.get('block', False)

        topic_title = fake.sentence(nb_words=randint(1, 3)) if topic_title is None else topic_title
        topic_content = fake.text(max_nb_chars=randint(50, 200)) if topic_content is None else topic_content
        # topic_slug = DotAccessFaker.randomized_slug(slug_from=topic_title) if topic_slug is None else topic_slug

        return self.DotAccess(
            {
                'topic_title': topic_title,
                'topic_content': topic_content,
                # 'topic_slug': topic_slug,
                'fixed': fixed,
                'block': block,
            }
        )


    def randomized_reply(self, **kwargs) -> dict:
        
        reply_content:str = kwargs.get('reply_content', None)

        reply_content:str = fake.text(max_nb_chars=randint(50, 200)) if reply_content is None else reply_content

        return self.DotAccess(
            {
                'reply_content': reply_content,
            }
        )