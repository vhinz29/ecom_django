from django.shortcuts import render, redirect
from information.models import Addinfo, Seminars
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from information.forms import AddinfoForm, SeminarsForm
from information.forms import AddinfoRegistrationForm ,SeminarsRegistrationForm

def info_register(request):
    valid = False
    sem_form = SeminarsRegistrationForm()
    form = AddinfoRegistrationForm()
    # print('form ', form)
    get_forms = request.POST.get('registers')
    get_semforms = request.POST.get('seminars')

    if request.method == 'POST':
        # print('get additional formssssssssssssssssss ', get_forms)
        # print('get seminar formssssssssssssssssss ', get_semforms)
        form = AddinfoRegistrationForm(request.POST or None, request.FILES)
        seminar_form = SeminarsRegistrationForm(request.POST or None, request.FILES)

        if get_forms == 'Information':
            if form.is_valid():
                count = 1
                for x in form:
                    if count == 1:
                        form_username = Addinfo.objects.filter(user_addinfo=int(x.value()))
                        if form_username.exists():
                            messages.success(request, ('Username Already Exist'))
                            return redirect('info_register')
                    count += 1

            form.save()
            valid = True

        if seminar_form.is_valid():
            if get_semforms == 'Seminars':
                seminar_form.save()
                valid = True

        if valid == True:
                messages.success(request, ('Additional Information Registered'))
                return render(request, 'info_register.html', {'form': form,
                                                              'sem_form': sem_form})


        if valid == False:
            return render(request, 'info_register.html', {'form': form,
                                                          'sem_form': sem_form})

    else:
        return render(request, 'info_register.html', {'form': form,
                      'sem_form':sem_form})



def info_delete(request):
    print('information delete')
    # sem_form = SeminarsRegistrationForm()
    # form = AddinfoRegistrationForm()
    valid = False
    temps_add = Addinfo.objects.all().order_by('ID_number')
    temps_sem = Seminars.objects.all().order_by('seminar_dates')
    get_pick_dates = request.session.get('get_infos')

    get_forms = request.POST.get('registers')
    get_semforms = request.POST.get('seminars')

    usernames = None
    users_id = None
    sem_id_number = None
    seminars_info = []
    for add in temps_add:
        if str(add.user_addinfo) == str(request.user):
            usernames = add
            users_id = add.ID_number
        # print('add info ', add, add.user_addinfo, add.id)

    for add in temps_sem:
        if str(add.id_driver) == str(users_id):
            seminars_info.append(add.seminar_dates)
            if str(add.seminar_dates) == str(get_pick_dates):
                sem_id_number = add
                user_id_sem = add.id


    # print('informationnnnnnnnnnnnnnnnnnnnnnnnnnnnnn ', usernames)
    # print('seminarsssssssssssssssssssssssssssssssss ', seminars_info)

    form = AddinfoForm(request.POST or None, instance=usernames)
    sem_form = SeminarsForm(request.POST or None, instance=sem_id_number)
    # print('seminars form ', sem_form)

    if request.user.is_authenticated :
        # form = AddinfoForm(request.POST or None, instance=usernames)
        # sem_form = SeminarsForm(request.POST or None, instance=sem_id_number)

        if request.method == 'POST':
            print('get additional formssssssssssssssssss ', get_forms)
            print('get seminar formssssssssssssssssss ', get_semforms)

            if form.is_valid():
                if get_forms == 'Information':
                    usernames.delete()
                    valid = True
            if sem_form.is_valid():
                if get_semforms == 'Seminars':
                    sem_id_number.delete()
                    valid = True

            if valid == True:
                messages.success(request, ('Record Deleted'))
                return redirect('info_delete')
                # return render(request, 'info_delete.html', {'form': form,
                #                                           'sem_form': sem_form})

            # if valid == False:
            #     return redirect('info_delete')
            #     # return render(request, 'info_delete.html', {'form': form,
            #     #                                               'sem_form': sem_form})
        else:
            return render(request, 'info_delete.html', {
                'form': form,
                'sem_form': sem_form,
                'seminars_info': seminars_info,
                'sem_id_number': sem_id_number,
            })

    else:
        return render(request, 'info_delete.html', {
            'form': form,
            'sem_form': sem_form,
            'seminars_info': seminars_info,
            'sem_id_number': sem_id_number,
                                                 })


def info_date(request ,infos ,picks):
    print('information date ',infos)
    val = request.session['get_infos'] = infos
    selects = request.session['selects'] = picks

    # print('value request session ',val ,selects)
    if selects == 'deletes':
        return redirect('info_delete')
    elif selects == 'updates':
        return redirect('info')


def info(request):
    valid = False
    temps_add = Addinfo.objects.all().order_by('ID_number')
    temps_sem = Seminars.objects.all().order_by('seminar_dates')
    get_pick_dates = request.session.get('get_infos')

    get_forms = request.POST.get('registers')
    get_semforms = request.POST.get('seminars')

    usernames = None
    users_id = None
    sem_id_number = None
    seminars_info = []
    for add in temps_add:
        if str(add.user_addinfo) == str(request.user):
            usernames = add
            users_id = add.ID_number

    for add in temps_sem:
        if str(add.id_driver) == str(users_id):
            seminars_info.append(add.seminar_dates)
            if str(add.seminar_dates) == str(get_pick_dates):
                sem_id_number = add
                user_id_sem = add.id


    form = AddinfoForm(request.POST or None, instance=usernames)
    sem_form = SeminarsForm(request.POST or None, instance=sem_id_number)

    if request.user.is_authenticated:
        # form = AddinfoForm(request.POST or None, instance=usernames)
        # sem_form = SeminarsForm(request.POST or None, instance=sem_id_number)

        if request.method == 'POST':
            print('get additional formssssssssssssssssss ', get_forms)
            print('get seminar formssssssssssssssssss ', get_semforms)

            if form.is_valid():
                if get_forms == 'Information':
                    usernames.save()
                    valid = True
            if sem_form.is_valid():
                if get_semforms == 'Seminars':
                    print('seminarsssssssssssssssssssssssssssssssss')
                    sem_id_number.save()
                    valid = True

            if valid == True:
                messages.success(request, ('Record Updated'))
                return redirect('info')

        else:
            return render(request, 'info.html', {
                'form': form,
                'sem_form': sem_form,
                'seminars_info': seminars_info,
                'sem_id_number': sem_id_number,
            })

    else:
        return render(request, 'info.html', {
            'form': form,
            'sem_form': sem_form,
            'seminars_info': seminars_info,
            'sem_id_number': sem_id_number,
        })
