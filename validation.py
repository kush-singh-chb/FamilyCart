import re

from flask_restful import reqparse


def register_validate():
    parser_register = reqparse.RequestParser()
    parser_register.add_argument('email', help='This field cannot be blank', required=True)
    parser_register.add_argument('first_name', help='This field cannot be blank', required=True)
    parser_register.add_argument('last_name', help='This field cannot be blank', required=True)
    parser_register.add_argument('eir_code', help='This field cannot be blank', required=True)
    parser_register.add_argument('password', help='This field cannot be blank', required=True)
    return parser_register


def login_validate():
    parser_register = reqparse.RequestParser()
    parser_register.add_argument('username', help='This field cannot be blank', required=True)
    parser_register.add_argument('password', help='This field cannot be blank', required=True)
    return parser_register


def check_service_validate():
    parser_register = reqparse.RequestParser()
    parser_register.add_argument('eircode', help='This field cannot be blank', required=True)
    return parser_register


def validate_email(email) -> bool:
    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return bool(pattern.match(email))


def validate_eir(code) -> bool:
    eir_code_pattern = re.compile("(?:^[AC-FHKNPRTV-Y][0-9]{2}|D6W)[ -]?[0-9AC-FHKNPRTV-Y]{4}$")
    return bool(eir_code_pattern.match(code))


def category_create_validate():
    parser_register = reqparse.RequestParser()
    parser_register.add_argument('name', help='This field cannot be blank', required=True)
    return parser_register
