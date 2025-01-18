#!/bin/python3
from argparse import ArgumentParser
from collections import namedtuple
import re

from course_to_name import course_initials_to_index, course_index_to_name
from strats_list import strats_list

ParsedLine = namedtuple('ParsedLine', 'function operator value')

class TaskConstraints:
    def __init__(self):
        self.course = ''
        self.start = []
        self.end = []
        self.require = []
        self.ban = ['leave_course', 'use_warp', 'goto_pu']
        self.block_labels = ['course:', 'start:', 'end:', 'require:', 'ban:', 'allow:']

def throw_error(type: str, error: str, line_num: int, optional_message: str = None) -> Exception:
    type_str = 'Syntax Error' if type == 'syn' else 'Error'
    print(f'{type_str}: {error}{(" on line " + str(line_num)) if line_num else ""}')
    if optional_message: print(f'       {optional_message}')
    return Exception

def find_operator_in_line(line: str, line_num: int) -> str|None|Exception:
    operator_search = re.match(r'([^<>=!]*)?((?P<operator>[<>=!]=?)|(?P<unsupported_operator>[^A-Za-z0-9_"\s]+))\s*', line)
    if operator_search:
        if operator_search.group('operator'):
            operator = operator_search.group('operator')
            unsupported_operator = False
        else:
            operator = operator_search.group('unsupported_operator')
            unsupported_operator = True

        if unsupported_operator:
            return throw_error('', f'unsupported operator "{operator}"', line_num)
    else:
        return None

    return operator

def check_known_course(course_name: str, line_num: int) -> bool|Exception:
    # Find the course by initials, full name, or stage index
    if course_name not in course_initials_to_index.keys()                              \
       and course_name not in [name.lower() for name in course_index_to_name.values()] \
       and course_name not in course_initials_to_index.values():
        return throw_error('', f'unknown course "{course_name}"', line_num)
    return True

def escape(text: str) -> str:
    return text.replace("'", "\\'")

def parse_block_line(tc: TaskConstraints, current_block: str, line: str, line_num: int):
    # Make sure every quote has a match
    if line.count('"') % 2 != 0:
        return throw_error('syn', 'unterminated string', line_num)

    if current_block == 'course':
        tc.course = line.lower()
        if check_known_course(tc.course, line_num) == Exception:
            return Exception

    elif current_block != 'ban' and current_block != 'allow':
        operator = find_operator_in_line(line, line_num)
        # If there is no operator in a line,
        # assume the condition to be '= true'
        if not operator:
            line = f'{line} = true'
            operator = '='
        elif operator == Exception:
            return Exception

        # Separate line at the operator
        line = [elem.strip() for elem in line.split(operator)]
        # Convert single equality sign to double
        operator = '==' if operator == '=' else operator
        # 'action_count' calls take a parameter,
        # so we need to format them properly
        if 'action_count' in line[0].lower():
            action_count_split = line[0].lower().split(' ', 1)
            # 'PLACEHOLDER' will become 'true' or 'false'
            # when the conditional Lua statements are generated
            # (see: generate_<start/end>_condition_statement)
            action_count_call = f'{action_count_split[0]}({action_count_split[1]}, PLACEHOLDER)'
            line[0] = action_count_call
        # Add the parsed line to the current block
        # (escaping `line[1]` because it might have an apostrophe in it)
        exec(f"tc.{current_block}.append(ParsedLine('{line[0]}', '{operator}', '{escape(line[1])}'))")
    # Handle ban and allow blocks
    else:
        line = line.lower()
        if line.strip('"') not in strats_list:
            return throw_error('', f'unknown strategy / action "{line.strip()}"', line_num, 
                               'If this is a function, consider putting it in a "require" section')
        if current_block == 'allow':
            tc.ban.remove(line)
        else:
            tc.ban.append(line)

# Implement these functions to provide suggestions
# to help with spelling errors

def try_match_block_label(unknown_block_label: str) -> str:
    ...

def try_match_action_name(unknown_action: str) -> str:
    ...

def parse_file(path: str) -> TaskConstraints|Exception:
    with open(path, 'r', encoding='utf-8') as file:
        tc = TaskConstraints()
        current_block = ''
        line_num = 0
        for line in file:
            line_num += 1
            # Ignore comments
            line = line.strip().split('//')[0]
            # Ignore newlines
            if not line:
                continue
            line_lower = line.lower()
            # This can be a one-line block label, so handle it separately
            if 'course' in line_lower and 'leave_course' not in line_lower:
                if ':' not in line_lower:
                    return throw_error('syn', 'missing ":"', line_num)
                tc.course = line_lower.split(':')[1].strip()
                # If there is no course name in this line,
                # we'll find it somewhere in the block
                if not tc.course:
                    current_block = 'course'
                elif check_known_course(tc.course, line_num) == Exception:
                    return Exception
                continue
            # Update current_block if we enter a new one
            if line_lower in tc.block_labels:
                if ':' not in line_lower:
                    return throw_error('syn', 'missing ":"', line_num)
                current_block = line_lower.strip(':')
                continue
            elif ':' in line:
                return throw_error('', f'unknown section name "{line.split(":")[0]}"', line_num, try_match_block_label(line.split(":")))
            # Parse the current statement
            if parse_block_line(tc, current_block, line, line_num) == Exception:
                return Exception

    if not tc.course or not tc.start or not tc.end:
        if not tc.course:
            return throw_error('', 'missing required section "course"', 0)
        if not tc.start:
            return throw_error('', 'missing required section "start"', 0)
        if not tc.end:
            return throw_error('', 'missing required section "end"', 0)

    return tc

def generate_strat_function_call(strat: str) -> str:
    match strat:
        case 'blj':
            return 'DQonBLJ()'
        case 'c_up_slide':
            return 'DQonCUpSlide()'
        case 'use_warp':
            return 'DQonUseWarp()'
        case 'use_shell':
            return 'DQonUseShell()'
        case 'use_cannon':
            return 'DQonUseCannon()'
        case 'leave_course':
            return 'DQonExitCourse()'
        case 'goto_pu':
            return 'DQonGotoPU()'
        case 'downwarp':
            return 'DQonDownwarp()'
        case _:
            return f'DQonAction({strat}, "")'

def generate_dq_statement(statement: ParsedLine, update_previous_action: str) -> str:
    # TODO:
    # - handle proper conjugation for each action
    # - generate more natural-sounding english where possible (based on the statement operator?)
    if 'action_count' in statement.function:
        action = statement.function.split('"')[1]
        return f'DQ("Performed action \\"{action}\\" " .. {statement.function.replace("PLACEHOLDER", update_previous_action)} .. "/{statement.value} times")'
    match statement.function:
        case 'coin_count':
            return f'DQ("Only collected " .. coin_count() .. "/{statement.value} coins")'
        case 'red_coin_count':
            return f'DQ("Only collected " .. red_coin_count() .. "/{statement.value} red coins")'
        case 'life_count':
            return f'DQ("Only collected " .. life_count() .. "/{statement.value} 1-ups")'
        case 'a_press_count':
            return f'DQ("Pressed A " .. a_press_count() .. "/{statement.value} times")'
        case 'yellow_box_broken_count':
            return f'DQ("Broke " .. yellow_box_broken_count() .. "/{statement.value} yellow boxes")'
        case 'wing_box_broken_count':
            return f'DQ("Broke " .. wing_box_broken_count() .. "/{statement.value} wing cap boxes")'
        case 'metal_box_broken_count':
            return f'DQ("Broke " .. metal_box_broken_count() .. "/{statement.value} metal cap boxes")'
        case 'vanish_box_broken_count':
            return f'DQ("Broke " .. vanish_box_broken_count() .. "/{statement.value} vanish cap boxes")'
        # For custom functions, the user is expected to handle
        # DQs themselves, so we won't call DQ for them
        case _:
            return ''

def generate_start_condition_statement(statements: list[ParsedLine]):
    statement_one = statements[0]
    end_str = f'    if {statement_one.function}() {statement_one.operator} {statement_one.value}'
    if len(statements) > 1:
        for statement in statements[1:]:
            end_str += f' and {statement.function}() {statement.operator} {statement.value}'
    end_str += ' then return true end'
    return end_str

def generate_end_condition_statement(statements: list[ParsedLine]) -> str:
    # Last statement in 'end' block is what should actually stop timing
    # e.g. you need 6 red coins and then need to enter the disappear action:
    # you want to be able to DQ properly if you enter the disappear action (which
    # ostensibly is what should actually stop timing) with less than 6 red coins
    last_statement = statements[-1]
    end_str = f'    if {last_statement.function}() {last_statement.operator} {last_statement.value} then\n'
    if len(list(statements)) > 1:
        update_previous_action = ''
        for i, statement in enumerate(statements[:-1]):
            # For action_count calls, only update previous action on the last
            # call (because there can be multiple action_count checks in one frame)
            update_previous_action = 'true' if i == len(statements) - 1 else 'false'
            end_str += f'        if not ({statement.function.replace("PLACEHOLDER", update_previous_action)}{"()" if "action_count" not in statement.function else ""} {statement.operator} {statement.value}) then\n'
            dq_statement = generate_dq_statement(statement, update_previous_action)
            if dq_statement:
                end_str += f'            {dq_statement}\n'
            end_str += '''            return false
        end
'''
    end_str += f'''        return true
    end'''
    return end_str

def generate_requirements_function(statements: list[ParsedLine]) -> str:
    end_str = ''
    update_previous_action = ''
    for i, statement in enumerate(statements):
        # For action_count calls, only update previous action on the last
        # call (because there can be multiple action_count checks in one frame)
        update_previous_action = 'true' if i == len(statements) - 1 else 'false'
        end_str += f'    if not ({statement.function.replace("PLACEHOLDER", update_previous_action)}{"()" if "action_count" not in statement.function else ""} {statement.operator} {statement.value}) then'
        dq_statement = generate_dq_statement(statement, update_previous_action)
        if dq_statement:
            end_str += f'        {dq_statement}\n'
        end_str += '''
        return false
    end
'''
    return end_str

def generate_conditions_lua(tc: TaskConstraints, path: str, custom_functions: str):
    with open(path, 'w+', encoding='utf-8') as file:
        # Course specified by initials
        if not ' ' in tc.course:
            course_index = course_initials_to_index[tc.course]
        # Course specified by stage index
        elif tc.course.isdigit():
            course_index = tc.course
        # Course specified by full name
        else:
            # Get dict key by value
            course_index_to_name_lower = {item[0]: item[1].lower() for item in course_index_to_name.items()}
            course_index = list(filter(lambda x: course_index_to_name_lower[x] == tc.course, course_index_to_name_lower))[0]

        course_name = course_index_to_name[course_index]

        file_str = f"""-- Auto-generated by tcl.py --
dofile(PATH .. 'DefaultFunctions.lua')
dofile(PATH .. 'DefaultGameInfo.lua')
dofile(PATH .. 'DQFunctions.lua')
"""
        if custom_functions:
            file_str += f"""
-- Custom Functions --
{custom_functions}
--/
"""
        file_str += f"""
COURSE_NUMBER = {course_index} -- {course_name}

function Conditions.startCondition()
"""
        file_str += generate_start_condition_statement(tc.start)
        file_str += f"""
    return false
end

function Conditions.endCondition()
    if {'not require()' if tc.require else 'false'}"""
        for strat in tc.ban:
            file_str += f' or {generate_strat_function_call(strat)}'
        file_str += f''' then return false end
'''
        file_str += generate_end_condition_statement(tc.end)
        file_str += f"""
    return false
end"""
        if tc.require:
            file_str += f"""

function require()
{generate_requirements_function(tc.require)}    return true
end
--/"""
        file.write(file_str)

def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('src', nargs=1, help='TASCompLang source file')
    arg_parser.add_argument('-cf', nargs='?', const='CustomFunctions.lua', help='use custom functions (provide a path to override the default, which is "CustomFunctions.lua")')
    arg_parser.add_argument('-o', nargs=1, default='Conditions.lua', help='path to output file')
    args = arg_parser.parse_args()

    tc: TaskConstraints = parse_file(args.src[0])

    custom_functions_str = ''
    if args.cf:
        print(f'Copying custom functions from "{args.cf}"')
        with open(args.cf, encoding='utf-8') as file:
            custom_functions_str = file.read()
    if tc != Exception:
        generate_conditions_lua(tc, args.o, custom_functions_str)
        print(f'Output to {"Conditions.lua"}')
main()
