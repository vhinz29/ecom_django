from django.test import TestCase
from datetime import time
from datetime import datetime
from datetime import timedelta
from datetime import date
from calendar import monthrange
import random


# Create your tests here.
import string
txt = "-CompanyX-"
keys = [x for x in txt if x.isalpha()]

print(keys)
sample = {'-id': 'descend', '-last_name': 'descend'}
print('sample dictionary ',str(list(sample)[1]) ,list(sample.keys())[1])
print('sample dictionary keys ',sample.keys())
if '-id' not in sample.keys():
    print('sample keys in',sample.keys())
else:
    print('sample keys  in', sample.keys())

streets = '24th St. E'
streets = streets.replace("St.", "")
# streets = streets.split()
streets =' '.join(streets.split())
print('streets ',streets)

date_today = datetime.now()
print('date today ',date_today)
timed = datetime.strptime('03:55', '%H:%M').time()
times = timed.strftime('%H:%M')

print('timed ',times)

date_format = '%Y-%m-%d %H:%M'
time_login = datetime.strptime('2023-02-28 14:30', date_format)
time_login = time_login.strftime('%Y-%m-%d %H:%M')
print(time_login)




d = datetime.today() - timedelta(hours=0, minutes=50)

times = d.strftime('%H %M')
times = times.split()
print('time ',times)
print('time ',times)
hour = float(times[0]) + (float(times[1]) / 60)
hour = float(round(hour, 2))
print('hours ',hour)


nums_time = '03:55'
nums_time = nums_time.replace(":", " ")

nums_time = nums_time.split()
print('time ',nums_time[0] ,nums_time[1])

# log_in = models.DateTimeField(max_length=20,blank=True, null=True) = '2025-03-03 08:00'
# log_out = models.DateField( blank=True, null= = '17:00'

attendance = [['defensived' ,'2025-03-03 08:00' ,'18:00'],
['hardworks' ,'2025-03-03 08:00' ,'18:00'],
['shielded' ,'2025-03-03 08:00' ,'18:00'],
['affairs' ,'2025-03-03 08:00' ,'17:00'],
['delicious' ,'2025-03-03 08:00' ,'17:00'],
['fulloves' ,'2025-03-03 08:00' ,'17:00'],
['heartys' ,'2025-03-03 08:00' ,'17:00'],
['romances' ,'2025-03-03 08:00' ,'17:00'],
['secretlove' ,'2025-03-03 08:00' ,'18:00'],
['strongman','2025-03-03 08:00' ,'18:00']]

for x in attendance:
    print(x)

lists ={'1':[1,2,3,4,5] ,'2':[1,5]}
for key ,value in lists.items():
    print(key ,value[0:2])


hexString = hex(10005)

print('hex string ',hexString)
nums = 'Melvin'
nums1 = 'Melvins'

print('names ',[nums] + [nums1])




date_now = datetime.now()
dates = date_now.strftime('%Y-%m-%d')
month = int(date_now.strftime('%m'))
day = int(date_now.strftime('%d'))
month_range = monthrange(2025, int(month))
loop = day
print('month and day ',month ,day)
date_pick = date( 2025, int(month), int(day))

print('month range ',month_range ,date_pick)
loop_range = loop + 27
new_loop = 1
while loop <= loop_range :
    if loop <= month_range[1]:
        date_pick = date(2025, int(month), int(loop))
        print('date pick', date_pick.strftime('%Y-%m-%d'))
    else:
        date_pick = date(2025, int(month+1), int(new_loop))
        new_loop += 1

    loop += 1

value = '17:00:00'
if value < '':
    print('value is less than')
else:
    print('value is greater than')


record = {'affairs': '19:00', 'defensived': '18:00', 'delicious': '18:30', 'fulloves': '17:30',
         'hardworks': '18:00', 'heartys': '18:00', 'romances': '18:00', 'secretlove': '18:00',
                 'shielded': '18:00','strongman': '18:00'}

print(record)
records = {}
for key, value in record.items():
    if value == '18:00':
        records[key] = value

print(records)

pks = random.randrange(1, 10)
print('pk number ',pks)
key_value = 'afdsgjlrTY4578910286IOITPGmdjtuy607'
print('key value ',len(key_value))

find = 0
list_key = list(key_value)
print('list key ',list_key)
get_key = ''
while find <= len(key_value)-1:
    for num in range(48, 123):
        # if num >= 58 and num <= 64:
        #     pass
        # elif num >=91 and num <= 96:
        #     pass
        # else:

        if list_key[find] == chr(num):
            print('nums ',find, chr(num))

            get_key += chr(num)
            find += 1
            break


print('list key ',list_key)
print('get key  ',list(get_key))
if key_value == get_key:
    print('The password is Melvin G. Diaz')


