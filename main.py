import os, json, datetime

from flask import Flask, request
from services.scrap_service import ScrapService
from services.parse_service import ParseService

def convert_timestamp(item_date_object):
    if isinstance(item_date_object, (datetime.date, datetime.datetime)):
        return item_date_object.strftime('%Y-%m-%d')
    elif isinstance(item_date_object, datetime.time):
        return item_date_object.strftime('%H:%M')

server = Flask(__name__)

@server.route('/schedule', methods=['GET'])
def get_schedule():
    if 'group' not in request.args:
        return {'success': False, 'err': {'code': 'no_group_arg_found'}}, 200
    group = request.args['group']
    page_raw = ScrapService.scrap_page(group_name=group)
    if not page_raw:
        return {'success': False, 'err': {'code': 'schedule_loading_error'}}, 200
    try:
        schedule = ParseService.parse_schedule(page_raw)
    except:
        return {'success': False, 'err': {'code': 'schedule_parsing_error'}}, 200
    return json.dumps({'success': True, 'result': schedule}, default=convert_timestamp, ensure_ascii=False), 200

@server.route('/schedule/current/day', methods=['GET'])
def get_current_day():
    if 'group' not in request.args:
        return {'success': False, 'err': {'code': 'no_group_arg_found'}}, 200
    group = request.args['group']
    page_raw = ScrapService.scrap_page(group_name=group)
    if not page_raw:
        return {'success': False, 'err': {'code': 'schedule_loading_error'}}, 200
    try:
        current_day = ParseService.parse_current_day(page_raw)
    except:
        return {'success': False, 'err': {'code': 'schedule_parsing_error'}}, 200
    return json.dumps({'success': True, 'result': current_day}, default=convert_timestamp, ensure_ascii=False), 200

@server.route('/schedule/current/lesson', methods=['GET'])
def get_current_lesson():
    if 'group' not in request.args:
        return {'success': False, 'err': {'code': 'no_group_arg_found'}}, 200
    group = request.args['group']
    page_raw = ScrapService.scrap_page(group_name=group)
    if not page_raw:
        return {'success': False, 'err': {'code': 'schedule_loading_error'}}, 200
    try:
        current_lesson = ParseService.parse_current_lesson(page_raw)
    except:
        return {'success': False, 'err': {'code': 'schedule_parsing_error'}}, 200
    return json.dumps({'success': True, 'result': current_lesson}, default=convert_timestamp, ensure_ascii=False), 200

@server.route('/schedule/lesson/names', methods=['GET'])
def get_lesson_names():
    if 'group' not in request.args:
        return {'success': False, 'err': {'code': 'no_group_arg_found'}}, 200
    group = request.args['group']
    page_raw = ScrapService.scrap_page(group_name=group)
    if not page_raw:
        return {'success': False, 'err': {'code': 'schedule_loading_error'}}, 200
    try:
        schedule = ParseService.parse_schedule(page_raw)
        lesson_names = set()
        for week in schedule:
            for day in week['days']:
                for lesson in day['lessons']:
                    lesson_names.add(lesson['name'])
    except:
        return {'success': False, 'err': {'code': 'schedule_parsing_error'}}, 200
    return json.dumps({'success': True, 'result': list(lesson_names)}, default=convert_timestamp, ensure_ascii=False), 200

server.run(host='0.0.0.0', port=os.getenv('PORT', 8080))    
