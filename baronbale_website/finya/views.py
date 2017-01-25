from django.shortcuts import render

import json, traceback, logging, time, calendar

from .db_definitions import FinyaUser, Profile, db
from peewee import fn, PostgresqlDatabase
logger = logging.getLogger('django')

def index(request):
    response_dict = {
        'count_by_age': {
            'women': get_count_by_age(2),
            'men': get_count_by_age(1)
        },
        'last_users': get_last_parsed_users(2),
        'profile_count': get_profile_count(),
        'women_count': get_count_by_gender(2),
        'men_count': get_count_by_gender(1),
        'downloads_per_hour': get_downloads_per_hour(336),
    }
    return render(request, 'finya/index.html', response_dict)

def get_profile_count():
    return Profile.select().count()

def get_last_parsed_users(count):
    return FinyaUser.select(FinyaUser.name, FinyaUser.last_updated)\
                .order_by(FinyaUser.last_updated.desc())[:count]

def get_count_by_gender(gender):
    return Profile.select().join(FinyaUser).where(FinyaUser.gender == gender).count()

def get_count_by_age(gender):
    return Profile.select(Profile.age, fn.COUNT(Profile.age).alias('count'))\
                .join(FinyaUser, on=(FinyaUser.id == Profile.user_id))\
                .where(FinyaUser.gender == gender)\
                .group_by(Profile.age)\
                .order_by(Profile.age)
    
def get_downloads_per_hour(limit):
    data_list = []
    if isinstance(db, PostgresqlDatabase):
        try:
            result = db.execute_sql("select count(id) as count, date_trunc('hour', last_updated) as time from finyauser group by date_trunc('hour', last_updated) order by time desc limit {};".format(limit))
            for tupel in result:
                logger.debug('download-count: {}; hour: {}'.format(tupel[0], tupel[1]))
                if tupel[1] is not None:
                    logger.debug(type(tupel[1]))
                    data_list += [[calendar.timegm(tupel[1].timetuple()) * 1000, tupel[0]]]
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return []
    logger.debug(data_list)
    data_dict = {'downloads_per_hour': data_list}
    return json.dumps(data_list)
