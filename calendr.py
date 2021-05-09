import calendar
import datetime
import json

class Calendr:
    def __init__(self):
        self.weekdays = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]

    def now(self):
        return datetime.datetime.now()

    def to_weekday(self, date, forwards = False):
        return self.get_day_of_week(date.year, date.month, date.day, forwards)

    def get_day_of_week(self, year, month, day, forwards = False):
        temp_date = datetime.date(year, month, day)
        temp_date_weekday = temp_date.strftime('%A')
        next_month = month + 1
        _day = day

        if temp_date_weekday == 'Sunday':
            if forwards:
                _day += 1
            else:
                _day -= 2

        elif temp_date_weekday == 'Saturday':
            if forwards:
                _day += 2
            else:
                _day -= 1

        _month = month
        _year = year

        days_in_month = calendar.monthrange(year, next_month)[1]

        if _day > days_in_month:
            _day -= days_in_month
            _month += 1

            if _month > 12:
                _month -= 12
                _year += 1

        elif _day < 1:
            _month -= 1

            if _month < 1:
                _month += 12
                _year -= 1

            days_in_month_previous = calendar.monthrange(_year, _month)[1]
            _day += days_in_month_previous

        return datetime.datetime(_year, _month, _day)

    def get_weekdays(self):
        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]

        business_days = 0

        for i in range(1, days_in_month):
            try:
                thisdate = datetime.date(now.year, now.month, i)
            except(ValueError):
                break
            if thisdate.weekday() < 5 and not self.is_holiday(thisdate): # Monday == 0, Sunday == 6
                business_days += 1

        return business_days

    def get_hours_diff(self, time1, time2):
        time1 = datetime.datetime.strptime(time1,"%H:%M")
        time2 = datetime.datetime.strptime(time2,"%H:%M")
        diff = time2 - time1
        return diff.total_seconds()/3600

    def is_holiday(self, datetime_obj):
        f = open('./data/calendar/holidays.json', "r")
        data = json.loads(f.read())['data']

        current_day = datetime_obj.strftime('%d')
        current_month = datetime_obj.strftime('%m')
        current_year = datetime_obj.strftime('%Y')

        holidays = []

        for d in data:
            holiday_month = int(d['date']['month'])
            holiday_year = int(current_year)

            if d['type'] == 'date':
                holiday_day = int(d['date']['day'])

            elif d['type'] == 'nth-day':
                day_count = 0
                weekday_count = 0
                n = d['date']['n']

                if n == 'last':
                    days_in_month = calendar.monthrange(holiday_year, holiday_month)[1]
                    weekday_count = days_in_month

                    while day_count < 1:
                        temp_date = datetime.date(holiday_year, holiday_month, weekday_count)
                        weekday_count -= 1

                        if temp_date.strftime('%A') == d['date']['day']:
                            day_count += 1
                            weekday_count += 1

                else:
                    n = int(n)
                    while day_count < n:
                        weekday_count += 1
                        temp_date = datetime.date(holiday_year, holiday_month, weekday_count)

                        if temp_date.strftime('%A') == d['date']['day']:
                            day_count += 1


                holiday_day = weekday_count

            temp_date = datetime.date(holiday_year, holiday_month, holiday_day)
            temp_date_weekday = temp_date.strftime('%A')

            if temp_date_weekday == 'Sunday':
                holiday_day += 1
            elif temp_date_weekday == 'Saturday':
                holiday_day -= 1

            day = "{:02d}/{:02d}/{:4d}".format(holiday_month, holiday_day, holiday_year)

            holidays.append(day)

        # for holiday in holidays:
        #     print(f"{holiday['holiday']}:\n\t{holiday['day']}\n")
        current_date = "{:02d}/{:02d}/{:4d}".format(int(current_month), int(current_day), int(current_year))

        return current_date in holidays

calendr = Calendr()
