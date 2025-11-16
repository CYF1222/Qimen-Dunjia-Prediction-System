import data

def leap_year(year):
    if((year%4==0 and year%100!=0) or year%400==0):
        return 1
    else:
        return 0

def Solar_terms(year,month,date):
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
    
    if(term_date1<=date<term_date2):
        return month_const[0][-1],date-term_date1
    elif(date>=term_date2):
        return month_const[1][-1],date-term_date2
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
            return month_const[1][-1],date+data.MONTH_DAYS[month_p]-term_date2
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
                return month_const[1][-1],date+29-term_date2
            else:
                return month_const[1][-1],date+28-term_date2
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
                
            return month_const[1][-1],date+data.MONTH_DAYS[month_p]-term_date2