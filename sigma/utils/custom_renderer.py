from rest_framework import status
from rest_framework.renderers import JSONRenderer


class CustomJsonResponse(JSONRenderer):

    def modify_error_response(self, data, status_code):
        """Modify error response"""
        error_detail, error_message = self._modify_error_response(data)

        modified_data = {"error": error_detail, "statusCode": status_code, "message": error_message}
        return modified_data

    def modify_success_response(self, data, status_code):
        """Modify success response"""

        return data

    def _modify_error_response(self, data):
        """Deep formatting of error response"""

        if data["errors"][0]["code"] == "required":
            error_detail = "missing required field"
            error_message = f"{data['errors'][0]['attr']} is required"

        if data["errors"][0]["code"] != "required":
            error_detail = data["errors"][0]["code"]
            error_message = data["errors"][0]["detail"]

        return error_detail, error_message

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Modify API response format"""

        response = renderer_context["response"]

        if status.is_client_error(response.status_code) or status.is_server_error(
            response.status_code
        ):
            modified_data = self.modify_error_response(response.data, response.status_code)

        else:
            modified_data = self.modify_success_response(response.data, response.status_code)

        return super().render(modified_data, accepted_media_type, renderer_context)
