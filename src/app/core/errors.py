from enum import Enum


class Error(str, Enum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNICORN_EXCEPTION = "UNICORN_EXCEPTION"
    HTTP_EXCEPTION = "HTTP_EXCEPTION"

    @property
    def details(self):
        return ERROR_DETAILS[self]


ERROR_DETAILS = {
    Error.VALIDATION_ERROR: {
        "code": "VALIDATION_ERROR",
        "message": "Validation error",
    },
    Error.UNICORN_EXCEPTION: {
        "code": "UNICORN_EXCEPTION",
        "message": "Unicorn exception",
    },
    Error.HTTP_EXCEPTION: {
        "code": "HTTP_EXCEPTION",
        "message": "HTTP exception",
    },
}
