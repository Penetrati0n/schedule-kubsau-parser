# General Info

## General API Information
* The base url is: `http://schedule-kubsau.herokuapp.com/`
* The base successful response is: 
```
{
  "success": true,
  "result": {
      ...
  }
}
```

## Error Codes and Messages
* If there is an error, the API will return an error with a message of the reason.

*The error payload on API is as follows:*
```
{
  "success": false,
  "err": {
      "code": "error_code"
  }
}
```
* Specific error codes and messages defined in [Error Codes](./error_codes.md).

## General Information on Endpoints
* For GET endpoints, parameters must be sent as a query string.


# Schedule Endpoints
## Schedule
Get a schedule (list of 2 [weeks](./models.md#week)).
```
GET /schedule
```
Parameters:
| Name         | Type      | Required   |
|--------------|-----------|------------|
| group        | STRING    | YES        |

## Current Day
Get the schedule for the current [day](./models.md#day).
```
GET /schedule/current/day
```
Parameters:
| Name         | Type      | Required   |
|--------------|-----------|------------|
| group        | STRING    | YES        |

## Current Lesson
Get the current [lesson](./models.md#lesson).
```
/schedule/current/lesson
```
Parameters:
| Name         | Type      | Required   |
|--------------|-----------|------------|
| group        | STRING    | YES        |

## List of Lessons
Get a list of all lesson names.
```
GET /schedule/lesson/names
```
Parameters:
| Name         | Type      | Required   |
|--------------|-----------|------------|
| group        | STRING    | YES        |

