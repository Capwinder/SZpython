# -*- coding: utf-8 -*-
import os
import datetime
import json


def generate_schedule(name_list, start_date, end_date, count=0):
    date = start_date
    schedule_list = []
    day_count = 0
    while date < end_date:
        index = count % len(name_list)
        date_str = date.strftime('%Y年%m月%d日')
        name = name_list[index]
        line = date_str + ' ' + name
        schedule_list.append(line)
        day_count += 1
        count += 1
        date = start_date + datetime.timedelta(days=day_count)
    return schedule_list, count


def loading_info(name_and_start_date_file=None):
    if os.path.exists(name_and_start_date_file):
        with open(name_and_start_date_file, 'r') as file:
            info_list = [line.strip() for line in file.readlines()]
        name_list = info_list[1:]
        start_date_list = list(map(int, info_list[0].split(' ')))
    else:
        name_list = input('请输入职员姓名，用空格隔开：').strip().split(' ')
        start_date_list = list(map(int, input('请输入排班起始日期（格式：xxxx-xx-xx）：').split('-')))
        with open(name_and_start_date_file, 'w') as file:
            for num in start_date_list:
                file.write(f'{num} ')
            file.write('\n')
            for name in name_list:
                file.write(f'{name}\n')
    return name_list, start_date_list


def straight_start():
    name_and_start_date_file = 'info_config/name_and_start_date_file.txt'
    name_list, start_date_list = loading_info(name_and_start_date_file)

    start_date = datetime.date(*start_date_list)
    year = start_date_list[0] if start_date_list[1] < 12 else start_date_list[0] + 1
    month = start_date_list[1] + 1 if start_date_list[1] < 12 else 1
    day = 1
    end_date_list = [year, month, day]
    end_date = datetime.date(*end_date_list)

    schedule_list, count = generate_schedule(name_list, start_date, end_date)
    with open('info_config/count_file.txt', 'w') as file:
        file.write(str(count))

    schedule_dict = {}
    for date_name in schedule_list:
        date, name = date_name.split(' ')
        schedule_dict[date] = name
    return schedule_dict


def next_month_schedule():
    if os.path.exists('info_config/count_file.txt'):
        with open('info_config/count_file.txt', 'r') as file:
            count = int(file.readline())
    else:
        print('请先生成起始月排班表')
        return

    name_and_start_date_file = 'info_config/name_and_start_date_file.txt'
    name_list, start_date_list = loading_info(name_and_start_date_file)

    year = start_date_list[0] if start_date_list[1] < 12 else start_date_list[0] + 1
    month = start_date_list[1] + 1 if start_date_list[1] < 12 else 1
    day = 1
    start_date_list = [year, month, day]
    start_date = datetime.date(*start_date_list)

    year = start_date_list[0] if start_date_list[1] < 12 else start_date_list[0] + 1
    month = start_date_list[1] + 1 if start_date_list[1] < 12 else 1
    day = 1
    end_date_list = [year, month, day]
    end_date = datetime.date(*end_date_list)
    schedule_list, count = generate_schedule(name_list, start_date, end_date, count)

    with open(name_and_start_date_file, 'r') as file:
        lines = file.readlines()

    lines[0] = f'{start_date_list[0]} {start_date_list[1]} {start_date_list[2]} \n'
    with open(name_and_start_date_file, 'w') as file:
        file.writelines(lines)

    with open('info_config/count_file.txt', 'w') as file:
        file.write(str(count))

    if os.path.exists('info_config/add_workers_file.txt'):
        with open('info_config/add_workers_file.txt', 'r') as file:
            info_list = [line.strip() for line in file.readlines()]
        workers_name_list = info_list[1:]
        hire_date_list = list(map(int, info_list[0].strip().split(' ')))
        hire_date = datetime.date(*hire_date_list)
        if hire_date.month > datetime.date(*start_date_list).month:
            pass
        else:
            schedule_list = add_workers_schedule(workers_name_list, hire_date)
            os.remove('info_config/add_workers_file.txt')
    if os.path.exists('info_config/del_workers_file.txt'):
        with open('info_config/del_workers_file.txt', 'r') as file:
            info_list = [line.strip() for line in file.readlines()]
        workers_name_list = info_list[1:]
        resignation_date_list = list(map(int, info_list[0].strip().split(' ')))
        resignation_date = datetime.date(*resignation_date_list)
        if resignation_date.month > datetime.date(*start_date_list).month:
            pass
        else:
            schedule_list = del_workers_schedule(workers_name_list, resignation_date)
            os.remove('info_config/del_workers_file.txt')

    schedule_dict = {}
    for date_name in schedule_list:
        date, name = date_name.split(' ')
        schedule_dict[date] = name
    return schedule_dict


def add_workers_schedule(workers_name_list, hire_date):
    name_and_start_date_file = 'info_config/name_and_start_date_file.txt'
    name_list, start_date_list = loading_info(name_and_start_date_file)
    start_date = datetime.date(*start_date_list)

    if hire_date.month > start_date.month:
        hire_date_list = hire_date.strftime('%Y-%m-%d').split('-')
        with open('info_config/add_workers_file.txt', 'w') as file:
            file.write(f'{hire_date_list[0]} {hire_date_list[1]} {hire_date_list[2]} \n')
            for name in workers_name_list:
                file.write(f'{name}\n')
        print('添加成功！')

    elif hire_date.month < start_date.month:
        print('无法添加过去的时间作为入职时间')
        raise ValueError("can't add past time")

    else:
        year = start_date_list[0] if start_date_list[1] < 12 else start_date_list[0] + 1
        month = start_date_list[1] + 1 if start_date_list[1] < 12 else 1
        day = 1
        end_date_list = [year, month, day]
        end_date = datetime.date(*end_date_list)
        delta_count = (end_date - start_date).days

        if os.path.exists('info_config/count_file.txt'):
            with open('info_config/count_file.txt', 'r') as file:
                count = int(file.readline())
        else:
            print('请先生成起始月排班表')
            raise ValueError("'count' has not been defined")
        count -= delta_count
        front_schedule_list, count = generate_schedule(name_list, start_date, hire_date, count)

        added_name_list = name_list + workers_name_list
        count = count + (count // len(name_list)) * (len(added_name_list) - len(name_list))
        latter_schedule_list, count = generate_schedule(added_name_list, hire_date, end_date, count)
        schedule_list = front_schedule_list + latter_schedule_list
        print('添加成功！')

        with open('info_config/count_file.txt', 'w') as file:
            file.write(str(count))

        with open('info_config/name_and_start_date_file.txt', 'a') as file:
            for name in workers_name_list:
                file.write(f'{name}\n')

        schedule_dict = {}
        for date_name in schedule_list:
            date, name = date_name.split(' ')
            schedule_dict[date] = name
        return schedule_dict


def del_workers_schedule(workers_name_list, resignation_date):
    name_and_start_date_file = 'info_config/name_and_start_date_file.txt'
    name_list, start_date_list = loading_info(name_and_start_date_file)
    start_date = datetime.date(*start_date_list)

    if resignation_date.month > start_date.month:
        resignation_date_list = resignation_date.strftime('%Y-%m-%d').split('-')
        with open('info_config/del_workers_file.txt', 'w') as file:
            file.write(f'{resignation_date_list[0]} {resignation_date_list[1]} {resignation_date_list[2]} \n')
            for name in workers_name_list:
                file.write(f'{name}\n')
        print('已添加日志，将在指定日期删除！')

    elif resignation_date.month < start_date.month:
        print('无法添加过去的时间作为离职时间')
        raise ValueError("can't add past time")

    else:
        year = start_date_list[0] if start_date_list[1] < 12 else start_date_list[0] + 1
        month = start_date_list[1] + 1 if start_date_list[1] < 12 else 1
        day = 1
        end_date_list = [year, month, day]
        end_date = datetime.date(*end_date_list)
        delta_count = (end_date - start_date).days

        if os.path.exists('info_config/count_file.txt'):
            with open('info_config/count_file.txt', 'r') as file:
                count = int(file.readline())
        else:
            print('请先生成起始月排班表')
            raise ValueError("'count' has not been defined")
        count -= delta_count
        front_schedule_list, count = generate_schedule(name_list, start_date, resignation_date, count)

        index = count % len(name_list)
        off_duty_list = name_list[index:]
        for name in workers_name_list:
            if name in off_duty_list:
                off_duty_list.remove(name)
            if name in name_list:
                name_list.remove(name)
        num = len(off_duty_list)
        special_date = resignation_date + datetime.timedelta(days=num)
        middle_schedule_list, new_count = generate_schedule(off_duty_list, resignation_date, special_date)
        count += new_count

        latter_schedule, new_count = generate_schedule(name_list, special_date, end_date)
        count += new_count + 1
        schedule_list = front_schedule_list + middle_schedule_list + latter_schedule
        print('删除成功！')

        with open('info_config/count_file.txt', 'w') as file:
            file.write(str(count))

        with open('info_config/name_and_start_date_file.txt', 'w') as file:
            file.write(f'{start_date_list[0]} {start_date_list[1]} {start_date_list[2]} \n')
            for name in name_list:
                file.write(f'{name}\n')

        schedule_dict = {}
        for date_name in schedule_list:
            date, name = date_name.split(' ')
            schedule_dict[date] = name
        return schedule_dict


def main():
    if not (os.path.exists('info_config/count_file.txt') and
            os.path.exists('info_config/name_and_start_date_file.txt')):
        opt = '0'
    else:
        print('输入1生成下个月的排班表，输入2添加职员，输入3删除职员，输入4初始化所有信息')
        opt = input('请选择您的操作：')

    schedule_dic = {}
    if opt == '0':
        schedule_dic = straight_start()

    elif opt == '1':
        schedule_dic = next_month_schedule()

    elif opt == '2':
        workers_list = input('请输入要添加的职员姓名，用空格隔开：').strip().split(' ')
        hire_date = datetime.date(*list(map(int, input('请输入入职日期（格式：xxxx-xx-xx）：').strip().split('-'))))
        schedule_dic = add_workers_schedule(workers_list, hire_date)
        print('添加成功！')

    elif opt == '3':
        workers_list = input('请输入要删除的职员姓名，用空格隔开：').strip().split(' ')
        resignation_date = datetime.date(*list(map(int, input('请输入离职日期（格式：xxxx-xx-xx）：').strip().split('-'))))
        schedule_dic = del_workers_schedule(workers_list, resignation_date)
        print('删除成功！')

    elif opt == '4':
        os.remove('info_config/count_file.txt')
        os.remove('info_config/name_and_start_date_file.txt')
        print('初始化成功！')

    else:
        print('请选择正确的操作！')
    return schedule_dic


if __name__ == '__main__':
    schedule = main()
    with open('info_config/name_and_start_date_file.txt', 'r') as fi:
        m = fi.readline().strip().split(' ')[1]
    with open(f'schedule of month {m}.json', 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)
