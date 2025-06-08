from django.db import models
import datetime
from django.contrib.auth.models import User
from datetime import date
from datetime import datetime

class Addinfo(models.Model):
    user_addinfo = models.ForeignKey(User, on_delete=models.CASCADE)
    ID_number = models.CharField(max_length=20,blank=True, null=True)
    ID_issue = models.DateField( blank=True, null=True)
    ID_expired = models.DateField(blank=True, null=True)
    # seminar_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.ID_number


class Seminars(models.Model):
    id_driver = models.ForeignKey(Addinfo, on_delete=models.CASCADE)
    seminar_dates = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Seminars"

    def __str__(self):
        return str(self.seminar_dates)

class Jans_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)
    decoy_vars = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend


    @property
    def decoy_vars(self ):
        # total_salary = 0.00
        if self.log_in != None and self.log_out != None and self.total_hour == 0.00:
            save_data = Jans_2025.objects.get(pk=self.id)
            # print('date time ', type(self.log_out), type(self.log_in.time()) )
            format = '%H:%M:%S'
            login = self.log_in.strftime('%H:%M:%S')
            logout = self.log_out.strftime('%H:%M:%S')
            reg_hour = datetime.strptime(str(logout), format) - datetime.strptime(str(login), format)
            ot_hour = datetime.strptime(str(logout), format) - datetime.strptime('17:00:00', format)


            reg_hour = str(reg_hour).replace(":", " ").split()
            reg_hour = float(reg_hour[0]) + (int(reg_hour[1]) / 60)

            ot_hour = str(ot_hour).replace(":", " ").split()
            ot_hour = float(ot_hour[0]) + (int(ot_hour[1]) / 60)

            save_data.total_rate = 86.59

            total_salary = round((reg_hour - ot_hour)   * save_data.total_rate, 2)
            total_ot_salary = round(ot_hour   * 65 , 2)
            print('hours of work ', reg_hour, ot_hour ,reg_hour - ot_hour ,total_salary)

            save_data.total_hour =  round(reg_hour , 1)
            save_data.total_salary = total_salary + total_ot_salary
            # if save_data.ot_request_time == 0.0:

            if ot_hour == 0.0:
                save_data.ot_request_time = 0.0
                save_data.ot_approved_time = 0.0

                save_data.ot_request = False
                save_data.ot_approved = False

            else:
                if ot_hour <= 1:
                    save_data.ot_request_time = str(ot_hour) + str(' hr')
                    save_data.ot_approved_time = str(ot_hour) + str(' hr')
                else:
                    save_data.ot_request_time = str(ot_hour) + str(' hrs')
                    save_data.ot_approved_time = str(ot_hour) + str(' hrs')

                save_data.ot_request = True
                save_data.ot_approved = True

            # if save_data.ot_approved_time == 0.0:

            save_data.save()
            decoy_vars = None
            return decoy_vars


        # elif self.log_in != None and self.log_out != None and self.total_hour != 0.00:
        #     total_hour = float(self.total_hour)
        #     ot_approved_time = float(self.ot_approved_time.split()[0])
        #     total_rate = float(self.total_rate)
        #     total_salary =  round((total_hour - ot_approved_time)  * total_rate, 2)
        #     # total = total_salaries(self.id)
        #     print('total salary ',total_salary ,self.id)
        #     return decoy_vars


    class Meta:
        verbose_name_plural = 'Jans_2025'

# March 2025
class Attendance(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested',default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend



class Febs_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Febs_2025'

class Aprs_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=1 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Aprs_2025'


class Mays_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Mays_2025'


class Junes_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Junes_2025'


class Julys_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Julys_2025'


class Augs_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Augs_2025'


class Septs_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Septs_2025'

class Octs_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Octs_2025'


class Novs_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Novs_2025'

class Decs_2025(models.Model):
    user_attend = models.CharField(max_length=30,blank=True, null=True)
    log_in = models.DateTimeField(max_length=30,blank=True, null=True)
    log_out = models.TimeField( max_length=30,blank=True, null=True)
    total_hour = models.DecimalField(default=0 , max_digits=7, decimal_places=2 )
    total_rate = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    total_salary = models.DecimalField(default=0 ,max_digits=7, decimal_places=2 )
    ot_request = models.BooleanField('ot_requested', default=False)
    ot_request_time = models.CharField(max_length=30, blank=True, null=True)
    ot_approved = models.BooleanField('ot_approval', default=False)
    ot_approved_time = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user_attend

    class Meta:
        verbose_name_plural = 'Decs_2025'




