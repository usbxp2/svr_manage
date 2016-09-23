from django import template
from django.utils.html import format_html
import datetime

register = template.Library()

@register.simple_tag
def page_cut(current_page, loop_page):

    differ = abs(current_page - loop_page)
    if differ < 5:
        li = '''<li class=""><a href="?page=%s">%s<span class="sr-only">(current)</span></a></li>''' % (loop_page, loop_page)
        return format_html(li)
    else:
        #这里一定要返回一个空字符串，否则在前端会显示一系列的None
        return ''

@register.filter
def time_color(exp_date):
    startdate = datetime.datetime.now().date()
    enddate = startdate + datetime.timedelta(30)
    if (enddate - exp_date).days > 0 and (enddate - exp_date).days <= 30:
        td = '''<td class="%s">%s</td>''' % ('exp_date', exp_date)
        return format_html(td)
    elif (enddate - exp_date).days > 30:
        td = '''<td class="outof">%s</td>''' % (exp_date)
        return format_html(td)
    else:
        td = '''<td>%s</td>''' % (exp_date)
        return format_html(td)