from parsers import parser_module
from parsers import parser_support_module


competitions = parser_support_module.parse() + parser_module.parse()
with open('parsed_rocket.txt','w') as outfile:
    for competition_data in competitions:
        outfile.write(str(competition_data))

