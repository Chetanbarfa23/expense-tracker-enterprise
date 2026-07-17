# ==========================================
# SUCCESS RESPONSE
# ==========================================

def success_response(message, data=None):

    response = {
        "success": True,
        "message": message
    }

    if data is not None:

        response["data"] = data

    return response


# ==========================================
# ERROR RESPONSE
# ==========================================

def error_response(message):

    return {
        "success": False,
        "message": message
    }