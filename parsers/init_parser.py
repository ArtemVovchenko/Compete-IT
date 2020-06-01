from parsers.competition import Competition
from parsers import parser_module
from parsers import parser_support_module

competitions = parser_support_module.parse() + parser_module.parse()

