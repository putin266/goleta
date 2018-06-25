from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.status_code == 400:
            return_msg = ''
            return_data = {}
            for key, value in response.data.items():
                for msg in value:
                    return_msg = return_msg + msg
            return_data['error_msg'] = return_msg
            return_data['status_code'] = response.status_code
            response.data = return_data
            response.status_code = 200

    return response