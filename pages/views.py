from django.shortcuts import render, get_object_or_404, redirect
from .models import ReservedTable, UserReviews, Table
from django.contrib import messages
from menu.models import Food
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
import datetime
import json

valid_table_capacity = valid_table_time = True

def index(request):
    discount_foods = Food.objects.exclude(discount=None).exclude(discount=0)
    reviews = UserReviews.objects.all().order_by('-created_date')
    sum = 0
    if reviews.count():
        for review in reviews:
            sum += review.rate
        average_rating = round(sum/reviews.count(), 1)
    else:
        average_rating = 1
    context = {
        'foods': discount_foods,
        'reviews': reviews,
        'average_rating': average_rating
    }
    return render(request, 'pages/index.html', context)

@login_required
def rate(request):
    if request.method == "POST":
        status = request.POST['review_status']
        user = request.user
        content = request.POST['content']
        user_rate = request.POST['rating']
        if status == 'new':
            new_review = UserReviews.objects.create(user=user, content=content, rate=user_rate)
            new_review.save()
            messages.success(request, 'Your review has been recorded!')
            return redirect('index')
        if status == 'updating':
            review = UserReviews.objects.get(user=user.id)
            review.content = content
            review.rate = user_rate
            review.save(update_fields=['content', 'rate'])
            messages.success(request, 'Review edition succeeded!')
            return redirect('index')

@login_required
def get_tables(request):            
    if request.method == 'POST':
        tables = Table.objects.all()
        context = {}
        table_list = []
        for table in tables:
            table_dic = {}
            table_dic['capacity'] = table.capacity
            table_dic['price'] = table.price_per_duration
            table_dic['id'] = table.id
            table_list.append(table_dic)
        context['tables'] = table_list
        return HttpResponse(json.dumps(context), content_type='applications/json')

@login_required
def check_table(request):
    if request.method == 'POST':
        table = get_object_or_404(Table, pk=request.POST['tableId'])
        context = {}
        reserved_times_list = []
        if not table:
            return Http404()
        is_busy = False
        if table.reserved_times.all():
            is_busy = True
            reserved_times = table.reserved_times.all()
            for t in reserved_times:
                reserved_times_list.append({
                    'start_time': '{0}:{1:02d}'.format(t.start_time.hour, t.start_time.minute),
                    'end_time': '{0}:{1:02d}'.format(t.end_time.hour, t.end_time.minute)
                })
            context = {
                'is_busy': True,
                'time_list': reserved_times_list
            }
            return HttpResponse(json.dumps(context), content_type='applications/json')
        else:
            is_busy = False
            context['is_busy'] = False
            return HttpResponse(json.dumps(context), content_type='applications/json')

@login_required
def check_capacity(request):
    global valid_table_capacity
    valid_table_capacity = True
    if request.method == 'POST':
        id = request.POST['tableId']
        table = get_object_or_404(Table, pk=id)
        if not table:
            return Http404()
        num_of_people = request.POST['numOfPeople']
        message = ''
        error = False
        if int(num_of_people) > table.capacity:
            message = 'Maximum capacity exceeded! Please choose another table!'
            error = True
            valid_table_capacity = False
        context = {
            'error': error,
            'message': message
        }
        return HttpResponse(json.dumps(context), content_type='applications/json')
    
@login_required
def check_res_time(request):
    global valid_table_time
    valid_table_time = True
    if request.method == 'POST':
        id = request.POST['tableId']
        start_time = request.POST['startTime'].split(':')
        end_time = request.POST['endTime'].split(':')
        table = get_object_or_404(Table, pk=id)
        error = False
        message = ''
        if not table:
            return Http404()
        if datetime.timedelta(hours=int(start_time[0]), minutes=int(start_time[1])) -datetime.timedelta(hours=int(end_time[0]), minutes=int(end_time[1])) >= datetime.timedelta(hours=0, minutes=0):
            error = True
            valid_table_time = False
            message = 'Please enter correct time'
            context = {
                'error': error,
                'message': message
            }
            return HttpResponse(json.dumps(context), content_type='applications/json')
        if table.reserved_times.all():
            reserved_times = table.reserved_times.all()
            st = datetime.timedelta(hours=int(start_time[0]), minutes=int(start_time[1]))
            et = datetime.timedelta(hours=int(end_time[0]), minutes=int(end_time[1]))
            for t in reserved_times:
                ts = datetime.timedelta(hours=t.start_time.hour, minutes=t.start_time.minute)
                te = datetime.timedelta(hours=t.end_time.hour, minutes=t.end_time.minute)
                if check_invalidity(st, et, ts ,te):
                    error = True
                    valid_table_time = False
                    message = 'Your time choice is overlapping with someone else\'s!'
                    context = {
                        'error': error,
                        'message': message
                    }
                    return HttpResponse(json.dumps(context), content_type='applications/json')
            else:
                cost = ReservedTable.get_total_price(start_time, end_time, table.duration, table.price_per_duration)
                message = 'The cost is {0}'.format(cost)
                context = {
                    'error': error,
                    'message': message
                }
                return HttpResponse(json.dumps(context), content_type='applications/json')
        else:
            cost = ReservedTable.get_total_price(start_time, end_time, table.duration, table.price_per_duration)
            message = 'The cost is {0}'.format(cost)
            context = {
                'error': error,
                'message': message
            }
            return HttpResponse(json.dumps(context), content_type='applications/json')

def check_invalidity(st, et, ts, te):
    if ts < st < te or ts < et < te or st < ts and et > te:
        return True
    else:
        return False

@login_required
def order_table(request):
    global valid_table_time, valid_table_capacity
    if request.method == 'POST':
        if not valid_table_time or not valid_table_capacity:
            messages.error(request, 'Invalid request!')
            return redirect('index')
        id = request.POST['tableId']
        num_of_people = request.POST['num_of_people']
        st = request.POST['from']
        et = request.POST['to']
        table = get_object_or_404(Table, pk=id)
        if not table:
            return Http404()
        start_time = datetime.datetime.strptime(st, '%H:%M').time()
        end_time = datetime.datetime.strptime(et, '%H:%M').time()
        new_res = ReservedTable.objects.create(table=table, user=request.user, start_time=start_time, end_time=end_time)
        new_res.save()
        messages.success(request, 'Table successfully reserved!')
        return redirect('index')

        
