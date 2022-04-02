# Models
## Teacher
```
{
    "name": "teacher_name",
    "link": "teacher_link"
}
```

## Lesson
```
{
    "time": {
        "from_time": "08:00",
        "to_time": "09:30"
    },
    "is_lection": false,
    "name": "lesson_name",
    "teachers": [
        ...
    ],
    "audiences": [
        "audiences_name"
    ],
    "number": 1
}
```
* `teachers` is list of [teachers](#teacher).
* The list of teachers and audiences may be empty.

## Day
```
{
    "date": "2022-01-01",
    "lessons": [
        ...
    ]
}
```
* `lessons` is list of [lessons](#lesson).
* The list of lessons may be empty.

## Week
```
{
    "name": "week_name",
    "days": [
        ...
    ]
}
```
* `days` is list of [days](#day).
