import data
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def leap_year(year):
    if((year%4==0 and year%100!=0) or year%400==0):
        return 1
    else:
        return 0

def Solar_terms(year,month,day):
    month_const=data.TERM_CONST[month]
    
    if(1900<=year<2000):
        year_const1=month_const[0][0]
        year_const2=month_const[1][0]
        term_date1=int(year_const1 + 0.2422 * (year - 1900) - int((year - 1900)/4))
        term_date2=int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900)/4))
    elif(2000<=year<2100):
        year_const1=month_const[0][1]
        year_const2=month_const[1][1]
        term_date1=int(year_const1 + 0.2422 * (year - 2000) - int((year - 2000)/4))
        term_date2=int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000)/4))
    elif(2100<=2200):
        year_const1=month_const[0][2]
        year_const2=month_const[1][2]
        term_date1=int(year_const1 + 0.2422 * (year - 2100) - int((year - 2100)/4))
        term_date2=int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100)/4))
    
    if(term_date1<=day<term_date2):
        return month_const[0][-1],day-term_date1
    elif(day>=term_date2):
        return month_const[1][-1],day-term_date2
    else:
        if(month==1):
            month_p=12
            month_const=data.TERM_CONST[month_p]
            year_p=year-1
            if(1900<=year_p<2000):
                year_const2=month_const[1][0]
                term_date2=int(year_const2 + 0.2422 * (year_p - 1900) - int((year_p - 1900)/4))
            elif(2000<=year_p<2100):
                year_const2=month_const[1][1]
                term_date2=int(year_const2 + 0.2422 * (year_p - 2000) - int((year_p - 2000)/4))
            elif(2100<=year_p<2200):
                year_const2=month_const[1][2]
                term_date2=int(year_const2 + 0.2422 * (year_p - 2100) - int((year_p - 2100)/4))
            return month_const[1][-1],day+data.MONTH_DAYS[month_p]-term_date2
        elif(month==3):
            month_p=2
            month_const=data.TERM_CONST[month_p]
            if(1900<=year<2000):
                year_const2=month_const[1][0]
                term_date2=int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900)/4))
            elif(2000<=year<2100):
                year_const2=month_const[1][1]
                term_date2=int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000)/4))
            elif(2100<=2200):
                year_const2=month_const[1][2]
                term_date2=int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100)/4))
            
            if(leap_year(year)==1):
                return month_const[1][-1],day+data.MONTH_DAYS[month_p]+1-term_date2
            else:
                return month_const[1][-1],day+data.MONTH_DAYS[month_p]-term_date2
        else:
            month_p=month-1
            month_const=data.TERM_CONST[month_p]
            if(1900<=year<2000):
                year_const2=month_const[1][0]
                term_date2=int(year_const2 + 0.2422 * (year - 1900) - int((year - 1900)/4))
            elif(2000<=year<2100):
                year_const2=month_const[1][1]
                term_date2=int(year_const2 + 0.2422 * (year - 2000) - int((year - 2000)/4))
            elif(2100<=2200):
                year_const2=month_const[1][2]
                term_date2=int(year_const2 + 0.2422 * (year - 2100) - int((year - 2100)/4))
                
            return month_const[1][-1],day+data.MONTH_DAYS[month_p]-term_date2
        
def day_year(year,month,day):
    days=day
    for i in range(1,month):
        days=days+data.MONTH_DAYS[i]
    if(month>2 and leap_year(year)):
        days=days+1
    return days

def day_between_year(year):
    days=0
    for i in range(1900,year):
        if(leap_year(i)):
            days=days+366
        else:
            days=days+365
    return days

def get_jiazi(year, month, day):
    total_days = day_year(year, month, day) + day_between_year(year)
    index = (total_days+10) % 60
    if index == 0:
        index = 60
    return data.jiazi_dict[index]
