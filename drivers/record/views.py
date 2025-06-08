from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Profile, Zone, Logo, Todaname, Notifies
from information.models import Addinfo, Seminars, Attendance, Febs_2025, Aprs_2025
from information.models import Jans_2025, Mays_2025, Junes_2025, Julys_2025
from information.models import Augs_2025, Septs_2025, Octs_2025, Novs_2025, Decs_2025


from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .forms import ProfileForm
from .forms import ProfileRegistrationForm

from django.db.models import Q
from itertools import chain
from django.db.models.functions import Trim

from datetime import datetime
import json
from calendar import monthrange
from datetime import date
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import random
import time

global temp_val
temp_val = ''

global sequence_order
sequence_order = []

global dash_one, name_dash
dash_one, name_dash = Profile.objects.all().order_by('zone','last_name'), Profile.objects.get(pk=1)

global dash_count
dash_count = 2

global radio_cat,radio_val
radio_cat ,radio_val = ['normal'], {}

global pick_attends
pick_attends = ''

global dash_one_salary
dash_one_salary = datetime.now().strftime('%m')


def time_update_select(request ,month_day):
    print('ovetime approval select')
    value = month_day.isdigit()
    if value == True:
        request.session['approve_time_days'] = month_day
    else:
        format = '%b'
        no_months = datetime.strptime(month_day, format)
        request.session['approve_time_months'] = no_months.strftime("%m")

    month = request.session.get('approve_time_months')
    if month in [None ,'None', '']:
        month = int(datetime.now().strftime('%m'))

    day = request.session.get('approve_time_days')
    if day in [None ,'None', '']:
        day = int(datetime.now().strftime('%d'))

    month_range = monthrange(2025, int(month))
    if int(day) > int(month_range[1]):
        messages.success(request, ('Invalid Days Select: Out of Month Day'))
        return redirect('time_update')

    date_pick = date(int(2025), int(month), int(day))
    if str(date_pick.strftime("%a")) == 'Sun':
        messages.success(request, ('Invalid Days Select: Sunday'))
        return redirect('time_update')

    request.session['time_updates'] = [month , day]
    return redirect('time_update')
    # return render(request,'overtime_approval_select.html',{})


def time_update_salary(emp_name ,data_months):
    employee_pay = {}

    for emp in emp_name:
        total_5th_hr = 0
        total_5th_ot_hr = 0
        total_5th_salary = 0
        total_5th_ot_salary = 0

        total_20th_hr = 0
        total_20th_ot_hr = 0
        total_20th_salary = 0
        total_20th_ot_salary = 0
        ots = 0
        otss = 0
        count_5th = 0
        count_20th = 0
        for pick in data_months:
            if emp == str(pick.user_attend):
                if int(pick.log_in.strftime('%d')) >= 5 and int(pick.log_in.strftime('%d')) <= 20:
                    if str(pick.log_in.strftime('%a')) != 'Sun':

                        total_5th_hr += float(pick.total_hour)
                        if 'hr' in str(pick.ot_approved_time) or 'hrs' in str(pick.ot_approved_time):
                            ots = float(pick.ot_approved_time.split()[0])
                        elif str(pick.ot_approved_time) in ['None', None, '']:
                            ots = 0.0
                        else:
                            ots = float(pick.ot_approved_time)

                        # print('ots ',ots)
                        total_5th_ot_hr += ots
                        count_5th += 1
                    else:
                        pass
                        # total_5th_hr += 0
                        # total_5th_ot_hr += 0

                else:
                    if str(pick.log_in.strftime('%a')) != 'Sun':
                        total_20th_hr += pick.total_hour
                        if 'hr' in str(pick.ot_approved_time) or 'hrs' in str(pick.ot_approved_time):
                            otss = float(pick.ot_approved_time.split()[0])

                        elif str(pick.ot_approved_time) in ['None', None, '']:
                            otss = 0.0
                        else:
                            otss = float(pick.ot_approved_time)

                        total_20th_ot_hr += otss
                        count_20th += 1
                    else:
                        pass
                        # total_20th_hr += 0
                        # total_20th_ot_hr += 0

        # print('total 5th hour ', total_5th_hr)
        # print('total 5th ot hour ', total_5th_ot_hr)
        # print('total 20th hour ', total_20th_hr)
        # print('total 20th ot hour ', total_20th_ot_hr)
        total_5th_hours = float(round(float(total_5th_hr) - float(total_5th_ot_hr), 2))

        total_5th_salary = float(round(total_5th_hours * 86.59, 2))
        total_5th_ot_salary = float(total_5th_ot_hr) * 65
        fifth_total_salary = total_5th_salary + total_5th_ot_salary

        total_20th_hours = float(round(float(total_20th_hr) - float(total_20th_ot_hr), 2))

        total_20th_salary = float(round(total_20th_hours * 86.59, 2))
        total_20th_ot_salary = float(total_20th_ot_hr) * 65
        twenty_total_salary = total_20th_salary + total_20th_ot_salary
        # total_salary = float(fifth_total_salary) + float(twenty_total_salary)
        total_salary =  '{:.2f}'.format(fifth_total_salary + twenty_total_salary)

        # temp_5th = (total_5th_hours * 86.59) + (total_5th_ot_hr * 65)
        # temp_20th = (total_20th_hours * 86.59) + (total_20th_ot_hr * 65)
        # temp_total = temp_5th + temp_20th
        # total_salary = '{:,.2f}'.format(temp_total)
        # print('temp total ', temp_total ,total_salary)


        employee_pay[emp] = [count_5th, total_5th_hours, total_5th_ot_hr, fifth_total_salary,
                             count_20th, total_20th_hours, total_20th_ot_hr, twenty_total_salary,
                             total_salary]

    # for key ,value in employee_pay.items():
    #     print('employee pay ',key, value)
    return employee_pay


def time_update(request):
    print('time update')
    if request.user.is_authenticated == False:
        messages.success(request, ('User is not Log-in'))
        return redirect('home')

    day_select = [x for x in range(1, 32)]
    current_dates = request.session.get('time_updates')

    print('current dates ',current_dates)
    if current_dates in ['None', None, '']:
        # request.session['current_dates'] = datetime.now()
        current_dates = datetime.now()
    else:
        current_dates = date(int(2025), int(current_dates[0]), int(current_dates[1]))

    # current_dates = datetime.now()
    current_date = current_dates.strftime('%Y-%m-%d')
    date_now = current_dates.strftime('%A, %B %d, %Y')
    get_month_attend = int(current_dates.strftime('%m'))
    # get_year_attend = int(datetime.now().strftime('%Y'))
    # ot_hour = ['30:00 mins', '01:00 hr', '01:30 hrs', '02:00 hrs', '02:30 hrs', '03:00 hrs']

    # format = '%H:%M'
    # ampm = datetime.strptime('12:00', format)

    # data_months = Aprs_2025.objects.all().order_by('log_in','user_attend')
    check = 'data_months'
    data_months = get_overtime_approval_month_key(get_month_attend, check)
    data_months = data_months.order_by('user_attend' ,'log_in')

    emp_salary = data_months.filter(log_in__date=current_date).order_by('user_attend')
    emp_name = [str(x.user) for x in Profile.objects.all()]
    emp_name.sort()
    print('employee name ',emp_name)
    employee_pay = time_update_salary(emp_name ,data_months)


    if request.method == "POST":
        # get_date = request.POST['dates']
        rec_login = [str(x.log_in.strftime('%H:%M')) for x in emp_salary]
        rec_logout = [str(x.log_out.strftime('%H:%M')) for x in emp_salary]

        login_dict = dict(zip(emp_name, rec_login))
        logout_dict = dict(zip(emp_name, rec_logout))
        # print('record login ',login_dict)
        # print('record logout ',logout_dict)

        get_login = request.POST.getlist('login')
        get_logout = request.POST.getlist('logout')

        print('log in time modified ', get_login)
        print('log out time modified ', get_logout)

        get_login_dict = {}
        get_logout_dict = {}
        for login in range(0 ,len(get_login)):
            if get_login[login] != '':
                get_login_dict[emp_name[login]] = get_login[login]

        for logout in range(0 ,len(get_logout)):
            if get_logout[logout] != '':
                get_logout_dict[emp_name[logout]] = get_logout[logout]

        # get_login_dict = dict(zip(emp_name, get_login))
        # get_logout_dict = dict(zip(emp_name, get_logout))
        print('log in time modified ', get_login_dict)
        print('log out time modified ', get_logout_dict)
        verified_one = 0
        verified_two = 'False'

        for key, value in get_login_dict.items():
            if value not in [None,'None','']:
                if str(value) >= '08:00' and str(value) <= '17:00':
                    print('login ', key)

                    print('login ', value, str(logout_dict[key]))
                    # print('login ', value, str(get_logout_dict[key]))
                    if str(value) < str(logout_dict[key]):
                        print('greater than')
                        pass
                    else:
                        print('less than')
                        verified_two = 'True'

                    # if len(get_logout_dict) != 0:
                    if str(key) in get_logout_dict.keys():
                            if str(value) < str(get_logout_dict[key]):
                                print('greater than')
                                pass
                            else:
                                print('less than')
                                verified_two = 'True'

                    else:
                        pass
                        # verified_two = 'True'

                else:
                    verified_two = 'True'

            else:
                verified_two = 'True'

        for key, value in get_logout_dict.items():
            if value not in [None,'None','']:
                if str(value) >= '08:00' and str(value) <= '20:00':
                    print('logout ', key)
                    print('logout ', value ,str(login_dict[key]))
                    if str(value) > str(login_dict[key]):
                        print('greater than')
                        pass
                    else:
                        print('less than')
                        verified_two = 'True'

                    # if len(get_login_dict) != 0:
                    if str(key) in get_login_dict.keys():
                        if str(value) > str(get_login_dict[key]):
                            print('greater than')
                            pass
                        else:
                            print('less than')
                            verified_two = 'True'
                    else:
                        pass
                        # verified_two = 'True'

                else:
                    verified_two = 'True'
            else:
                verified_two = 'True'


        # for login in range(0 ,len(get_login)):
        #     if get_login[login] not in [None,'None','']:
        #         if str(get_login[login]) >= '08:00' and str(get_login[login]) <= '17:00':
        #             verified_one -= 1
        #         else:
        #             verified_two = 'True'
        #
        #     verified_one += 1
        #
        # for logout in range(0 ,len(get_logout)):
        #     if get_logout[logout] not in [None,'None','']:
        #         if str(get_logout[logout]) >= '08:00' and str(get_logout[logout]) <= '20:00':
        #             verified_one -= 1
        #
        #         else:
        #             verified_two = 'True'
        #
        #     verified_one += 1

        print('verified no. ',verified_one ,verified_two)
        # if len(get_login_dict) > 0 or len(get_logout_dict) > 0:
        #     pass
        if len(get_login_dict) == 0 and len(get_logout_dict) == 0:
            messages.success(request, ('Invalid: Check the Login and Logout'))
            return redirect('time_update')
        elif verified_two == 'True':
            messages.success(request, ('Invalid: Check the Login and Logout'))
            return redirect('time_update')

        data_date = data_months.filter(log_in__date=current_date).order_by('user_attend')
        get_id = []
        for data in range(0 ,len(data_date)):
            if get_login[data] != '':
                # print('data log in ',data_date[data].id  ,get_login[data])
                date_format = '%Y-%m-%d %H:%M:%S'
                nums_login = str(current_date) + ' ' + str(get_login[data]) + str(':00')
                get_logins = datetime.strptime(nums_login, date_format)
                data_date[data].log_in = get_logins
                data_date[data].save()
                get_id.append(str(data_date[data].id))

            if get_logout[data] != '':
                # print('data log out ',data_date[data].id  ,get_logout[data])
                data_date[data].log_out = get_logout[data]
                data_date[data].save()
                get_id.append(str(data_date[data].id))

        get_id = list(dict.fromkeys(get_id))

        print('get id ', get_id)
        # print('log out time modified ', get_logout)
        data_date = data_months.filter(log_in__date=current_date)
        for data in data_date:
            if str(data.id) in get_id:
                format = '%H:%M:%S'
                # print('log in ', data.log_in)
                # print('log out ', data.log_out)
                login = data.log_in.strftime('%H:%M:%S')
                logout = data.log_out.strftime('%H:%M:%S')

                total_hours = datetime.strptime(str(logout), format) - datetime.strptime(str(login), format)

                if str(logout) < '17:00:00':
                    total_hours_ot = '00:00:00'
                else:
                    total_hours_ot = datetime.strptime(str(logout), format) - datetime.strptime(
                        '17:00:00', format)
                total_hours = str(total_hours).replace(":", " ").split()
                tot_hours = float(total_hours[0]) + (int(total_hours[1]) / 60)


                total_hours_ot = str(total_hours_ot).replace(":", " ").split()
                tot_hours_ot = float(total_hours_ot[0]) + (int(total_hours_ot[1]) / 60)

                salary = float(round((tot_hours - tot_hours_ot) * 86.59, 2))
                ot_salary = tot_hours_ot * 65
                total_salaries = float(round(salary + ot_salary, 2))

                # print('total hours ', total_hours ,tot_hours)
                # print('total ot hours ', total_hours_ot ,tot_hours_ot)
                # print('total salary ', salary, ot_salary)
                # print('total salaries ', total_salaries)
                if float(tot_hours_ot) == 0:
                    data.ot_approved = False
                    data.ot_approved_time = None
                else:
                    data.ot_approved = True

                    if float(tot_hours_ot) <= 1:
                        data.ot_approved_time = str(float(round(tot_hours_ot, 1))) +' '+str('hr')
                    else:
                        data.ot_approved_time = str(float(round(tot_hours_ot, 1))) + ' ' + str('hrs')

                data.total_hour = tot_hours
                data.total_salary = total_salaries

                data.save()


        check = 'data_months'
        data_months = get_overtime_approval_month_key(get_month_attend, check)
        data_months = data_months.order_by('user_attend' ,'log_in')

        employee_pay = time_update_salary(emp_name, data_months)
        emp_name.sort()

        return render(request, 'time_update.html', {
            'date_now': date_now,
            'data_months': data_months,
            'day_select': day_select,
            'current_date': current_date,
            'employee_pay': employee_pay,


        })

    return render(request, 'time_update.html', {
        'date_now': date_now,
        'data_months': data_months,
        'day_select': day_select,
        'current_date': current_date,
        'employee_pay':employee_pay,


    })



def overtime_approval_select(request ,month_day):
    print('ovetime approval select')
    value = month_day.isdigit()
    if value == True:
        request.session['approve_days'] = month_day
    else:
        format = '%b'
        no_months = datetime.strptime(month_day, format)
        request.session['approve_months'] = no_months.strftime("%m")

    month = request.session.get('approve_months')
    if month in [None ,'None', '']:
        month = int(datetime.now().strftime('%m'))

    day = request.session.get('approve_days')
    if day in [None ,'None', '']:
        day = int(datetime.now().strftime('%d'))

    month_range = monthrange(2025, int(month))
    if int(day) > int(month_range[1]):
        messages.success(request, ('Invalid Days Select: Out of Month Day'))
        return redirect('overtime_approval')

    date_pick = date(int(2025), int(month), int(day))
    if str(date_pick.strftime("%a")) == 'Sun':
        messages.success(request, ('Invalid Days Select: Sunday'))
        return redirect('overtime_approval')

    request.session['current_dates'] = [month , day]
    return redirect('overtime_approval')
    # return render(request,'overtime_approval_select.html',{})

def get_overtime_approval_month_key(get_month_approval ,check):
    # print('get overtime approval ',get_month_approval  ,check)
    if get_month_approval == 1:
        if check == 'update_time':
            month_approval = Jans_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Jans_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Jans_2025.objects.get(id=int(check))

    elif get_month_approval == 2:
        if check == 'update_time':
            month_approval = Febs_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Febs_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Febs_2025.objects.get(id=int(check))

    elif get_month_approval == 3:
        if check == 'update_time':
            month_approval = Attendance.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval = Attendance.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Attendance.objects.get(id=int(check))

    elif get_month_approval == 4:
        if check == 'update_time':
            month_approval = Aprs_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval = Aprs_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Aprs_2025.objects.get(id=int(check))

    elif get_month_approval == 5:
        if check == 'update_time':
            month_approval = Mays_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Mays_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Mays_2025.objects.get(id=int(check))

    elif get_month_approval == 6:
        if check == 'update_time':
            month_approval = Junes_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Junes_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Junes_2025.objects.get(id=int(check))

    elif get_month_approval == 7:
        if check == 'update_time':
            month_approval = Julys_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Julys_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Julys_2025.objects.get(id=int(check))

    elif get_month_approval == 8:
        if check == 'update_time':
            month_approval = Augs_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Augs_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Augs_2025.objects.get(id=int(check))

    elif get_month_approval == 9:
        if check == 'update_time':
            month_approval = Septs_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Septs_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Septs_2025.objects.get(id=int(check))

    elif get_month_approval == 10:
        if check == 'update_time':
            month_approval = Octs_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Octs_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Octs_2025.objects.get(id=int(check))

    elif get_month_approval == 11:
        if check == 'update_time':
            month_approval = Novs_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval =Novs_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Novs_2025.objects.get(id=int(check))

    elif get_month_approval == 12:
        if check == 'update_time':
            month_approval = Decs_2025.objects.filter(ot_approved=True).order_by('user_attend')
        elif check == 'data_months':
            month_approval = Decs_2025.objects.all().order_by('log_in', 'user_attend')
        else:
            month_approval = Decs_2025.objects.get(id=int(check))

    # print('get overtime approval month key ',month_approval)
    return month_approval


def overtime_approval(request):
    print('overtime approval')
    if request.user.is_authenticated == False:
        messages.success(request, ('User is not Log-in'))
        return redirect('home')

    day_select = [x for x in range(1,32)]
    current_dates = request.session.get('current_dates')
    if current_dates in ['None',None,'']:
        # request.session['current_dates'] = datetime.now()
        current_dates = datetime.now()
    else:
        current_dates = date(int(2025), int(current_dates[0]), int(current_dates[1]))

    # current_dates = datetime.now()
    current_date = current_dates.strftime('%Y-%m-%d')
    date_now = current_dates.strftime('%A, %B %d, %Y')
    get_month_attend = int(current_dates.strftime('%m'))
    # get_year_attend = int(datetime.now().strftime('%Y'))
    ot_hour = ['30:00 mins', '01:00 hr', '01:30 hrs', '02:00 hrs', '02:30 hrs', '03:00 hrs']

    format = '%H:%M'
    ampm = datetime.strptime('12:00', format)


    # data_months = Aprs_2025.objects.all().order_by('log_in','user_attend')
    check = 'data_months'
    data_months = get_overtime_approval_month_key(get_month_attend ,check)
    data_months = data_months.order_by('user_attend')

    # print('data months ',data_months.filter(log_in__date = current_date))
    # for data in data_months.filter(log_in__date = current_date):
    #     print('log in ',data.log_in)
    ids = []
    update_ids = []
    count_approved = 0
    for data in data_months:
        if str(current_date) == str(data.log_in.strftime('%Y-%m-%d')):
            if data.ot_request == True:
                ids.append(int(data.id))

            if data.ot_approved == True:
                count_approved += 1
                update_ids.append(int(data.id))

    # print('count approved ',count_approved ,ids)
    approved = ''
    if request.method == 'POST':
        temp_ot = request.POST.getlist('time')
        check_list = request.POST.getlist('boxes')
        time_approved = request.POST.get('time_approve')

        # temp_ot_remove = [ot for ot in temp_ot if ot != 'None']
        count = 0
        modified_true = 'False'
        # print('temp ot and checklist ', temp_ot, check_list ,time_approved)
        if temp_ot == [] and check_list == [] and time_approved == '':
            return redirect('overtime_approval')

        if time_approved == 'time_modified':

            for check in update_ids:
                # save_data = Aprs_2025.objects.get(id=int(check))
                # print('save data ',get_month_attend ,get_year_attend ,check)
                save_data = get_overtime_approval_month_key(get_month_attend ,check)
                verify_logout = str(save_data.log_out.strftime('%H%M')).replace(".", "").split()
                if int(verify_logout[0]) <= 1700:
                    format = '%H:%M'
                    logout_hour = save_data.log_out.strftime('%H')
                    logout_min = save_data.log_out.strftime('%M')

                    ot_hour = save_data.ot_approved_time.split()[0].replace(".", " ").split()
                    if int(ot_hour[1]) == 5:
                        temp_mins = 3
                    else:
                        temp_mins = ot_hour[1]

                    temp_hour = int(logout_hour) + int(ot_hour[0])
                    total_hour = str(temp_hour) +str(':') + str(temp_mins) + str('0')

                    total_ot_hour = float(save_data.total_hour) + float(save_data.ot_approved_time.split()[0])

                    total_pay = (float(save_data.total_hour) * 86.59) +  (float(save_data.ot_approved_time.split()[0]) * 65)
                    save_data.log_out = total_hour
                    save_data.total_hour =  round(total_ot_hour, 2)
                    save_data.total_salary =  round(total_pay, 2)
                    save_data.save()
                    modified_true = 'True'

                else:
                    messages.success(request, (save_data.user_attend,' Overtime Salary Already Update'))
                    # return redirect('overtime_approval')

            if modified_true == 'True':
                messages.success(request, ('Overtime Salary Update'))
            return redirect('overtime_approval')


        for id in range(0 ,len(ids)):
            if str(ids[id]) in check_list:
                if temp_ot[id] == 'None':
                    messages.success(request, ('Invalid Entry'))
                    return redirect('overtime_approval')

        for temp in range(0 ,len(temp_ot)):
            if temp_ot[temp] != 'None':
                # ['30:00 mins', '01:00 hr', '01:30 hrs', '02:00 hrs', '02:30 hrs', '03:00 hrs']
                if temp_ot[temp].split()[0] == '0.5':
                    temp_ot[temp] = '30:00 mins'
                elif temp_ot[temp].split()[0] == '1.0':
                    temp_ot[temp] = '01:00 hr'
                elif temp_ot[temp].split()[0] == '1.5':
                    temp_ot[temp] = '01:30 hrs'
                elif temp_ot[temp].split()[0] == '2.0':
                    temp_ot[temp] = '02:00 hrs'
                elif temp_ot[temp].split()[0] == '2.5':
                    temp_ot[temp] = '02:30 hrs'
                elif temp_ot[temp].split()[0] == '3.0':
                    temp_ot[temp] = '03:00 hrs'

        ot_approved = dict(zip(ids, temp_ot))
        # print('ot approved ', ot_approved)
        for check in ids:
            if str(check) in check_list:
                # save_data = Aprs_2025.objects.get(id=int(check))
                save_data = get_overtime_approval_month_key(get_month_attend ,check)
                save_data.ot_approved = True
                val = ot_approved[check]

                get_val = val.split()[0].replace(":", " ").split()

                if int(get_val[0]) == 30:
                    mins = 30
                    hr = 0
                    req_mins = 0.5
                    req_hr = 0
                    hours = 'hr'

                elif int(get_val[0]) == 1:
                    hr = int(get_val[0])
                    req_hr = int(get_val[0])
                    if get_val[1] == '30':
                        mins = 30
                        hours = 'hrs'
                        req_mins = 0.5
                    else:
                        mins = '00'
                        hours = 'hr'
                        req_mins = 0

                else:
                    hr = int(get_val[0])
                    req_hr = int(get_val[0])
                    if get_val[1] == '30':
                        mins = 30
                        hours = 'hrs'
                        req_mins = 0.5

                    else:
                        mins = '00'
                        hours = 'hrs'
                        req_mins = 0

                format = '%H:%M'
                temps = str(17 + hr) +':'+ str(mins)
                temp_time = float(req_hr) + float(req_mins)
                temp_time = str(temp_time) + ' ' + str(hours)
                save_data.ot_approved_time = temp_time


            else:
                # save_data = Aprs_2025.objects.get(id=int(check))
                save_data = get_overtime_approval_month_key(get_month_attend ,check)
                format = '%H:%M'
                temp_login = save_data.log_in.strftime('%H:%M')
                temp_logout = save_data.log_out.strftime('%H:%M')
                regular_hrs = datetime.strptime('17:00', format) - datetime.strptime(temp_login, format)
                regular_hrs =  float(str(regular_hrs).replace(":", " ")[0])  + float(str(regular_hrs).replace(":", " ")[2:4]) / 60

                save_data.total_hour =  round(regular_hrs, 2)
                save_data.total_salary =  round(regular_hrs * 86.59 , 2)

                save_data.ot_approved = False
                save_data.ot_approved_time = None
                format = '%H:%M'
                save_data.log_out = datetime.strptime('17:00', format)

            save_data.save()

        if count_approved < len(check_list):
            # request.session['notifys'] = len(check_list)
            messages.success(request, ('OT Request Approved'))
        elif count_approved > len(check_list):
            # request.session['notifys'] = len(check_list)
            messages.success(request, ('OT Request Dispproved'))

        # data_months = get_overtime_approval_month(get_month_attend, get_year_attend)
        check = 'data_months'
        data_months = get_overtime_approval_month_key(get_month_attend, check)
        data_months = data_months.order_by('user_attend')

    # Update Overtime Time

    check = 'update_time'
    update_ot_time = get_overtime_approval_month_key(get_month_attend ,check)
    # update_ot_time = data_months.filter(ot_approved=True).order_by('user_attend')

    return render(request, 'overtime_approval.html', {
        'date_now': date_now,
        'data_months': data_months,
        'current_date':current_date,
        'ot_hour':ot_hour,
        'update_ot_time':update_ot_time,
        'day_select': day_select,
        'ampm': ampm,
    })


def overtime_select(request, date_ot):
    date_ot = date_ot.replace("-", " ").split()
    # print('date request ',date_ot ,type(date_ot))
    request.session['date_request_ot'] = date_ot
    return redirect('overtime')

def overtime_five_days():
    date_now = datetime.now()
    dates = date_now.strftime('%Y-%m-%d')
    month = int(date_now.strftime('%m'))
    day = int(date_now.strftime('%d'))
    month_range = monthrange(2025, int(month))
    loop = day
    date_pick = date(2025, int(month), int(day))

    loop_range = loop + 4
    new_loop = 1
    list_month = []
    while loop <= loop_range:
        if loop <= month_range[1]:
            date_pick = date(2025, int(month), int(loop))
            if str(date_pick.strftime('%a')) == 'Sun':
                loop_range += 1

            else:
                list_month.append(date_pick)
                # print('date pick', date_pick.strftime('%Y-%m-%d'))

        # else:
        #     date_pick = date(2025, int(month + 1), int(new_loop))
        #     new_loop += 1
        loop += 1
    return list_month

def overtime(request):
    print('overtime')
    if request.user.is_authenticated == False:
        messages.success(request, ('User is not Log-in'))
        return redirect('home')

    ot_five_days = overtime_five_days

    current_dates = request.session.get('date_request_ot')
    if current_dates not in ['', None, 'None']:
        current_dates = date(2025, int(current_dates[1]), int(current_dates[2]))
    else:
        current_dates = datetime.now()

    current_date = current_dates.strftime('%Y-%m-%d')
    date_now = current_dates.strftime('%A, %B %d, %Y')
    get_month_overtime = int(current_dates.strftime('%m'))

    ot_hour = ['30:00 mins' ,'01:00 hr', '01:30 hrs', '02:00 hrs' ,'02:30 hrs' ,'03:00 hrs']
    temp_ot = request.POST.get('ot')
    temp_time = request.POST.get('time')
    if str(temp_time) not in ['Select Time' ,None ,'None']:
        val = temp_time.split()
        date_format = '%Y-%m-%d %H:%M'
        get_val = val[0].replace(":", " ").split()
        if int(get_val[0]) == 30:
            mins = 0.5
            hr = 0.0
            hours = 'hr'

        elif int(get_val[0]) == 1:
            hr = int(get_val[0])

            if get_val[1] == '30':
                mins = 0.5
                hours = 'hrs'

            else:
                mins = 0.0
                hours = 'hr'

        else:
            hr = int(get_val[0])
            hours = 'hrs'

            if get_val[1] == '30':
                mins = 0.5
                hours = 'hrs'

            else:
                mins = 0.0
                hours = 'hrs'

        temps = float(hr) + mins
        get_val = str(temps) +' ' +str(hours)

    else:
        get_val = 'False'

    # ot_month = Attendance.objects.all()
    # data_months = Attendance.objects.filter(user_attend = request.user)
    check = 'data_months'
    # ot_month = Aprs_2025.objects.all().order_by('log_in','user_attend')
    ot_month = get_overtime_approval_month_key(get_month_overtime, check)
    count_approved = 0

    noti_count = Notifies.objects.filter(is_seen=True).count()

    reqs_noti = []
    for data in ot_month:
        if str(current_date) == str(data.log_in.strftime('%Y-%m-%d')):
            if str(data.user_attend) == str(request.user):
                # ot_days = Aprs_2025.objects.get(id=data.id)
                check = data.id
                ot_days = get_overtime_approval_month_key(get_month_overtime, check)
                # for ot in ot_month:
                #     if str(ot.id) == str(data.id):
                #         ot_days = ot
                reqs_noti.append(data.user_attend)

            if data.ot_request == True:
                count_approved += 1


    if request.method == 'POST':
        if temp_ot == 'True' and get_val != 'False':
            ot_days.ot_request = True
            ot_days.ot_request_time = get_val
            ot_days.save()
            messages.success(request, ('Request Overtime on Process'))

            for reqs in reqs_noti:
                Notifies.objects.filter(notify_user=reqs, is_seen=False).update(is_seen=True)
            noti_count = Notifies.objects.filter(is_seen=True).count()
            request.session['value_notify'] = get_val

        elif temp_ot != 'False' :
            messages.success(request, ('Request Overtime Incomplete'))
        else:
            ot_days.ot_request = False
            ot_days.ot_request_time = None
            ot_days.save()
            messages.success(request, ('No Request Overtime'))

        return render(request, 'overtime.html', {'ot_hour': ot_hour,
                                                 'ot_days': ot_days,
                                                 'date_now': date_now,
                                                 'ot_month': ot_month,
                                                 'noti_count': noti_count,
                                                 'ot_five_days': ot_five_days,
                                                 })

    else:
        return render(request, 'overtime.html', {'ot_hour':ot_hour,
                                                 'ot_days':ot_days,
                                                 'date_now':date_now,
                                                 'ot_month':ot_month,
                                                 'noti_count':noti_count,
                                                 'ot_five_days': ot_five_days,
                                                 })

def notifications(request):
    Notifies.objects.filter(is_seen=True).update(is_seen=False)
    messages.success(request, ('Notifications Empty'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# def overtime(request):
#     print('overtime field')
#     # attends = Febs_2025()
#
#     # dt = datetime.now()
#     # dt.hour = 22
#     # dt.minute = 0
#     # dt.second = 0
#
#     loop = 1
#     # selected_month = Febs_2025.objects.all().order_by('log_in', 'user_attend')
#     while loop <= 31:
#         date_pick = date(int(2025), int(12), int(loop))
#         date_whole = date_pick.strftime('%Y-%m-%d')
#         selected_month = Decs_2025.objects.all().order_by('log_in', 'user_attend')
#         for select in selected_month:
#             if str(select.log_in.strftime('%Y-%m-%d')) == date_whole:
#                 # print('user and month', select.user_attend, date_whole, select.log_in.strftime('%Y-%m-%d'))
#
#                 format = '%H:%M'
#                 temp_login = select.log_in.strftime('%H:%M')
#                 temp_logout = select.log_out.strftime('%H:%M')
#
#                 regular_hrs = datetime.strptime('17:00', format) - datetime.strptime(temp_login, format)
#                 # print('regular hours ',select.user_attend ,regular_hrs)
#                 ot_time = datetime.strptime(temp_logout, format) - datetime.strptime('17:00',format)
#
#                 ot_time = datetime.strptime(str(ot_time), "%H:%M:%S")
#                 ot_hr = float(ot_time.strftime('%H'))
#                 ot_min = float(ot_time.strftime('%M'))
#                 if ot_min != 0 :
#                     ot_total_time = ot_hr + .5
#                 else:
#                     ot_total_time = ot_hr
#
#                 if ot_total_time == 0:
#                     ot_request = False
#                 else:
#                     if ot_total_time <= 1:
#                         ot_total_time = str(ot_total_time) +' '+ str('hr')
#                     else:
#                         ot_total_time = str(ot_total_time) + ' ' + str('hrs')
#                     ot_request = True
#
#                 print('overtime hours ', select.user_attend, ot_time, ot_hr, ot_min, ot_total_time ,ot_request)
#
#                 select.ot_request = ot_request
#                 select.ot_request_time  = ot_total_time
#                 select.ot_approved = ot_request
#                 select.ot_approved_time = ot_total_time
#                 select.save()
#         loop += 1
#     return render(request, "overtime.html", {})

def attendance_update(request ,pk ,monthyear):
    print('attendance update ', pk, monthyear )
    return_back = request.session.get('back_return')

    value = pk.isdigit()
    valid= ''
    if value == True:
        # print('pk is integer ')
        months = monthyear[0:3].lower()
        pk = pk
        valid = 'true'
    else:
        # print('pk is datetime ',pk ,type(pk))
        nums = pk.replace("-", " ").split()
        get_dates = date(int(nums[0]), int(nums[1]), int(nums[2]))
        months = str(get_dates.strftime('%b').lower())
        valid = 'false'

    if months == 'jan':
        if valid == 'true':
            prof = Jans_2025.objects.get(pk=int(pk))
            pick_attend = Jans_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Jans_2025.objects.all()
            pick_attend = Jans_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')

    elif months == 'feb':
        # prof = Febs_2025.objects.get(pk=int(pk))
        # pick_attend = Febs_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')
        if valid == 'true':
            prof = Febs_2025.objects.get(pk=int(pk))
            pick_attend = Febs_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Febs_2025.objects.all()
            pick_attend = Febs_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')

    elif months == 'mar':
        # prof = Attendance.objects.get(pk=int(pk))
        # pick_attend = Attendance.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Attendance.objects.get(pk=int(pk))
            pick_attend = Attendance.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Attendance.objects.all()
            pick_attend = Attendance.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')

    elif months == 'apr':
        # prof = Aprs_2025.objects.get(pk=int(pk))
        # pick_attend = Aprs_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')
        if valid == 'true':
            prof = Aprs_2025.objects.get(pk=int(pk))
            pick_attend = Aprs_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Aprs_2025.objects.all()
            pick_attend = Aprs_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')

    elif months == 'may':
        # prof = Mays_2025.objects.get(pk=int(pk))
        # pick_attend = Mays_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Mays_2025.objects.get(pk=int(pk))
            pick_attend = Mays_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Mays_2025.objects.all()
            pick_attend = Mays_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')

    elif months == 'jun':
        # prof = Junes_2025.objects.get(pk=int(pk))
        # pick_attend = Junes_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Junes_2025.objects.get(pk=int(pk))
            pick_attend = Junes_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Junes_2025.objects.all()
            pick_attend = Junes_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')


    elif months == 'jul':
        # prof = Julys_2025.objects.get(pk=int(pk))
        # pick_attend = Julys_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Julys_2025.objects.get(pk=int(pk))
            pick_attend = Julys_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Julys_2025.objects.all()
            pick_attend = Julys_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')

    elif months == 'aug':
        # prof = Augs_2025.objects.get(pk=int(pk))
        # pick_attend = Augs_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Augs_2025.objects.get(pk=int(pk))
            pick_attend = Augs_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Augs_2025.objects.all()
            pick_attend = Augs_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')

    elif months == 'sep':
        # prof = Septs_2025.objects.get(pk=int(pk))
        # pick_attend = Septs_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Septs_2025.objects.get(pk=int(pk))
            pick_attend = Septs_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Septs_2025.objects.all()
            pick_attend = Septs_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')


    elif months == 'oct':
        # prof = Octs_2025.objects.get(pk=int(pk))
        # pick_attend = Octs_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Octs_2025.objects.get(pk=int(pk))
            pick_attend = Octs_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Octs_2025.objects.all()
            pick_attend = Octs_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')


    elif months == 'nov':
        # prof = Novs_2025.objects.get(pk=int(pk))
        # pick_attend = Novs_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Novs_2025.objects.get(pk=int(pk))
            pick_attend = Novs_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Novs_2025.objects.all()
            pick_attend = Novs_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')


    elif months == 'dec':
        # prof = Decs_2025.objects.get(pk=int(pk))
        # pick_attend = Decs_2025.objects.filter(user_attend = prof.user_attend).order_by('log_in')

        if valid == 'true':
            prof = Decs_2025.objects.get(pk=int(pk))
            pick_attend = Decs_2025.objects.filter(user_attend=prof.user_attend).order_by('log_in','user_attend')
        else:
            prof = Decs_2025.objects.all()
            pick_attend = Decs_2025.objects.filter(user_attend=monthyear).order_by('log_in','user_attend')


    get_name = Profile.objects.all()
    for name in get_name:
        if str(name.user) == monthyear:
            get_names = name

    fifth_pay = {}
    twenty_pay = {}
    sum_fifth_pay = {}
    sum_twenty_pay = {}

    total_fifth_pay = {}
    fifth_total_days = 0
    fifth_total_hrs = 0
    fifth_ot_total =0
    fifth_ot_salary =0
    fifth_total_payment = 0
    fifth_total_salary = 0

    total_twenty_pay = {}
    twenty_total_days = 0
    twenty_total_hrs = 0
    twenty_ot_total = 0
    twenty_ot_salary = 0
    twenty_total_payment = 0
    twenty_total_salary = 0
    for pick in pick_attend:
        temp = []
        if int(pick.log_in.strftime('%d')) >= 5 and int(pick.log_in.strftime('%d')) <= 20:
            if pick.log_in.strftime('%a') != 'Sun':
                val = int(pick.log_in.strftime('%d'))
                temp.append(pick.log_in.strftime('%a %B %d, %Y'))
                temp.append(pick.log_in.strftime('%I:%M %p'))
                temp.append(pick.log_out.strftime('%I:%M %p'))
                temp_login = pick.log_in.strftime('%H:%M')
                temp_logout = pick.log_out.strftime('%H:%M')

                format = '%H:%M'
                total_hrs =  datetime.strptime('17:00', format) - datetime.strptime(temp_login, format)
                total_ot_hr = datetime.strptime(temp_logout, format) - datetime.strptime('17:00', format)

                format = '%H:%M'
                total_hours = str(total_hrs)
                date_format = '%H:%M:%S'

                total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
                ot_times = total_ot_hr.strftime('%H %M').split()
                # ot_times = ot_times.split()
                ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
                ot_hrs = float(round(ots, 2))

                total_hours = datetime.strptime(total_hours, date_format)
                times = total_hours.strftime('%H %M')
                times = times.split()
                hour = float(times[0]) + (float(times[1]) / 60)
                total_hrs = float(round(hour, 2))

                ot_per_hour = 65
                ot_total_pay = ot_hrs * 65
                total_salary = total_hrs * 86.59
                total_payment = total_salary + ot_total_pay

                temp.append(total_hrs)
                temp.append(pick.total_rate)
                temp.append(ot_hrs)
                temp.append('{:,.2f}'.format(ot_per_hour))
                temp.append(ot_total_pay)
                temp.append('{:,.2f}'.format(total_salary))
                temp.append('{:,.2f}'.format(total_payment))

                # summary computation
                fifth_total_days += 1
                fifth_total_hrs += total_hrs
                fifth_ot_total += ot_hrs
                fifth_ot_salary += ot_total_pay
                fifth_total_payment += total_salary
                fifth_total_salary += total_payment

                fifth_pay[val] = temp

            else:
                val = int(pick.log_in.strftime('%d'))

                temp.append(pick.log_in.strftime('%a %B %d, %Y'))
                temp.append('Day-off')
                fifth_pay[val] = temp
        else:

            if pick.log_in.strftime('%a') != 'Sun':
                val = int(pick.log_in.strftime('%d'))
                temp.append(pick.log_in.strftime('%a %B %d, %Y'))
                temp.append(pick.log_in.strftime('%I:%M %p'))
                temp.append(pick.log_out.strftime('%I:%M %p'))
                temp_login = pick.log_in.strftime('%H:%M')
                temp_logout = pick.log_out.strftime('%H:%M')

                format = '%H:%M'
                total_hrs = datetime.strptime('17:00', format) - datetime.strptime(temp_login, format)
                total_ot_hr = datetime.strptime(temp_logout, format) - datetime.strptime('17:00', format)

                format = '%H:%M'
                total_hours = str(total_hrs)
                date_format = '%H:%M:%S'

                total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
                ot_times = total_ot_hr.strftime('%H %M').split()
                # ot_times = ot_times.split()
                ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
                ot_hrs = float(round(ots, 2))

                total_hours = datetime.strptime(total_hours, date_format)
                times = total_hours.strftime('%H %M')
                times = times.split()
                hour = float(times[0]) + (float(times[1]) / 60)
                total_hrs = float(round(hour, 2))

                ot_per_hour = 65
                ot_total_pay = ot_hrs * 65
                total_salary = total_hrs * 86.59
                total_payment = total_salary + ot_total_pay

                temp.append(total_hrs)
                temp.append(pick.total_rate)
                temp.append(ot_hrs)
                temp.append('{:,.2f}'.format(ot_per_hour))
                temp.append(ot_total_pay)
                temp.append('{:,.2f}'.format(total_salary))
                temp.append('{:,.2f}'.format(total_payment))

                # total summary
                twenty_total_days += 1
                twenty_total_hrs += total_hrs
                twenty_ot_total += ot_hrs
                twenty_ot_salary += ot_total_pay
                twenty_total_payment += total_salary
                twenty_total_salary += total_payment
                twenty_pay[val] = temp

            else:
                val = int(pick.log_in.strftime('%d'))
                temp.append(pick.log_in.strftime('%a %B %d, %Y'))
                temp.append('Day-off')
                twenty_pay[val] = temp

    total_fifth_pay['Total Days'] = fifth_total_days
    total_fifth_pay['Total Hrs'] = fifth_total_hrs
    total_fifth_pay['OT Total Hrs'] =  '{:,.1f}'.format(fifth_ot_total)
    total_fifth_pay['OT Salary'] =  '{:,.2f}'.format(fifth_ot_salary)
    total_fifth_pay['Total Payment'] =  '{:,.2f}'.format(fifth_total_payment)
    total_fifth_pay['Total Salary'] =   '{:,.2f}'.format(fifth_total_salary)

    total_twenty_pay['Total Days'] = twenty_total_days
    total_twenty_pay['Total Hrs'] = twenty_total_hrs
    total_twenty_pay['OT Total Hrs'] =  '{:,.1f}'.format(twenty_ot_total)
    total_twenty_pay['OT Salary'] = '{:,.2f}'.format(twenty_ot_salary)
    total_twenty_pay['Total Payment'] =  '{:,.2f}'.format(twenty_total_payment)
    total_twenty_pay['Total Salary'] =  '{:,.2f}'.format(twenty_total_salary)

    return render(request, "attendance_update.html", {'fifth_pay':fifth_pay,
              'twenty_pay': twenty_pay,
              'total_fifth_pay': total_fifth_pay,
              'total_twenty_pay':total_twenty_pay,
              'get_names':get_names,
              'return_back': return_back,
              })


def attendance_attend_gets(get_months):
    global pick_attends
    pick_attend_update_attend = {'jan': Jans_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'feb': Febs_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'mar': Attendance.objects.all().order_by('user_attend', 'log_in'),
                                 'apr': Aprs_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'may': Mays_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'jun': Junes_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'jul': Julys_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'aug': Augs_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'sep': Septs_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'oct': Octs_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'nov': Novs_2025.objects.all().order_by('user_attend', 'log_in'),
                                 'dec': Decs_2025.objects.all().order_by('user_attend', 'log_in')}

    for keys, values in pick_attend_update_attend.items():
        if keys == get_months:
            pick_attends = values

    return pick_attends


def attendance(request):
    global pick_attends
    print('attendanceeeeeee ',pick_attends)
    request.session['back_return'] = 'attendance_back'
    attend_date = request.session.get('context')

    name_nums = request.session.get('name_nums')
    month_year_dates = request.session.get('datess')
    dict_attend = request.session.get('dict_attends')
    nums_username = ''

    print('attend date ',attend_date)
    print('name nums ', name_nums)
    print('month year dates ', month_year_dates)
    print('dict attend ', dict_attend)
    if attend_date is None:
        pick_attends = pick_attends
    else:
        pick_attends = attendance_attend_gets(attend_date[0])

    if name_nums is None:
        num_days = []
        name_days = []
    else:
        num_days = name_nums[0]
        name_days = name_nums[1]
    # print('name & number month ', name_nums)

    if request.method == "POST":
        print('request method post attendanceeeeeeeeeeeeeeeeeee')
        get_month = request.POST.get('month')
        get_year = request.POST.get('year')
        resets = request.POST.get('reset_name')

        # print('get reset ', resets)
        # print('get year ', get_year)
        context = [get_month, get_year]
        pick_attend = ''

        if resets == 'reset':
            num_days = None
            name_days = None
            month_year_dates = None
            nums_username = None
            request.session['name_nums'] = None
            request.session['attend_info'] = None
            request.session['datess'] = None
            context = [None]
            request.session['context'] = context
            pick_attends = ''
            dict_attend = {}

        print('context ',context)
        if None not in context:
            request.session['context'] = context

            if context[0] == 'jan':
                pick_attend = Jans_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Jans_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'January 2025'

            elif context[0] == 'feb':
                pick_attend = Febs_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Febs_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'February 2025'
            elif context[0] == 'mar':
                pick_attend = Attendance.objects.all().order_by('user_attend','log_in')
                pick_username = Attendance.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'March 2025'
            elif context[0] == 'apr':
                pick_attend = Aprs_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Aprs_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'April 2025'
            elif context[0] == 'may':
                pick_attend = Mays_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Mays_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'May 2025'
            elif context[0] == 'jun':
                pick_attend = Junes_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Junes_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'June 2025'
            elif context[0] == 'jul':
                pick_attend = Julys_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Julys_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'July 2025'
            elif context[0] == 'aug':
                pick_attend = Augs_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Augs_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'Augaust 2025'
            elif context[0] == 'sep':
                pick_attend = Septs_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Septs_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'September 2025'
            elif context[0] == 'oct':
                pick_attend = Octs_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Octs_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'October 2025'
            elif context[0] == 'nov':
                pick_attend = Novs_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Novs_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'November 2025'
            elif context[0] == 'dec':
                pick_attend = Decs_2025.objects.all().order_by('user_attend','log_in')
                pick_username = Decs_2025.objects.all().order_by('user_attend')
                month_year_dates = request.session['datess'] = 'December 2025'

            nums_username = {}
            num_days = []
            name_days = []
            namedays = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

            month_to_num = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
            for key, value in month_to_num.items():
                if key == context[0]:
                    nums = value
            no_day = monthrange(int(context[1]) ,int(nums))
            start_days = date(int(context[1]), int(nums), 1)
            start_days = str(start_days.strftime('%a'))
            start_days = ''.join(start_days[0:2])
            no_index = int(namedays.index(start_days))
            for x in range(1, int(no_day[1]) + 1):
                name_days.append(namedays[no_index])
                num_days.append(str(x))
                no_index += 1
                if no_index == 7 :
                    no_index = 0

            prof = Profile.objects.all().order_by('user')
            for x in pick_username:
                if str(x.user_attend) not in nums_username.keys():
                    for y in prof:
                        if str(y.user) == x.user_attend:
                            profs =  str(y.last_name)+ str(', ') + str(y.first_name)
                    nums_username[x.user_attend] = int(x.id) ,profs

            # print('username ',nums_username)
            counts = 1
            for key, value in nums_username.items():
                for y in pick_attend:
                    if key == str(y.user_attend):
                        if counts == int(y.log_in.strftime('%d')):
                            if str(y.log_in.strftime('%a')) == 'Sun':
                                # temps = y.log_in.strftime('%Y-%m-%d %H:%M:%S')
                                value += ('D',)
                                nums_username.update({key:value})
                            else:
                                # temps = str('Login: ')+(str(y.log_in.strftime('%H:%M'))
                                #          +' '+ str('Logout: ')+str(y.log_out.strftime('%H:%M')))
                                temps = y.log_in.strftime('%Y-%m-%d')

                                value += (temps,)
                                nums_username.update({key: value})
                        else:
                            pass
                        counts += 1
                        if counts == no_day[1] + 1:
                            counts = 1

            context_one = [num_days, name_days]
            request.session['name_nums'] = context_one

            pick_attends = attendance_attend_gets(context[0])
            # pick_attends = pick_attend
            dict_attend = {}
            for x in pick_attends:
                if str(x.user_attend) not in dict_attend.keys():
                    for prof in Profile.objects.all():
                        if str(prof.user) == str(x.user_attend):
                            names = str(prof.first_name) +' '+ str(prof.last_name)
                            attends = str(x.user_attend)
                            bodynum = str(prof.bodynum)

                dict_attend[str(x.user_attend)] =  str(x.id) ,str(x.user_attend) ,names, str(x.log_in.strftime('%Y-%m-%d')), bodynum

            request.session['dict_attends'] = dict_attend


            return render(request, "attendance.html", {'num_days': num_days,
                       'name_days': name_days,
                       'month_year_dates':month_year_dates,
                       'pick_username':pick_username,
                       'pick_attends': pick_attends,
                       'dict_attend': dict_attend,
                       })

        else:
            pass
            # print('context incomplete information')
            # attend_date = request.session.get('context')

    return render(request, "attendance.html", {'num_days':num_days,
           'name_days':name_days,
           'month_year_dates': month_year_dates,
           'pick_attends': pick_attends,
           'dict_attend': dict_attend,

           })

# def attendance(request):
#     attends = Jans_2025()
#     prof = Profile.objects.all()

    # dt = datetime.now()
    # dt.hour = 22
    # dt.minute = 0
    # dt.second = 0

    # for x in prof:
        # print(x.user)
    # loop = 1
    # Jans_2025.objects.filter(user_attend=usernames).order_by('log_in')
    # while loop <= 31:
    #     date_pick = date(int(2025), int(1), int(loop))
    #     date_whole= date_pick.strftime('%Y %m %d')

        # dates_list = str('2025-12-')+str(loop)+' '+str('08:00:00')
        # attend =  [['defensived'],
        #            ['hardworks'],
        #            ['shielded'],
        #            ['affairs'],
        #            ['delicious'],
        #            ['fulloves'],
        #            ['heartys'],
        #            ['romances'],
        #            ['secretlove'],
        #            ['strongman']]
        #
        #
        # for x in range(0 ,len(attend)):
        #     attends = Jans_2025()
        #
        #     if attend[x].log_in.strftime('%Y-%m-%d') :
        #
            # print('date time ',attend[x][0])
            # date_format = '%Y-%m-%d %H:%M:%S'
            # time_login = datetime.strptime(attend[x][1], date_format)
            # time_logins = time_login.strftime('%Y-%m-%d %H:%M:%S')
            # # print('time_logins ', time_logins ,x[2])
            # time_logout = datetime.strptime(attend[x][2], '%H:%M:%S').time()
            # time_logouts = time_logout.strftime('%H:%M:%S')
            # # print('time_logouts ', time_logouts)
            #
            # nums_time = time_logouts.replace(":", " ")
            # nums_time = nums_time.split()
            # total_login_out =  int(time_logout.strftime('%H')) - int(time_login.strftime('%H'))
            # # print('total_login_out ', total_login_out)
            #
            # date_format = '%H:%M'
            # total_hours = datetime.strptime(str(total_login_out)+str(':00'), date_format)
            #
            # times = total_hours.strftime('%H %M')
            # times = times.split()
            # # print('time ', times)
            # hour = float(times[0]) + (float(times[1]) / 60)
            # total_hours = float(round(hour, 2))
            # # print('hours ', total_hours)
            # total_salaries = total_hours * 86.59
            # total_salaries = float(round(total_salaries, 2))



            # attends.user_attend =
            # attends.log_in =
            # attends.log_out =
            # attends.total_hour =
            # attends.total_rate =
            # attends.total_salary = total_salaries


            # attends.save()
    #     loop += 1
    # return render(request, "attendance.html", {})

def get_attendance_payroll(get_month_attend ,usernames, get_year_attend):
    print('get attendance payroll ',get_month_attend ,usernames, get_year_attend)
    jan = Jans_2025.objects.filter(user_attend=usernames).order_by('log_in')
    feb = Febs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    mar = Attendance.objects.filter(user_attend=usernames).order_by('log_in')
    apr = Aprs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    may = Mays_2025.objects.filter(user_attend=usernames).order_by('log_in')
    jun = Junes_2025.objects.filter(user_attend=usernames).order_by('log_in')
    jul = Julys_2025.objects.filter(user_attend=usernames).order_by('log_in')
    aug = Augs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    sep = Septs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    oct = Octs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    nov = Novs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    dec = Decs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    list_month = [jan, feb ,mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    loop = 0
    month_attendance = ''
    print('get month attend and usernames ',get_month_attend ,usernames)
    if get_year_attend == 2025:
        while loop <= 11:
            for x in list_month[loop]:
                # print('month name ',x.log_in.strftime('%m'))
                month_num = int(x.log_in.strftime('%m'))
                if month_num == get_month_attend:
                    month_attendance = list_month[loop]
                    loop = 12
                    break
            loop += 1

    # print('Get month number attendance ', month_attendance)
    return month_attendance

def calendars_update(request ,date_pick ,date_key):
    print('calendars update')
    return_back = request.session.get('back_return')
    print('return back ', return_back)
    date_pick_get = date_pick
    date_pick_key = date_key
    print('date picks ',date_pick)
    print('date key ', date_key)
    choose_profile = Profile.objects.all()
    for names in choose_profile:
        if str(names.user) == str(date_key):
            names_users = str(names.first_name) +' '+ str(names.last_name)
    # print('name users ',names_users)
    picks = ''
    if '[' in list(date_pick):
        date_pick = date_pick.replace("[", "")
        date_pick = date_pick.replace("]", "")
        date_pick = date_pick.replace(",", "")
        date_pick = date_pick.replace("'", "").split()
        date_pick = date_pick[1]
        date_pick = date_pick.replace("-", " ").split()
        usernames = date_key
        picks = 'true'

    else:
        date_pick = date_pick.replace("-", " ").split()
        usernames = date_key
        picks = 'false'

    date_pick = date(int(date_pick[0]), int(date_pick[1]), int(date_pick[2]))
    date_whole_date = date_pick.strftime('%Y %m %d')
    date_of_update = date_pick.strftime('%B %d, %Y')
    date_month = date_pick.strftime('%b').lower()

    jan = Jans_2025.objects.filter(user_attend=usernames).order_by('log_in')
    feb = Febs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    mar = Attendance.objects.filter(user_attend=usernames).order_by('log_in')
    apr = Aprs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    may = Mays_2025.objects.filter(user_attend=usernames).order_by('log_in')
    jun = Junes_2025.objects.filter(user_attend=usernames).order_by('log_in')
    jul = Julys_2025.objects.filter(user_attend=usernames).order_by('log_in')
    aug = Augs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    sep = Septs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    oct = Octs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    nov = Novs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    dec = Decs_2025.objects.filter(user_attend=usernames).order_by('log_in')
    list_month = {'jan':jan, 'feb':feb, 'mar':mar, 'apr':apr, 'may':may, 'jun':jun, 'jul':jul, 'aug':aug, 'sep':sep, 'oct':oct, 'nov':nov, 'dec':dec}

    select_date ={}

    for key, value in list_month.items():
        if str(key) == str(date_month):
            temp = value

    for x in temp:
        if str(x.log_in.strftime('%Y %m %d')) == date_whole_date:
            numpk = x.pk
            get_querys = x

            temp_login =  x.log_in.strftime('%H:%M')
            temp_logout = x.log_out.strftime('%H:%M')

    format = '%H:%M'
    total_hrs = datetime.strptime(temp_logout, format) - datetime.strptime(temp_login, format)

    if str(temp_logout) < '17:00:00':
        total_ot_hr = '00:00:00'
    else:
        total_ot_hr = datetime.strptime(str(temp_logout), format) - datetime.strptime(
            '17:00', format)


    # total_ot_hr = datetime.strptime(temp_logout, format) - datetime.strptime('17:00', format)

    format = '%H:%M'
    total_hours = str(total_hrs)
    date_format = '%H:%M:%S'
    total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
    ot_times = total_ot_hr.strftime('%H %M')
    ot_times = ot_times.split()
    ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
    ot_hrs = float(round(ots, 1))

    total_hours = datetime.strptime(total_hours, date_format)
    times = total_hours.strftime('%H %M')
    times = times.split()
    hour = float(times[0]) + (float(times[1]) / 60)
    total_hrs = float(round(hour, 1))
    total_hr = total_hrs

    total_hrs = total_hrs - ot_hrs

    ot_per_hour = 65
    ot_total_pay= ot_hrs * 65
    total_salary = total_hrs * 86.59
    total_payment = total_salary + ot_total_pay


    select_date['Total Hour'] = total_hr
    select_date['Rate'] = 86.59
    select_date['OT Hours'] = ot_hrs
    select_date['OT Rate'] = 65
    select_date['OT Pay'] = round(ot_total_pay, 2)
    select_date['Total Salary'] =  round(total_salary, 2)
    select_date['Total Payment'] = round(total_payment, 2)
    login_of_update = get_querys.log_in.strftime('%I:%M %p')
    logout_of_update = get_querys.log_out.strftime('%I:%M %p')


    if request.method == "POST":
        # get_date = request.POST['dates']
        get_login = request.POST['login']
        get_logout = request.POST['logout']

        info_complete = 'true'
        if get_login == '':
            info_complete = 'false'

        if get_logout == '':
            info_complete = 'false'

        if info_complete == 'false':
            return redirect('calendars_update',date_pick= date_pick_get ,date_key = date_pick_key)


        if str(date_month) == 'jan':
            update_date = Jans_2025.objects.filter(id = numpk)

        elif str(date_month) == 'feb':
            update_date = Febs_2025.objects.filter(id = numpk)
        elif str(date_month) == 'mar':
            update_date = Attendance.objects.filter(id = numpk)
        elif str(date_month) == 'apr':
            update_date = Aprs_2025.objects.filter(id = numpk)
        elif str(date_month) == 'may':
            update_date = Mays_2025.objects.filter(id = numpk)
        elif str(date_month) == 'jun':
            update_date = Junes_2025.objects.filter(id = numpk)
        elif str(date_month) == 'jul':
            update_date = Julys_2025.objects.filter(id = numpk)
        elif str(date_month) == 'aug':
            update_date = Augs_2025.objects.filter(id = numpk)
        elif str(date_month) == 'sep':
            update_date = Septs_2025.objects.filter(id = numpk)
        elif str(date_month) == 'oct':
            update_date = Octs_2025.objects.filter(id = numpk)
        elif str(date_month) == 'nov':
            update_date = Novs_2025.objects.filter(id = numpk)
        elif str(date_month) == 'dec':
            update_date = Decs_2025.objects.filter(id = numpk)

        # date_format = '%Y-%m-%d %H:%M:%S'
        #             time_login = datetime.strptime(attend[x][1], date_format)
        #             time_logins = time_login.strftime('%Y-%m-%d %H:%M:%S')


        date_format = '%Y-%m-%d %H:%M:%S'
        nums_date = str(date_pick.strftime('%Y-%m-%d'))
        nums_login = str(nums_date) +' '+str(get_login)+str(':00')
        get_login = datetime.strptime(nums_login, date_format)
        get_logins = get_login.strftime('%H %M')
        temp_login = get_login.strftime('%H:%M')

        nums_logout = str(nums_date) + ' ' + str(get_logout) + str(':00')
        get_logout = datetime.strptime(nums_logout, date_format)
        get_logouts = get_logout.strftime('%H %M')
        temp_logout = get_logout.strftime('%H:%M')

        format = '%H:%M'
        total_hours = datetime.strptime(temp_logout, format) - datetime.strptime(temp_login, format)

        print('total hours ',total_hours)
        if str(temp_logout) < '17:00:00':
            total_ot_hr = '00:00:00'
            ot_reqs = False
            ot_reqs_val = None
        else:
            total_ot_hr = datetime.strptime(str(temp_logout), format) - datetime.strptime(
                '17:00', format)
            ot_reqs = True

        format = '%H:%M:%S'
        total_hours = datetime.strptime(str(total_hours), format) - datetime.strptime(
            str(total_ot_hr), format)


        date_format = '%H:%M:%S'
        total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
        ot_times = total_ot_hr.strftime('%H %M').split()
        ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
        total_ot = float(round(ots, 2))
        total_ot_salaries = float(round(ots * 65, 2))

        if ot_reqs == True:
            if total_ot <= 1:
                ot_reqs_val = str(total_ot) +str(' hr')
            else:
                ot_reqs_val = str(total_ot) + str(' hrs')

        total_hours =str(total_hours)
        date_format = '%H:%M:%S'
        total_hours = datetime.strptime(total_hours, date_format)
        times = total_hours.strftime('%H %M')
        times = times.split()
        hour = float(times[0]) + (float(times[1]) / 60)
        total_hours = float(round(hour, 2))
        total_salaries = total_hours * 86.59
        total_salaries = float(round(total_salaries + total_ot_salaries, 2))

        total_hours = total_hours + total_ot


        if info_complete == 'true':
            update_date.update(log_in = get_login ,log_out = get_logout ,total_hour= total_hours,total_rate= 86.59,
                               total_salary=total_salaries ,ot_request = ot_reqs ,ot_request_time = ot_reqs_val,
                               ot_approved = ot_reqs , ot_approved_time = ot_reqs_val)

            if picks == 'true':
                return redirect('calendars')
            elif picks == 'false':
                return redirect('attendance')

    return render(request, "calendars_update.html", {'date_of_update':date_of_update,
             'login_of_update':login_of_update,
             'logout_of_update': logout_of_update,
             'select_date': select_date,
             'names_users':names_users,
             'return_back':return_back,
             })


def calendars(request):
    print('calendars')
    request.session['back_return'] = 'calendars_back'
    choose_profile = Profile.objects.all()
    get_user_names = request.session.get('get_names')
    # print('get request usernames ', get_user_names)
    if get_user_names  == 'None' or get_user_names == None:
        if str(request.user) == 'AnonymousUser':
            messages.success(request, ('User is not Login'))
            return redirect('home')
        else:
            get_user_names = request.user
    # print('get request usernames ', get_user_names)
    for names in choose_profile:
        if str(names.user) == str(get_user_names):
            names_users = str(names.first_name) +' '+ str(names.last_name)
    if request.method == 'POST':
        butadd = request.POST.get('add')
        butminus = request.POST.get('minus')
        buttoday = request.POST.get('today')
        get_req_date = request.session.get('dates')
        get_req_date = get_req_date.split()
        get_user_name = request.POST.get('username')

        context = [butadd ,butminus ,buttoday]
        # print('get request usernameeeeeeee ', get_user_name)
        if str(get_user_name) != 'None':
            # print('get request username get posttttttttttttttttt', get_user_name)
            request.session['get_names'] = get_user_name
            get_user_names = get_user_name
            return redirect('calendars')

        if 'minus' in context or 'add' in context or 'today' in context:
            pass
            # print('button add, minus, today ', butadd, butminus, buttoday)
        else:
            # print('button add, minus, today ', butadd, butminus, buttoday)
            return redirect('calendars')

        if butadd == 'add':
            temp_month = int(get_req_date[1])- 1
            temp_year = int(get_req_date[0])
            if temp_month == 0:
                temp_month = 12
                temp_year = int(get_req_date[0]) - 1
            start_date = date(temp_year,  temp_month, 1)

            temporary_date_today = datetime.now()
            temps = temporary_date_today.strftime('%Y %m')
            temps =temps.split()
            if int(temps[0]) == temp_year and int(temps[1]) == temp_month:
                month_days = temporary_date_today.strftime('%d')
            else:
                month_days = 1

        elif butminus == 'minus':
            temp_month = int(get_req_date[1]) + 1
            temp_year = int(get_req_date[0])
            if temp_month == 13:
                temp_month = 1
                temp_year = int(get_req_date[0]) + 1
            start_date = date(temp_year, temp_month, 1)

            temporary_date_today = datetime.now()
            temps = temporary_date_today.strftime('%Y %m')
            temps = temps.split()
            if int(temps[0]) == temp_year and int(temps[1]) == temp_month:
                month_days = temporary_date_today.strftime('%d')
            else:
                month_days = 1

        elif buttoday == 'today':
            start_date = datetime.now()
            month_days = start_date.strftime('%d')
            start_date = date(int(start_date.strftime('%Y')), int(start_date.strftime('%m')), 1)

        month = start_date.strftime('%b %Y')
        whole_date = start_date.strftime('%Y %m %d')
        get_days = monthrange(int(start_date.strftime('%Y')), int(start_date.strftime('%m')))

        temp_month_minus = int(start_date.strftime('%m')) - 1
        temp_year_minus = int(start_date.strftime('%Y'))
        if temp_month_minus == 0:
            temp_month_minus = 12
            temp_year_minus = int(start_date.strftime('%Y')) - 1

        get_days_minus = monthrange(temp_year_minus, temp_month_minus)
        start_dates_days_letter = int(start_date.strftime("%w")) + 1
        request.session['dates'] = whole_date
        no_days = []
        dic_cal_days = {}
        dic_cal_present_days = ''
        attend = {}

        total_hours_5 = 0
        total_salary_5 = 0
        total_hours_20 = 0
        total_salary_20 = 0
        total_rates = 0
        user_pays = {}

        ot_hrs_5 = 0
        ot_hrs_20 = 0
        total_hours_5 = 0
        total_hrs_20 = 0
        ot_total_hrs_5 = 0
        ot_total_hrs_20 = 0

        # get_month_attend = 4
        get_month_attend = int(start_date.strftime('%m'))
        get_year_attend = int(start_date.strftime('%Y'))
        attend = get_attendance_payroll(get_month_attend ,get_user_names ,get_year_attend)

        for x in range(1, int(get_days[1]) + 1):
            no_days.append(x)
        temp_total = int(get_days[1]) + int(start_dates_days_letter)
        num = 0
        nums = 1
        temps_nums = 0
        temps = int(get_days_minus[1]) - int(start_dates_days_letter) + 2
        for x in range(1, 43):
            loop = 'false'
            if int(start_dates_days_letter) > x:
                dic_cal_days[str('cal') + str(x)] = temps
                temps += 1

            elif x >= int(start_dates_days_letter) and x <= temp_total - 1:
                if len(attend) == 0:
                    pass
                elif attend[num].log_in.strftime('%a') != 'Sun':
                    for y in range(0 ,len(attend)):
                        if no_days[num] == int(attend[y].log_in.strftime('%d')):
                            # print('number of days ', no_days[num], int(attend[y].log_in.strftime('%d')))

                            get_attend = str(attend[y].log_in.strftime('%Y-%m-%d')) +' '+ str(attend[y].log_in.strftime('%H:%M%p')) +' '\
                            + str(attend[y].log_out.strftime('%H:%M%p')) +' '+ str(attend[y].total_hour) +' '+ str(attend[y].total_rate) +' '+ str(attend[y].total_salary)

                            total_rates = attend[y].total_rate
                            if int(attend[y].log_in.strftime('%d')) >= 5 and int(attend[y].log_in.strftime('%d')) <= 20:
                                format = '%H:%M'
                                temp_login = attend[y].log_in.strftime('%H:%M')
                                temp_logout = attend[y].log_out.strftime('%H:%M')


                                total_hrs = datetime.strptime(temp_logout, format) - datetime.strptime(temp_login, format)

                                if str(temp_logout) < '17:00:00':
                                    total_ot_hr = '00:00:00'
                                else:
                                    total_ot_hr = datetime.strptime(str(temp_logout), format) - datetime.strptime(
                                        '17:00', format)

                                # total_ot_hr = datetime.strptime(temp_logout, format) - datetime.strptime('17:00',
                                #                                                                          format)

                                format = '%H:%M:%S'
                                total_hrs = datetime.strptime(str(total_hrs), format) - datetime.strptime(
                                    str(total_ot_hr), format)

                                # print('total hours ',total_hrs ,temp_login , temp_logout)
                                format = '%H:%M'
                                total_hours = str(total_hrs)
                                date_format = '%H:%M:%S'

                                total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
                                ot_times = total_ot_hr.strftime('%H %M').split()
                                # ot_times = ot_times.split()
                                ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
                                ot_hrs_5 = float(round(ots, 2))

                                # print('y attend ', attend[y].total_hour)

                                total_hours = datetime.strptime(total_hours, date_format)
                                times = total_hours.strftime('%H %M')
                                times = times.split()
                                hour = float(times[0]) + (float(times[1]) / 60)
                                total_hrs_5 = float(round(hour, 2))

                                ot_total_hrs_5 += ot_hrs_5
                                total_hours_5 += total_hrs_5
                                total_salary_5 += 86.59 * total_hrs_5

                            else:
                                format = '%H:%M'
                                temp_login = attend[y].log_in.strftime('%H:%M')
                                temp_logout = attend[y].log_out.strftime('%H:%M')

                                total_hrs = datetime.strptime(temp_logout, format) - datetime.strptime(temp_login, format)

                                if str(temp_logout) < '17:00:00':
                                    total_ot_hr = '00:00:00'
                                else:
                                    total_ot_hr = datetime.strptime(str(temp_logout), format) - datetime.strptime(
                                        '17:00', format)
                                # total_ot_hr = datetime.strptime(temp_logout, format) - datetime.strptime('17:00',format)

                                format = '%H:%M:%S'
                                total_hrs = datetime.strptime(str(total_hrs), format) - datetime.strptime(
                                    str(total_ot_hr), format)

                                format = '%H:%M'
                                total_hours = str(total_hrs)
                                date_format = '%H:%M:%S'

                                total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
                                ot_times = total_ot_hr.strftime('%H %M').split()
                                # ot_times = ot_times.split()
                                ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
                                ot_hrs_20 = float(round(ots, 2))

                                total_hours = datetime.strptime(total_hours, date_format)
                                times = total_hours.strftime('%H %M')
                                times = times.split()
                                hour = float(times[0]) + (float(times[1]) / 60)
                                total_hrs_20 = float(round(hour, 2))

                                ot_total_hrs_20 += ot_hrs_20
                                total_hours_20 += total_hrs_20
                                total_salary_20 += 86.59 * total_hrs_20

                            get_attends =  get_attend.split()
                            dic_cal_days[str('cal')+str(x)] = [no_days[num] ,get_attends[0] , get_attends[1] ,get_attends[2],
                                                               get_attends[3] ,get_attends[4] ,get_attends[5]]
                            loop = 'true'

                if loop == 'false':
                    dic_cal_days[str('cal') + str(x)] = no_days[num]


                if no_days[num] == int(month_days):
                    dic_cal_present_days = str('cal') + str(x)
                num += 1
            else:
                dic_cal_days[str('cal') + str(x)] = nums
                nums += 1

        if len(attend) == 0:
            ot_per_hour = 0
            ot_total_pay_5 = 0
            ot_total_pay_20 = 0
            total_payment_5 = 0
            total_payment_20 = 0
        else:
            ot_per_hour = 65
            ot_total_pay_5 = ot_total_hrs_5 * 65
            ot_total_pay_20 = ot_total_hrs_20 * 65
            total_payment_5 = total_salary_5 + ot_total_pay_5
            total_payment_20 = total_salary_20 + ot_total_pay_20

        iters = 0
        for key, value in dic_cal_days.items():
            if iters % 7 == 0:
                pass
            else:
                if type(value) == int:
                    dic_cal_days[key] = value, 'none'
            iters += 1

        user_pays['rate'] = total_rates
        user_pays['total_hours_5'] = total_hours_5
        user_pays['total_salary_5'] = '{:,.2f}'.format(total_salary_5)
        user_pays['total_hours_20'] = total_hours_20
        user_pays['total_salary_20'] = '{:,.2f}'.format(total_salary_20)

        user_pays['ot_rate'] = ot_per_hour
        user_pays['ot_total_hrs_5'] = ot_total_hrs_5
        user_pays['ot_total_pay_5'] = '{:,.2f}'.format(ot_total_pay_5)
        user_pays['total_payment_5'] = '{:,.2f}'.format(total_payment_5)

        user_pays['ot_total_hrs_20'] = ot_total_hrs_20
        user_pays['ot_total_pay_20'] = '{:,.2f}'.format(ot_total_pay_20)
        user_pays['total_payment_20'] = '{:,.2f}'.format(total_payment_20)

        return render(request, "calendars.html", {'month': month,
              'no_days': no_days,
              'start_dates_days_letter': start_dates_days_letter,
              'dic_cal_days': dic_cal_days,
              'dic_cal_present_days': dic_cal_present_days,
              'attend': attend, 'user_pays': user_pays,
              'choose_profile': choose_profile,
              'names_users':names_users,
              'get_user_names':get_user_names,
              })

    else:
        get_month_attend = int(datetime.now().strftime('%m'))
        usernames = get_user_names
        attend = get_attendance_payroll(get_month_attend, usernames, 2025)

        # attend = Attendance.objects.filter(user_attend = get_user_names).order_by('log_in')
        get_month_attend = 0
        for x in attend:
            get_month_attend = int(x.log_in.strftime('%m'))

        attendee = {}
        year = datetime.now().year
        month = datetime.now().strftime('%b %Y')
        whole_date = datetime.now().strftime('%Y %m %d')
        get_month = datetime.now().strftime('%m')
        get_days = monthrange(year, int(get_month))
        month_day = datetime.now().strftime('%d')
        start_date = date(int(year), int(get_month), 1)
        start_dates_days = start_date.strftime("%d")
        start_dates_days_letter = int(start_date.strftime("%w")) + 1

        request.session['dates'] = whole_date
        get_days_minus = monthrange(year, int(get_month) - 1)
        get_days_add = monthrange(year, int(get_month) + 1)

        no_days = []
        dic_cal_days = {}
        dic_cal_days1 = {}
        dic_cal_present_days = ''
        loop = 'false'
        for x in range(1 ,int(get_days[1]) + 1):
            no_days.append(x)
        temp_total = int(get_days[1]) + int(start_dates_days_letter)
        num = 0
        nums = 1
        temps = int(get_days_minus[1]) - int(start_dates_days_letter) + 2

        total_hours_5 = 0
        total_salary_5 = 0
        total_hours_20 = 0
        total_salary_20 = 0
        total_rates = 0
        user_pays = {}

        ot_hrs_5 = 0
        ot_hrs_20 = 0
        total_hours_5 = 0
        total_hrs_20 = 0
        ot_total_hrs_5 = 0
        ot_total_hrs_20 = 0

        counter = 0
        for x in range(1 ,43):
            loop = 'false'
            if int(start_dates_days_letter) > x:
                dic_cal_days[str('cal') + str(x)] = temps
                # dic_cal_days1[str('cal') + str(x)] = temps
                temps += 1

            elif  x >= int(start_dates_days_letter) and x <= temp_total-1:
                if attend[num].log_in.strftime('%a') != 'Sun':
                    for y in range(0 ,len(attend)):
                        if no_days[num] == int(attend[y].log_in.strftime('%d')):
                            # print('number of days ', no_days[num], int(attend[y].log_in.strftime('%d')))

                            get_attend = str(attend[y].log_in.strftime('%Y-%m-%d')) +' '+ str(attend[y].log_in.strftime('%H:%M%p')) +' '\
                            + str(attend[y].log_out.strftime('%H:%M%p')) +' '+ str(attend[y].total_hour) +' '+ str(attend[y].total_rate) +' '+ str(attend[y].total_salary)

                            total_rates = attend[y].total_rate
                            if float(attend[y].log_in.strftime('%d')) >= 5 and int(attend[y].log_in.strftime('%d')) <= 20:
                                counter += 1

                                # print('number of if y ',y ,counter ,attend[y].log_in)
                                format = '%H:%M'
                                temp_login = attend[y].log_in.strftime('%H:%M')
                                temp_logout = attend[y].log_out.strftime('%H:%M')

                                total_hrs = datetime.strptime(temp_logout, format) - datetime.strptime(temp_login ,format)

                                # print('total hours ',total_hrs)
                                if str(temp_logout) < '17:00:00':
                                    total_ot_hr = '00:00:00'
                                else:
                                    total_ot_hr = datetime.strptime(str(temp_logout), format) - datetime.strptime(
                                        '17:00', format)

                                format = '%H:%M:%S'
                                total_hrs = datetime.strptime(str(total_hrs), format) - datetime.strptime(
                                    str(total_ot_hr), format)

                                # total_ot_hr = datetime.strptime(temp_logout, format) - datetime.strptime('17:00',format)

                                # print('total hours ',total_hrs ,temp_login , temp_logout)
                                format = '%H:%M'
                                total_hours = str(total_hrs)
                                date_format = '%H:%M:%S'

                                total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
                                ot_times = total_ot_hr.strftime('%H %M').split()
                                # ot_times = ot_times.split()
                                ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
                                ot_hrs_5 = float(round(ots, 2))

                                # print('y attend ', attend[y].total_hour)

                                total_hours = datetime.strptime(total_hours, date_format)
                                times = total_hours.strftime('%H %M')
                                times = times.split()
                                hour = float(times[0]) + (float(times[1]) / 60)
                                total_hrs_5 = float(round(hour, 2))

                                # print('total hours ', ot_hrs_5 ,total_hrs_5 ,attend[y].log_in ,attend[y].log_out)

                                ot_total_hrs_5 += ot_hrs_5
                                total_hours_5 += total_hrs_5
                                total_salary_5 += float(attend[y].total_rate) * total_hrs_5

                            else:
                                # print('number of else y ', y)
                                format = '%H:%M'
                                temp_login = attend[y].log_in.strftime('%H:%M')
                                temp_logout = attend[y].log_out.strftime('%H:%M')

                                total_hrs = datetime.strptime(temp_logout, format) - datetime.strptime(temp_login, format)

                                if str(temp_logout) < '17:00:00':
                                    total_ot_hr = '00:00:00'
                                else:
                                    total_ot_hr = datetime.strptime(str(temp_logout), format) - datetime.strptime(
                                        '17:00', format)

                                # print('total hours ',total_hrs , total_ot_hr)
                                format = '%H:%M:%S'
                                total_hrs = datetime.strptime(str(total_hrs), format) - datetime.strptime(str(total_ot_hr), format)
                                # total_ot_hr = datetime.strptime(temp_logout, format) - datetime.strptime('17:00',
                                #                                                                          format)

                                format = '%H:%M'
                                total_hours = str(total_hrs)
                                date_format = '%H:%M:%S'

                                total_ot_hr = datetime.strptime(str(total_ot_hr), date_format)
                                ot_times = total_ot_hr.strftime('%H %M').split()
                                # ot_times = ot_times.split()
                                ots = float(ot_times[0]) + (float(ot_times[1]) / 60)
                                ot_hrs_20 = float(round(ots, 2))

                                total_hours = datetime.strptime(total_hours, date_format)
                                times = total_hours.strftime('%H %M')
                                times = times.split()
                                hour = float(times[0]) + (float(times[1]) / 60)
                                total_hrs_20 = float(round(hour, 2))

                                ot_total_hrs_20 += ot_hrs_20
                                total_hours_20 += total_hrs_20
                                total_salary_20 += float(attend[y].total_rate) * total_hrs_20

                            get_attends =  get_attend.split()
                            dic_cal_days[str('cal')+str(x)] = [no_days[num] ,get_attends[0] , get_attends[1] ,get_attends[2],
                                                               get_attends[3] ,get_attends[4] ,get_attends[5]]
                            loop = 'true'

                if loop == 'false':
                    dic_cal_days[str('cal') + str(x)] = no_days[num]

                if no_days[num] == int(month_day):
                    dic_cal_present_days = str('cal') + str(x)

                num += 1
            else:
                # 29 - 38
                dic_cal_days[str('cal') + str(x)] = nums
                # dic_cal_days1[str('cal') + str(x)] = nums
                nums += 1

        ot_per_hour = 65
        ot_total_pay_5 = ot_total_hrs_5 * 65
        ot_total_pay_20 = ot_total_hrs_20 * 65
        total_payment_5 = total_salary_5 + ot_total_pay_5
        total_payment_20 = total_salary_20 + ot_total_pay_20

        user_pays['rate'] = total_rates
        user_pays['total_hours_5'] = total_hours_5
        user_pays['total_salary_5'] = '{:,.2f}'.format(total_salary_5)
        user_pays['total_hours_20'] = total_hours_20
        user_pays['total_salary_20'] = '{:,.2f}'.format(total_salary_20)

        user_pays['ot_rate'] = ot_per_hour
        user_pays['ot_total_hrs_5'] = ot_total_hrs_5
        user_pays['ot_total_pay_5'] = '{:,.2f}'.format(ot_total_pay_5)
        user_pays['total_payment_5'] = '{:,.2f}'.format(total_payment_5)

        user_pays['ot_total_hrs_20'] = ot_total_hrs_20
        user_pays['ot_total_pay_20'] = '{:,.2f}'.format(ot_total_pay_20)
        user_pays['total_payment_20'] = '{:,.2f}'.format(total_payment_20)

        iters = 0
        for key, value in dic_cal_days.items():
            if iters % 7 == 0:
                pass
            else:
                if type(value) == int:
                    dic_cal_days[key] = value, 'none'
            iters += 1
        # for key, value in dic_cal_days.items():
        #     print('dic cal days items ', key, value)
        return render(request, "calendars.html", {'month': month,
                  'no_days': no_days,
                  'start_dates_days_letter': start_dates_days_letter,
                  'dic_cal_days': dic_cal_days,
                  'dic_cal_present_days': dic_cal_present_days,
                  'attend':attend,'user_pays':user_pays,
                  'choose_profile': choose_profile,
                  'names_users': names_users,
                  'get_user_names': get_user_names,
                  })

def dashone_salary(request ,months ):
    global dash_one_salary
    dash_one_salary = months
    return redirect('dashone')


def dashone_settings(request ,radio_category):
    global radio_cat, radio_val

    print('dashone settings radio value ',radio_val)
    if 'normal' in radio_cat:
        radio_cat.remove('normal')

    if radio_category in radio_cat:
        radio_cat.remove(radio_category)
        # radio_val = radio_val.pop(radio_cat)
    else:
        radio_cat.append(radio_category)
        radio_cat = list(dict.fromkeys(radio_cat))

    # print('radio category ',radio_cat)
    return redirect('dashone')

def dashone_sortuser(request ,sortusers):
    global dash_one
    print('dashone sort username ',sortusers )

    num = Profile.objects.all()
    num = [x for x in num if str(x.user) == sortusers]
    for x in num:
        nums = x.id

    temp_dash = Profile.objects.all()
    querylist1 ,querylist2 = [],[]
    for x in temp_dash:
        if int(x.id) < int(nums):
            querylist1.append(x)
        elif int(x.id) >= int(nums):
            querylist2.append(x)

    dash_one = ''
    dash_one = list(chain(querylist2, querylist1))

    # return render(request, 'dashone_sortuser.html',{})
    return redirect('dashone')

def dashone_sort(request ,pk):
    global name_dash
    print('dashone sort ',pk )

    name_dash = Profile.objects.get(pk=int(pk))
    dash_sort_pk = pk
    request.session['k'] = ['melvin', 'diaz']
    request.session['pk'] = pk

    # print('temp request session ',temp)
    # dash_sort_pk = request.session.get('dash_sort_pk')
    return redirect('dashone')

def get_bodyno_and_todambr(body_no ,toda_mbr):
    print('body number and toda mbr ',body_no ,toda_mbr)
    toda_mbr = str(toda_mbr)
    coords_value =[0,0]
    if int(body_no) <= 1999:
        # print('orange')
        if toda_mbr == '1st St.' :
            # print('1st Street')
            coords_value = [14.8278487,120.2794176]
        elif toda_mbr == '2nd St.':
            # print('2nd Street')
            coords_value = [14.8283286,120.2787579]
        elif toda_mbr == '3rd St.':
            # print('3rd Street')
            coords_value = [14.8294118,120.2781168]
        elif toda_mbr == '4th St.':
            # print('4th Street')
            coords_value = [14.8301511,120.2783971]
        elif toda_mbr == '5th St.':
            # print('5th Street')
            coords_value = [14.8300697,120.2797832]
        elif toda_mbr == '7th St.':
            # print('7th Street')
            coords_value = [14.8310814,120.2798832]
        elif toda_mbr == '9th St. W':
            # print('9th Street' [14.8320392,120.2803409]
            coords_value = [14.8320524,120.2805318]
        elif toda_mbr == '12th St. W':
            # print('12th Street')
            coords_value = [14.8339263,120.2782561]
        elif toda_mbr == '14th Jackson St. W':
            # print('14th Street')
            coords_value = [14.8341755,120.2803013]
        elif toda_mbr == '15th St. W':
            # print('15th Street')
            coords_value = [14.8351714,120.2808954]
        elif toda_mbr == 'Lindayag St.':
            # print('Lin. St. Street')
            coords_value = [14.8269803,120.2815128]

    elif int(body_no) <= 2999:
        # print('green')
        if toda_mbr == '26th St.' :
            # print('26th Street')
            coords_value = [14.8424809,120.2907407]
        elif toda_mbr == '24th St.':
            # print('24th Street')
            coords_value = [14.84266,120.2884174]
        elif toda_mbr == '23rd St. E':
            # print('23rd Street')
            coords_value = [14.8414325,120.2886826]
        elif toda_mbr == '21st St. E':
            # print('21st Street')
            coords_value = [14.8401802,120.2877653]
        elif toda_mbr == '20th St. E':
            # print('20th Street')
            coords_value = [14.8392774,120.2867414]
        elif toda_mbr == '18th St. E':
            # print('18th Street')
            coords_value = [14.8382363,120.2845238]
        elif toda_mbr == '17th St.':
            # print('17th Street')
            coords_value = [14.834941,120.2855051]
        elif toda_mbr == '16th St. E':
            # print('16th Street')
            coords_value = [14.8325848,120.2888607]
        elif toda_mbr == '14th Gate St.':
            # print('14th Gate')
            coords_value = [14.8300864,120.2896592]
        elif toda_mbr == '14th Jackson St. E':
            # print('14th Jack.')
            coords_value = [14.8345485,120.2807166]
        elif toda_mbr == '12th St. E':
            # print('12th St.')
            coords_value = [14.8297353,120.2865505]
        elif toda_mbr == '10th St. E':
            # print('10th St.')
            coords_value = [14.8277456,120.2850651]
        elif toda_mbr == '9th St. E':
            # print('9th St.')
            coords_value = [14.8320038,120.2805258]
        elif toda_mbr == '6th St.':
            # print('6th St.')
            coords_value = [14.8272286,120.2832078]
        elif toda_mbr == 'Katipunan St.':
            # print('Kat St.')
            coords_value = [14.8356548,120.2888747]
        elif toda_mbr == 'Fontaine Ext. St.':
            # print('Fon. Ext.')
            coords_value = [14.8345497,120.2841677]
    elif int(body_no) <= 3999:
        # print('blue')
        if toda_mbr == '18th St. W':
            # print('18th Street')
            coords_value = [14.839375,120.2837634]
        elif toda_mbr == '20th St. W':
            # print('20th Street')
            coords_value = [14.8402758,120.2855973]
        elif toda_mbr == '20th Place St.':
            # print('20th Place')
            coords_value = [14.8405875,120.2857329]
        elif toda_mbr == '21st St. W':
            # print('21st Street')
            coords_value = [14.8409236,120.2855237]
        elif toda_mbr == '22nd St.':
            # print('22nd St.')
            coords_value = [14.8417377,120.2861701]
        elif toda_mbr == '23rd St. W':
            # print('23rd St.')
            coords_value = [14.8433042,120.285571]
        elif toda_mbr == 'Anonas St.':
            # print('Anonas St.')
            coords_value = [14.8391103,120.2832983]
        elif toda_mbr == 'Arthur Tulay St.':
            # print('Arthur St.')
            coords_value = [14.8453992,120.2897216]
        elif toda_mbr == 'Kalaklan St.':
            # print('Kal. Brgy.')
            coords_value = [14.8381888,120.2786147]
        elif toda_mbr == 'Mabayuan St.':
            # print('Mab. Brgy.')
            coords_value = [14.8483267,120.2845778]
        elif toda_mbr == 'Sta Rita St.':
            # print('Sta. Brgy.')
            coords_value = [14.8474538,120.2890142]
        elif toda_mbr == 'Tabacuhan Brgy.':
            # print('Tab. Brgy.')
            coords_value = [14.8546074,120.3027336]
        elif toda_mbr == 'Mactan St.':
            # print('Sebul St.')
            coords_value = [14.8479828,120.2972053]

    return coords_value

def dashone_change_val(request):
    global dash_one, dash_one_salary, name_dash, dash_count
    time.sleep(5)
    # for dash in dash_one:
    #     print('user id ',dash.id)
    # print('lenght user id ', len(dash_one))
    if dash_count == len(dash_one) + 1:
        dash_count = 1

    pks = dash_count
    # pks = random.randrange(1, len(dash_one)+1)
    # dash_one = Profile.objects.all().order_by('zone', 'last_name')

    name_dash = Profile.objects.get(pk=pks)
    request.session['k'] = [name_dash.first_name, name_dash.last_name]
    request.session['pk'] = pks

    # num = Profile.objects.all()
    # num = [x for x in num if str(x.user) == str(name_dash.user)]
    # for x in num:
    #     nums = x.id
    nums = pks
    temp_dash = Profile.objects.all()
    querylist1, querylist2 = [], []
    for x in temp_dash:
        if int(x.id) < int(nums):
            querylist1.append(x)
        elif int(x.id) >= int(nums):
            querylist2.append(x)

    dash_one = ''
    dash_one = list(chain(querylist2, querylist1))

    dash_count += 1
    return redirect('dashone')

def dashone(request):
    global dash_one, name_dash,radio_cat ,radio_val ,dash_one_salary ,dash_count
    print('dashone ')

    # print('dashone ',dash_one)
    # print('name_dash ', name_dash)
    # print('radio cat ', radio_cat)
    # print('radio val ', radio_val)
    print('dash one salary ', dash_one_salary)

    animate_but = request.session.get('animation')

    dash_sort_pk = request.session.get('k')
    dash_sort_pk1 = request.session.get('pk')
    print('dash sort pk ', dash_sort_pk, dash_sort_pk1)
    # if dash_sort_pk1 is not None:
    #     del request.session['pk']
    #     dash_sort_pk1 = request.session.get('pk')
    # print('name dash ',type(name_dash.bodynum) ,name_dash.todaname ,name_dash ,name_dash.user)
    get_coords =  get_bodyno_and_todambr(int(name_dash.bodynum), name_dash.todaname)
    coords = get_coords
    streets = str(name_dash.todaname)
    streets = streets.replace("St.", "")
    streets = ' '.join(streets.split())
    if streets == '18th E':
        streets = streets.replace("E", "")
    # streets = "10 E 24th"
    # coords = [14.8425671,120.2884467]
    # coords = [0,0]
    # print('mapss of google ',coords ,streets)
    radio_cats = ' ,'.join(radio_cat)
    inforec = Addinfo.objects.all()
    infoadd = [x for x in inforec if str(x.user_addinfo) == str(name_dash.user)]

    # print('inforamation add ',infoadd ,name_dash.user)
    infobject = Seminars.objects.all()
    seminarec = [ str(x.seminar_dates) for x in infobject if str(x.id_driver) == str(infoadd[0]) ]
    seminarec.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d') ,reverse=True)
    # print('seminarec ',seminarec)

    total_nametoda = Todaname.objects.all().count()
    print('total name toda ',total_nametoda)
    nametoda = Todaname.objects.filter(todazone= name_dash.zone)
    count_toda = len(nametoda)

    count_zones = Profile.objects.all().count()
    count_per_zones = len([x for x in dash_one if x.zone == name_dash.zone])

    dash_salary_gets = get_attendance_payroll(int(dash_one_salary), str(name_dash.user), int(2025))

    dash_salary_total = {}
    salary_hour  = 0.0
    salary_hours  = 0.0

    salary_rate = 86.59
    ot_total_hour = 0.0
    ot_rate = 65
    for salary in dash_salary_gets:
        if str(salary.log_in.strftime('%a')) != 'Sun':
            if salary.total_hour not in [None, 'None']:
                salary_hour += float(salary.total_hour)
            if salary.ot_approved_time not in [None, 'None']:
                ot_total_hour += float(salary.ot_approved_time.split()[0])
    # print('salary hours ',salary_hour)
    salary_hours = salary_hour - ot_total_hour
    total_salary = salary_hours * salary_rate
    ot_salary = ot_rate * ot_total_hour
    total_payment = total_salary + ot_salary
    print('total payment ',total_payment)
    dash_salary_total['total_hour'] = '{:,.2f}'.format(salary_hours)
    dash_salary_total['total_salary'] = '{:,.2f}'.format(total_salary)
    dash_salary_total['ot_total_hour'] = '{:,.2f}'.format(ot_total_hour)
    dash_salary_total['ot_salary'] = '{:,.2f}'.format(ot_salary)
    dash_salary_total['total_payment'] = '{:,.2f}'.format(total_payment)
    # for key, value in dash_salary_total.items():
    #     print(key ,value)


    if request.method == 'POST':
        # request method radio
        temp_radio_val = {}
        radioid = request.POST.get('radio_id')

        animation = request.POST.get('animate')
        stop_animation = request.POST.get('animate_stop')
        if animation is not None:
            print('animation ',animation)
            request.session['animation'] = True
            animate_but = True

        if stop_animation is not None:
            print('stop animation ',animation)
            request.session['animation'] = False
            animate_but = False

        if radioid is None:
            pass
            # print('radio id is none')
        else:
            radioid = radioid.split()
            # print('radio id request ', radioid)
            temp_radio_val[radioid[0]] = radioid[1]

        radioname = request.POST.get('radio_name')
        if radioname is None:
            pass
            # print('radio name is none')
        else:
            radioname = radioname.split()
            # print('radio name request ', radioname)
            temp_radio_val[radioname[0]] = radioname[1]

        radiobody = request.POST.get('radio_body')
        if radiobody is None:
            pass
            # print('radio body is none')
        else:
            radiobody = radiobody.split()
            # print('radio body request ', radiobody)
            temp_radio_val[radiobody[0]] = radiobody[1]

        radiotoda = request.POST.get('radio_toda')
        if radiotoda is None:
            pass
            # print('radio toda is none')
        else:
            radiotoda = radiotoda.split()
            # print('radio toda request ', radiotoda)
            temp_radio_val[radiotoda[0]] = radiotoda[1]

        radiozone = request.POST.get('radio_zone')
        if radiozone is None:
            pass
            # print('radio zone is none')
        else:
            radiozone = radiozone.split()
            # print('radio zone request ', radiozone)
            temp_radio_val[radiozone[0]] = radiozone[1]

        if 'normal' in radio_cat:
            pass
        else:
            counts = 0
            radio_vals = {}
            # print('radio categoryyyyyyyyyyyyyyyy ', radio_cat, temp_radio_val ,len(temp_radio_val))
            if len(temp_radio_val) != 0:
                for radio in radio_cat:
                    temp = str('-') + str(radio)
                    # print('temporary negative value ',temp)
                    # print('temp radio value in dictionary ', radio_val ,temp_radio_val)
                    # if temp in temp_radio_val.keys():
                    for keys, values in temp_radio_val.items():
                        # keys = [x for x in keys if x.isalpha()]
                        if radio == keys:
                            counts = 1
                            if values == 'ascend':

                                radio_vals[keys] = values
                            else:
                                temps = str('-')+str(keys)
                                radio_vals[temps] = values


            else:
                if len(radio_cat) == 0:
                    radio_cats = ''
                    radio_val = {}
                else:
                    radio_cats = ' ,'.join(radio_val)
                    # print('radio val else ',radio_val)

                    temp = []
                    for x in radio_val.keys():
                        if x.isalpha():
                            # print('radio val keys condition if ', x)
                            temp.append(x)

                        else:
                            # print('radio val keys condition else ', x)
                            x = x.replace("-", "")
                            # tem = [y for y in ' '.join(x) if y.isalpha()]
                            temp.append(x)
                    radio_cat = temp

                    # radio_cat = temps
                    # print('radio cat else ',radio_cat)
                    # print('radio cat temps else ',temp)

            if counts == 1:
                radio_val = {}
                radio_val = radio_vals.copy()
                radio_cats = ' ,'.join(radio_vals.keys())
                # print('radio category value  ',' '.join(radio_vals.keys()) ,radio_vals ,len(radio_vals) )
                name_sort = ['-id', 'last_name']
                dash_one = Profile.objects.all().order_by(list(radio_vals)[0])
                if len(radio_vals) == 1:
                    dash_one = Profile.objects.all().order_by(list(radio_vals)[0])
                elif len(radio_vals) == 2:
                    dash_one = Profile.objects.all().order_by(list(radio_vals)[0] ,list(radio_vals)[1])
                elif len(radio_vals) == 3:
                    dash_one = Profile.objects.all().order_by(list(radio_vals)[0] ,list(radio_vals)[1] ,list(radio_vals)[2])
                elif len(radio_vals) == 4:
                    dash_one = Profile.objects.all().order_by(list(radio_vals)[0] ,list(radio_vals)[1] ,
                                          list(radio_vals)[2] ,list(radio_vals)[3])
                elif len(radio_vals) == 5:
                    dash_one = Profile.objects.all().order_by(list(radio_vals)[0] ,list(radio_vals)[1] ,
                                          list(radio_vals)[2] ,list(radio_vals)[3] ,list(radio_vals)[4])

            # radio_cats = ' ,'.join(radio_val.keys())
            # print('radio value in dictionary ', radio_val)

        get_zones = request.POST.get('zones')
        # print('get zones ',get_zones)
        resets = request.POST.get('reset_name')
        value = request.POST.get('nameid')
        nums = str(value).isdigit()
        strings = str(value).isalnum()
        # print('request post is empty ', value)
        radio_resets = request.POST.get('reset_radio')
        # print('radio resets ',radio_resets)

        if radio_resets == 'reset':
            radio_val = {}
            radio_cat = ['normal']
            radio_cats = ' ,'.join(radio_cat)
            # dash_one = Profile.objects.all().order_by('zone', 'last_name')

        if resets == 'reset':
            dash_count = 2
            # dash_one = Profile.objects.all().order_by('zone','last_name')
            name_dash = Profile.objects.get(pk=1)
            nametoda = Todaname.objects.all().order_by('todazone', 'brgy_name')

            temp_dash = Profile.objects.all()
            querylist1, querylist2 = [], []
            for x in temp_dash:
                if int(x.id) < int(1):
                    querylist1.append(x)
                elif int(x.id) >= int(1):
                    querylist2.append(x)

            dash_one = ''
            dash_one = list(chain(querylist2, querylist1))

            dash_salary_gets = get_attendance_payroll(int(dash_one_salary), str(name_dash.user), int(2025))

            dash_salary_total = {}
            salary_hour = 0.0
            salary_hours = 0.0

            salary_rate = 86.59
            ot_total_hour = 0.0
            ot_rate = 65
            for salary in dash_salary_gets:
                if str(salary.log_in.strftime('%a')) != 'Sun':
                    if salary.total_hour not in [None, 'None']:
                        salary_hour += float(salary.total_hour)
                    if salary.ot_approved_time not in [None, 'None']:
                        ot_total_hour += float(salary.ot_approved_time.split()[0])
            # print('salary hours ',salary_hour)
            salary_hours = salary_hour - ot_total_hour
            total_salary = salary_hours * salary_rate
            ot_salary = ot_rate * ot_total_hour
            total_payment = total_salary + ot_salary
            dash_salary_total['total_hour'] = '{:,.2f}'.format(salary_hours)
            dash_salary_total['total_salary'] = '{:,.2f}'.format(total_salary)
            dash_salary_total['ot_total_hour'] = '{:,.2f}'.format(ot_total_hour)
            dash_salary_total['ot_salary'] = '{:,.2f}'.format(ot_salary)
            dash_salary_total['total_payment'] = '{:,.2f}'.format(total_payment)


        if str(get_zones) in ['All' ,'Zone I' ,'Zone II','Zone III']:
            nametoda = Todaname.objects.all().order_by('todazone', 'brgy_name')
            if str(get_zones) == 'All':
                count_toda = len(nametoda)
            else:
                nametoda = Todaname.objects.filter(todazone=Zone.objects.get(name_zone=get_zones)).order_by('brgy_name')
                count_toda = len(nametoda)


        if not value:
            infoadd = [x for x in inforec if str(x.user_addinfo) == str(name_dash.user)]

            for x in infoadd:
                infoids = x.ID_number
            infobject = Seminars.objects.all()
            seminarec = [str(x.seminar_dates) for x in infobject if str(x.id_driver) == str(infoids)]
            seminarec.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=True)

            count_per_zones = len([x for x in dash_one if x.zone == name_dash.zone])

            return render(request, "dashone.html", {
                'dash_one': dash_one,
                'name_dash': name_dash,
                'nametoda': nametoda,
                'count_toda': count_toda,
                'infoadd': infoadd,
                'radio_cats': radio_cats,
                'seminarec': seminarec,
                'count_zones': count_zones,
                'count_per_zones': count_per_zones,
                'coords': coords,
                'streets':streets,
                'dash_salary_gets': dash_salary_gets,
                'dash_salary_total': dash_salary_total,
                'animate_but': animate_but,
                'total_nametoda': total_nametoda,
            })
            # print('request post is empty ',value)
        else:
            if nums == True:
                print('nums')
                temp_name_dash = Profile.objects.filter(pk=int(value))
                # print('request temp_name_dash', temp_name_dash)

                if not temp_name_dash:
                    # print('request temp_name_dash no value')
                    infoadd = [x for x in inforec if str(x.user_addinfo) == str(name_dash.user)]

                else:
                    # print('request temp_name_dash value', temp_name_dash)
                    name_dash = Profile.objects.get(pk=int(value))
                    infoadd = [x for x in inforec if str(x.user_addinfo) == str(name_dash.user)]


                for x in infoadd:
                    infoids = x.ID_number
                infobject = Seminars.objects.all()
                seminarec = [str(x.seminar_dates) for x in infobject if str(x.id_driver) == str(infoids)]
                seminarec.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'), reverse=True)


            elif strings == True:
                print('strings')
                char = ''
                querylist1 = []
                querylist2 = []
                for x in dash_one:
                    if str(x.user).lower() == value.lower():
                        # print('names: ',x.id)
                        temp = x.id
                        char = Profile.objects.filter(pk=int(temp))

                if not char:
                    pass
                    # print('request post username is empty', char)
                else:
                    # print('request post username is', char)
                    temp_dash = Profile.objects.all()
                    for x in temp_dash:
                        # print('x.id' ,x.id)
                        if int(x.id) < int(temp):
                            querylist1.append(x)
                        elif int(x.id) >= int(temp):
                            querylist2.append(x)
                    # print('querylist2 ',querylist2)
                    # print('querylist1 ', querylist1)
                    dash_one = ''
                    dash_one = list(chain(querylist2, querylist1))
                    # for x in dash_one:
                    #     print(x)
                infoadd = [x for x in inforec if str(x.user_addinfo) == str(name_dash.user)]
            count_per_zones = len([x for x in dash_one if x.zone == name_dash.zone])



    return render(request, "dashone.html", {
        'dash_one':dash_one,
        'name_dash':name_dash,
        'nametoda': nametoda,
        'count_toda':count_toda,
        'infoadd':infoadd,
        'inforec':inforec,
        'radio_cats':radio_cats,
        'seminarec': seminarec,
        'count_zones': count_zones,
        'count_per_zones':count_per_zones,
        'coords':coords,
        'streets':streets,
        'dash_salary_gets': dash_salary_gets,
        'dash_salary_total':dash_salary_total,
        'animate_but': animate_but,
        'total_nametoda': total_nametoda,
    })

def dashtwo(request):
    global ot_number

    print('dash two dash ')
    template = loader.get_template('dashtwo.html')
    context = {
        'ot_number':['1','2']
    }
    ot_number = {'ot_number': ['1', '2']}

    # ot_numbers = {'ot_number': [1]}
    # messages.success(request, ("Request add to notifications"))
    return HttpResponse(template.render(context,request))
    # return render(request, "dashtwo.html", {'context':context})

def dashboard(request):
    return render(request, "dashboard.html", {})

def seq(sequence_order):
    if len(sequence_order) == 1:
        names = Todaname.objects.all().order_by(sequence_order[0])
        seq_orders = " ,".join(sequence_order)
    elif len(sequence_order) == 2:
        names = Todaname.objects.all().order_by(sequence_order[0], sequence_order[1])
        seq_orders = " ,".join(sequence_order)
    elif len(sequence_order) == 3:
        names = Todaname.objects.all().order_by(sequence_order[0], sequence_order[1], sequence_order[2])
        seq_orders = " ,".join(sequence_order)
    elif len(sequence_order) == 4:
        names = Todaname.objects.all().order_by(sequence_order[0], sequence_order[1], sequence_order[2],
                                                sequence_order[3])
        seq_orders = " ,".join(sequence_order)

    return names , seq_orders

def todanames(request, sequence):
    global sequence_order
    entry = 'False'
    # print('sequenceeeeeeeeeeeeeeee ',sequence)
    # print('toda names request', request.POST, request.FILES)
    get_count = request.POST.get('order_count')
    get_toda = request.POST.get('order_toda')
    get_brgy = request.POST.get('order_brgy')
    get_zone = request.POST.get('order_zone')
    get_reset = request.POST.get('reset_name')
    all_files = [get_count ,get_toda ,get_zone ,get_reset]
    # print('get files ',all_files)

    if sequence == 'normal' or sequence == 'random':
        # names = Todaname.objects.all().order_by('todazone', 'brgy_name')
        # sequence_order = ['todazone', 'brgy_name']
        sequence_order = []
        # names = Todaname.objects.all()
        # seq_orders = 'random'


    elif sequence not in sequence_order:
        temp = str('-') + str(sequence)
        if temp in sequence_order:
            if None not in all_files:
                # print('request is not null')
                sequence_order.remove(temp)
                sequence_order.append(sequence)
            else:
                pass
                # print('request is null')
        else:
            sequence_order.append(sequence)

    # elif sequence == 'randoms':
    #     # names = Todaname.objects.all().order_by('todazone', 'brgy_name')
    #     # sequence_order = ['todazone', 'brgy_name']
    #     sequence_order = []
    #     names = Todaname.objects.all().order('?')
    #     seq_orders = 'random'


    # print('len sequence ',len(sequence_order))
    if len(sequence_order) == 0:
        sequence_order = []

        if sequence == 'normal':
            names = Todaname.objects.all()
            seq_orders = 'normal'
        elif sequence == 'random':
            names = Todaname.objects.all().order_by('?')
            seq_orders = 'random'

    elif len(sequence_order) == 1:
        names = Todaname.objects.all().order_by(sequence_order[0])
        seq_orders = " ,".join(sequence_order)
    elif len(sequence_order) == 2:
        names = Todaname.objects.all().order_by(sequence_order[0] ,sequence_order[1])
        seq_orders = " ,".join(sequence_order)
    elif len(sequence_order) == 3:
        names = Todaname.objects.all().order_by(sequence_order[0] ,sequence_order[1], sequence_order[2])
        seq_orders = " ,".join(sequence_order)
    elif len(sequence_order) == 4:
        names = Todaname.objects.all().order_by(sequence_order[0],sequence_order[1],sequence_order[2],sequence_order[3])
        seq_orders = " ,".join(sequence_order)

    # print('toda names request', request.POST, len(request.POST))
    if request.method == 'POST':

        # get_count = request.POST.get('order_count')
        # get_toda = request.POST.get('order_toda')
        # get_brgy = request.POST.get('order_brgy')
        # get_zone = request.POST.get('order_zone')
        # get_reset = request.POST.get('reset_name')

        # if get_toda in ['descend toda']:
        #     print('descending toda order')
        # if get_brgy in ['descend brgy']:
        #     print('descending brgy order')
        # if get_zone in ['descend zone']:
        #     print('descending zone order')
        if seq_orders == 'normal' or seq_orders == 'random':
            pass
        else:

            if get_count in ['descend count']:
                # print('descendinggggggggggggg count order')
                if 'id' in sequence_order:
                    for x in range (0,len(sequence_order)):
                        if sequence_order[x] == 'id':
                            sequence_order[x] = '-id'
                            sequence = '-id'
                entry = 'True'


            elif get_count in ['ascend count']:
                if '-id' in sequence_order:
                    for x in range (0,len(sequence_order)):
                        if sequence_order[x] == '-id':
                            sequence_order[x] = 'id'
                            sequence = 'id'
                entry = 'True'

            if get_brgy in ['descend brgy']:
                if 'brgy_name' in sequence_order:
                    # print('descendinggggggggggggggg brgy order')
                    for x in range(0, len(sequence_order)):
                        if sequence_order[x] == 'brgy_name':
                            sequence_order[x] = '-brgy_name'
                entry = 'True'

            elif get_brgy in ['ascend brgy']:
                if '-brgy_name' in sequence_order:
                    # print('ascendinggggggggggggggg brgy order')
                    for x in range(0, len(sequence_order)):
                        if sequence_order[x] == '-brgy_name':
                            sequence_order[x] = 'brgy_name'
                entry = 'True'


            if get_toda in ['descend toda']:
                if 'name_toda' in sequence_order:
                    # print('descendinggggggggggggggg name toda')
                    for x in range(0, len(sequence_order)):
                        if sequence_order[x] == 'name_toda':
                            sequence_order[x] = '-name_toda'
                entry = 'True'

            elif get_toda in ['ascend toda']:
                if '-name_toda' in sequence_order:
                    # print('ascendinggggggggggggggg name toda')
                    for x in range(0, len(sequence_order)):
                        if sequence_order[x] == '-name_toda':
                            sequence_order[x] = 'name_toda'
                entry = 'True'

            if get_zone in ['descend zone']:
                if 'todazone' in sequence_order:
                    # print('descendinggggggggggggggg name zone')
                    for x in range(0, len(sequence_order)):
                        if sequence_order[x] == 'todazone':
                            sequence_order[x] = '-todazone'
                entry = 'True'

            elif get_zone in ['ascend zone']:
                if '-todazone' in sequence_order:
                    # print('ascendinggggggggggggggg name zone')
                    for x in range(0, len(sequence_order)):
                        if sequence_order[x] == '-todazone':
                            sequence_order[x] = 'todazone'
                entry = 'True'

            if entry == 'True':
                get_values = seq(sequence_order)
                names = get_values[0]
                seq_orders = get_values[1]

        if get_reset == 'reset':

            # sequence_order = []
            # names = Todaname.objects.all().order_by('?')
            seq_orders = 'random'
            # return redirect('profile', user_id=user_id)
            return redirect('todanames' ,sequence='random')


        return render(request, "todanames.html", {'names':names , 'seq_orders':seq_orders})

    else:
        return render(request, "todanames.html", {'names':names, 'seq_orders':seq_orders})

def zone_select(request ,zone_pick):
    global temp_val

    print('zone select', zone_pick)
    # missing_names = Profile.objects.filter((zone=str(zone_pick))
    # print('missing names ',missing_names)

    names = []
    if zone_pick in ['Zone I', 'Zone II', 'Zone III']:
        zonepick = zone_pick.split()
        zone_1_2 = zonepick[0] +' '+zonepick[1]
        zonepick.append('ascend')
        zonepick.append('names')
        temp_val = zone_pick.split()
    else:
        zone_1_2 = temp_val[0] +' '+temp_val[1]
        zonepick = ''
        zonepick = temp_val
        zonepick = zonepick + zone_pick.split()

    print('zone pick ',zonepick)
    if request.user.is_authenticated:
        if zonepick[3] == 'num':
            if zonepick[2] == 'ascend':
                name = Profile.objects.all().order_by('id')
            elif zonepick[2] == 'descend':
                name = Profile.objects.all().order_by('-id')
            elif zonepick[2] == 'random':
                name = Profile.objects.all().order_by('?')

        elif zonepick[3] == 'body':
            if zonepick[2] == 'ascend':
                name = Profile.objects.all().order_by('bodynum')
            elif zonepick[2] == 'descend':
                name = Profile.objects.all().order_by('-bodynum')
            elif zonepick[2] == 'random':
                name = Profile.objects.all().order_by('?')

        elif zonepick[3] == 'names':
            if zonepick[2] == 'ascend':
                name = Profile.objects.all().order_by('last_name')
            elif zonepick[2] == 'descend':
                name = Profile.objects.all().order_by('-last_name')
            elif zonepick[2] == 'random':
                name = Profile.objects.all().order_by('?')

        elif zonepick[3] == 'phone':
            if zonepick[2] == 'ascend':
                name = Profile.objects.all().order_by('phone')
            elif zonepick[2] == 'descend':
                name = Profile.objects.all().order_by('-phone')
            elif zonepick[2] == 'random':
                name = Profile.objects.all().order_by('?')

        elif zonepick[3] == 'mail':
            if zonepick[2] == 'ascend':
                name = Profile.objects.all().order_by('email')
            elif zonepick[2] == 'descend':
                name = Profile.objects.all().order_by('-email')
            elif zonepick[2] == 'random':
                name = Profile.objects.all().order_by('?')

        # elif zonepick[3] == 'zones':
        #     if zonepick[2] == 'ascend':
        #         name = Profile.objects.all().order_by('zone')
        #     elif zonepick[2] == 'descend':
        #         name = Profile.objects.all().order_by('-zone')
        #     elif zonepick[2] == 'random':
        #         name = Profile.objects.all().order_by('?')

        for x in name:
            if str(x.zone) == zone_1_2:
                names.append(x)

        return render(request, "zone_select.html", {'names':names})
    else:

        return render(request, "zone_select.html", {})
def zone_profile(request ,pk):
    # print('pk number ',pk)
    if request.user.is_authenticated:
        names = Profile.objects.filter(id=int(pk))
        # names = Profile.objects.get(id=int(pk))
        for x in names:
            user = str(x.user)
        inforec = Addinfo.objects.all()

        for x in inforec:
            if str(x.user_addinfo) == user:
                inforecord = x.ID_number

        return render(request, "profile.html", {'names':names , 'inforecord':inforecord})
    else:
        return render(request, "zone_profile.html", {})
def zone_view(request ,arrange_order):

    if arrange_order == 'normal':
        names = Profile.objects.all().order_by( 'zone' ,'bodynum','last_name')
    else:
        temps = arrange_order.split()

        if temps[1] == 'num':
            if temps[0] == 'ascend':
                names = Profile.objects.all().order_by('id')
            elif temps[0] == 'descend':
                names = Profile.objects.all().order_by('-id')
            elif temps[0] == 'random':
                names = Profile.objects.all().order_by('?')

        elif temps[1] == 'body':
            if temps[0] == 'ascend':
                names = Profile.objects.all().order_by('bodynum')
            elif temps[0] == 'descend':
                names = Profile.objects.all().order_by('-bodynum')
            elif temps[0] == 'random':
                names = Profile.objects.all().order_by('?')

        elif temps[1] == 'names':
            if temps[0] == 'ascend':
                names = Profile.objects.all().order_by('last_name')
            elif temps[0] == 'descend':
                names = Profile.objects.all().order_by('-last_name')
            elif temps[0] == 'random':
                names = Profile.objects.all().order_by('?')

        elif temps[1] == 'phone':
            if temps[0] == 'ascend':
                names = Profile.objects.all().order_by('phone')
            elif temps[0] == 'descend':
                names = Profile.objects.all().order_by('-phone')
            elif temps[0] == 'random':
                names = Profile.objects.all().order_by('?')

        elif temps[1] == 'mail':
            if temps[0] == 'ascend':
                names = Profile.objects.all().order_by('email')
            elif temps[0] == 'descend':
                names = Profile.objects.all().order_by('-email')
            elif temps[0] == 'random':
                names = Profile.objects.all().order_by('?')

        elif temps[1] == 'zones':
            if temps[0] == 'ascend':
                names = Profile.objects.all().order_by('zone')
            elif temps[0] == 'descend':
                names = Profile.objects.all().order_by('-zone')
            elif temps[0] == 'random':
                names = Profile.objects.all().order_by('?')

    return render(request, 'zone_view.html', {
        'names':names})


def profile_registration(request):
    # if request.user.is_authenticated:
    # forms = ProfileForm()
    form = ProfileRegistrationForm()
    print('form ',form)
    if request.method == 'POST':
        form = ProfileRegistrationForm(request.POST or None, request.FILES)
        # form = ProfileRegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Profile Registered'))
            return render(request, 'profile_registration.html', {'form': form})
        else:
            return render(request, 'profile_registration.html', {'form': form})

    else:
        return render(request, 'profile_registration.html', {'form':form})


def update(request):
    if request.user.is_authenticated:
        names = Profile.objects.filter(user=request.user)
        if names.exists():
            for x in names:
                names = x
            temp = names.image
            form = ProfileForm(request.POST or None, instance=names)
        else:
            return render(request, 'update.html', {})


        if request.method == 'POST':
            # names.image = 'uploads/pictures/vhinz_selfie.png'
            get_pics = request.FILES
            # print('get pics request files ',get_pics, temp)
            if len(get_pics) == 0:
                names.image = temp
            else:
                names.image = get_pics
                for items, values in get_pics.items():
                    names.image = values
            form = ProfileForm(request.POST or None, instance=names)

            if form.is_valid():
                form.save()
                messages.success(request, ('Record Updated'))
                return render(request, 'update.html', {'form': form})
            else:
                return render(request, 'update.html', {'form': form})
        else:
            return render(request, 'update.html', {'form': form})
    else:
        return render(request, 'update.html', {})


def delete(request):
    print('user id ', request.user.id)
    if request.user.is_authenticated:
        names = Profile.objects.filter(user=request.user)
        # names1 = Profile.objects.get(pk=1)
        if names.exists():
            for x in names:
                names = x
            form = ProfileForm(request.POST or None, instance=names)
            if form.is_valid():
                print('delete namesssssssssss ',names)
                names.delete()
                messages.success(request, ('Record Deleted'))
                # return redirect('home')
                return render(request, 'delete.html', {})
            else:
                return render(request, 'delete.html', {'form': form})
        else:
            return render(request, 'delete.html', {})

    else:
        return render(request, 'delete.html', {})

def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password=password)
            login(request ,user)
            messages.success(request, ('Your have registered Successfully!!!'))
            return redirect('home')

        else:
            messages.success(request, ('There was a problem registering, please try again...'))
            return redirect('register')

    return render(request, 'register.html', {'form':form})
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("User error logging-in..."))
            return redirect('login_user')

    else:
        return render(request, 'login_user.html', {})

def logout_user(request):
    logout(request)
    messages.success(request ,('User is Logged out'))
    return redirect('home')

def profile(request):
    if request.user.is_authenticated:
        names = Profile.objects.filter(user=request.user)
        for x in names:
            user = str(x.user)
        inforec = Addinfo.objects.all()
        for x in inforec:
            if str(x.user_addinfo) == user:
                inforecord = x.ID_number


        # pk_names = Profile.objects.get(id=21)
        # print('names ',inforecord)

        return render(request, "profile.html", {'names':names ,
        'inforecord':inforecord})
    else:

        return render(request, "profile.html", {})
def view_information(request):

    return render(request, "view_information.html", {})


def home(request):
    get_logo = Logo.objects.filter(name_logo='gapo_logo')
    if request.method == 'POST':
        firstname = (request.POST['firstname']).capitalize()
        bodynum = request.POST['bodynum']

        names = Profile.objects.filter(first_name=firstname, bodynum=bodynum)
        # print('name', names)

        if len(names) != 0:
            for x in names:
                fullname = x.first_name + ' ' + x.last_name
            # print('fullname ',fullname)
            for x in names:
                user = str(x.user)
            inforec = Addinfo.objects.all()
            for x in inforec:
                if str(x.user_addinfo) == user:
                    inforecord = x.ID_number

            return render(request, "profile.html", {
                'get_logo': get_logo ,
                'names':names,
                'fullname': fullname,
                'inforecord': inforecord,
            })
        else:
            messages.success(request, ('Invalid Entry'))
            return render(request, "home.html", {'get_logo': get_logo})

    else:
        return render(request, "home.html", {'get_logo':get_logo,
                                             })

# notications count
def files(request):
    noti_count = Notifies.objects.filter(is_seen=True).count()
    if str(request.user) == 'AnonymousUser':
        img_name = None
    else:
        img_name = Profile.objects.get(user=str(request.user.id))
    return {'noti_count': noti_count ,'img_name':img_name}
    # return render(request, "files.html", {})

