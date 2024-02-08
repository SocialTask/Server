from flask import Flask, request, jsonify, g, send_from_directory

# Utility function to generate error responses with a message and status code
def error_response(message, status_code):
    response = jsonify({'error': message})
    response.status_code = status_code
    return response