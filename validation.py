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


eir_code_pattern = "(?:^[AC-FHKNPRTV-Y][0-9]{2}|D6W)[ -]?[0-9AC-FHKNPRTV-Y]{4}$"