import re

from datetime import datetime, time, timedelta
from bs4 import BeautifulSoup, Tag

class ParseService():
    LESSON_TIME_PATTERN = r'(?P<from_hour>[0-9]{2}):(?P<from_minute>[0-9]{2})(?P<to_hour>[0-9]{2}):(?P<to_minute>[0-9]{2})'
    LESSON_AUDIENCE_PATTERN = r'(?P<audience>[0-9]+[а-яА-ЯёЁ]+)'
    DAY_DATE_PATTERN = r'day\-(?P<year>[0-9]+)\-(?P<month>[0-9]+)\-(?P<day>[0-9]+)'
    WEEKS_ID = ['#first', '#second']
    
    def __parse_lesson(lesson_element: Tag) -> dict:
        #----------------------------------------------------------------------------------------------------
        # region Parse lesson time
        lesson_time_raw = lesson_element.select_one('.time').text
        lesson_time_match = re.search(ParseService.LESSON_TIME_PATTERN, lesson_time_raw)
        if lesson_time_match:
            lesson_time = {
                'from_time': time(int(lesson_time_match.group('from_hour')), int(lesson_time_match.group('from_minute'))),
                'to_time': time(int(lesson_time_match.group('to_hour')), int(lesson_time_match.group('to_minute'))),
            }
        else:
            lesson_time = None
        # endregion
        #----------------------------------------------------------------------------------------------------
        # region Parse type of lesson
        lesson_lection_element = lesson_element.select_one('.lection')
        is_lection = 'yes' in lesson_lection_element.attrs['class']
        # endregion
        #----------------------------------------------------------------------------------------------------
        # region Parse lesson name
        lesson_name_element = lesson_element.select_one('.diss')
        lesson_name_split_elemets = [i.strip() for i in lesson_name_element.text.split('\n') if i.strip() != '']
        if not lesson_name_split_elemets:
            return None
        lesson_name = lesson_name_split_elemets[0]
        # endregion
        #----------------------------------------------------------------------------------------------------
        # region Parse teachers
        teachers = []
        teacher_elemets = lesson_element.select('a')
        for te in teacher_elemets:
            teachers.append({'name': te.text, 'link': te.attrs['href']})
        # endregion
        #----------------------------------------------------------------------------------------------------
        # region Parse audiences
        audiences_element = lesson_element.select_one('.who-where')
        audiences_matches = re.findall(ParseService.LESSON_AUDIENCE_PATTERN, audiences_element.text)
        audiences = [m for m in audiences_matches]
        # endregion
        return {
            'time': lesson_time,
            'is_lection': is_lection,
            'name': lesson_name,
            'teachers': teachers,
            'audiences': audiences,
        }

    def __parse_day(day_element: Tag) -> dict:
        #----------------------------------------------------------------------------------------------------
        # region Parse date
        attrs = day_element.attrs['class']
        day_date_raw = next((item for item in attrs if re.search(ParseService.DAY_DATE_PATTERN, item)), None)
        if day_date_raw:
            day_date_match = re.search(ParseService.DAY_DATE_PATTERN, day_date_raw)
            day_date = datetime(
                year=int(day_date_match.group('year')),
                month=int(day_date_match.group('month')),
                day=int(day_date_match.group('day')),
            )
        else:
            day_date = None
        # endregion
        #----------------------------------------------------------------------------------------------------
        # region Parse lessons
        lessons = []
        lesson_number = 0
        for le in day_element.select('tr'):
            lesson_number += 1
            lesson = ParseService.__parse_lesson(le)
            if not lesson:
                continue
            lesson['number'] = lesson_number
            lessons.append(lesson)
        # endregion
        #----------------------------------------------------------------------------------------------------
        return {
            'date': day_date,
            'lessons': lessons,
        }

    def __parse_week(week_element: Tag) -> dict:
        #----------------------------------------------------------------------------------------------------
        # region Parse week name
        week_name_element = week_element.select_one('h3')
        week_name = week_name_element.text
        # endregion
        #----------------------------------------------------------------------------------------------------
        # region Parse days in week
        days_elements = week_element.select('div.card-block')
        days_info = []
        for de in days_elements:
            day_info = ParseService.__parse_day(de)
            days_info.append(day_info)
        # endregion
        #----------------------------------------------------------------------------------------------------
        return {
            'name': week_name,
            'days': days_info,
        }

    def parse_schedule(html_text: str) -> dict:
        #----------------------------------------------------------------------------------------------------
        # region Parse schedule
        parsed_html = BeautifulSoup(html_text, features="html.parser")
        schedule = []
        for id in ParseService.WEEKS_ID:
            schedule.append(ParseService.__parse_week(parsed_html.select_one(id)))
        # endregion
        #----------------------------------------------------------------------------------------------------
        return schedule

    def parse_current_day(html_text: str) -> dict:
        #----------------------------------------------------------------------------------------------------
        # region Parse current day
        parsed_html = BeautifulSoup(html_text, features="html.parser")
        days_elements = parsed_html.select('.card-block')
        day_info = None
        for de in days_elements:
            if de.select_one('.today'):
                day_info = ParseService.__parse_day(de)
                break
        # endregion
        #----------------------------------------------------------------------------------------------------
        return day_info

    def parse_current_lesson(html_text: str) -> dict:
        #----------------------------------------------------------------------------------------------------
        # region Parse current lesson
        current_day_info = ParseService.parse_current_day(html_text)
        lessons = current_day_info['lessons']
        current_datetime = datetime.utcnow() + timedelta(hours=3)
        current_time = time(current_datetime.hour, current_datetime.minute)
        current_lesson = {}
        for i in range(len(lessons) - 1):
            if i == 0 and current_time < lessons[i]['time']['from_time']:
                current_lesson = lessons[i]
                break
            elif lessons[i]['time']['from_time'] <= current_time < lessons[i + 1]['time']['from_time']:
                current_lesson = lessons[i]
                break
        if not current_lesson and lessons:
            current_lesson = lessons[-1]
        # endregion
        #----------------------------------------------------------------------------------------------------
        return current_lesson
