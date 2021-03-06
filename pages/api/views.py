from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import get_object_or_404
import datetime
from django.contrib.auth import get_user_model
from pages.models import UserReviews, Table, ReservedTable, OrderHistory, Bonus, UserBonus
from menu.models import Food
from accounts.models import CustomUser
from .serializers import ReviewSerializer, TableSerializer, ReservedTableSerializer

@api_view(['GET'])
def review_list(request):
    if request.method == 'GET':
        reviews = UserReviews.objects.all()        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class UserReview(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        if UserReviews.objects.filter(user=request.user).exists():
            review = UserReviews.objects.get(user=request.user)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(None)

    def post(self, request, *args, **kwargs):
        review, created = UserReviews.objects.get_or_create(user=request.user, content=request.data['content'], created_date=request.data['created_date'], rate=request.data['rate'])
        if created:
            serializer = ReviewSerializer(review)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        review = UserReviews.objects.get(user=request.user)
        review.content = request.data['content']
        review.created_date = request.data['created_date']
        review.rate = request.data['rate']
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

@api_view(['POST'])
def contact(request):
    if request.method == 'POST':
        subject = request.data['subject']
        email = request.data['email']
        message = request.data['message']
        if email and message:
            try:
                send_mail(
                    subject, 
                    'From: {0}\n{1}'.format(email, message), 
                    email, 
                    ['fantasyrestaurantt@gmail.com'],
                    fail_silently=False
                    )
                return Response({'message': 'Success!'}, status=status.HTTP_200_OK)
            except BadHeaderError:
                return Response({'message': 'Invalid Header found!'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'message': 'Something went wrong in the server:( Try again!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def table_list(request):
    if request.method == 'GET':
        tables = Table.objects.all().order_by('id')
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)
        
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def check_table(request, pk):
    if request.method == 'GET':
        table = Table.objects.get(pk=pk)
        reserved_list = table.reserved_times.all()
        serializer = ReservedTableSerializer(reserved_list, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def get_user_tables(request):
    if request.method == 'GET':
        tables = request.user.reserved_tables.all()
        serializer = ReservedTableSerializer(tables, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def order_table(request):
    if request.method == 'POST':
        table_id = request.data['tableId']
        num_of_people = int(request.data['num_of_people'])
        start_time = request.data['start_time']
        end_time = request.data['end_time']
        is_valid, err_mess = validate(table_id, num_of_people, start_time.split(':'), end_time.split(':'))
        if not is_valid:
            err_mess['is_valid'] = False
            return Response(err_mess)
        else:
            table = Table.objects.get(pk=table_id)
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
            end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
            new_res = ReservedTable.objects.create(table=table, user=request.user, start_time=start_time, end_time=end_time)
            new_res.save()
            serializer = ReservedTableSerializer(new_res)
            return Response({'is_valid': True, 'table': serializer.data}, status=status.HTTP_201_CREATED)

def validate(id, nom, st, et):
    is_valid = True
    err_mess = {
        'num_of_people_err': '',
        'time_err': ''
    }
    table = Table.objects.get(pk=id)
    if nom > table.capacity:
        is_valid = False
        err_mess['num_of_people_err'] = 'Maximum capacity exceeded!'
    if datetime.timedelta(hours=int(st[0]), minutes=int(st[1])) - datetime.timedelta(hours=int(et[0]), minutes=int(et[1])) >= datetime.timedelta(hours=0, minutes=0):
        is_valid = False
        err_mess['time_err'] = "Please enter correct time!"
    if table.reserved_times.all():
        reserved_times = table.reserved_times.all()
        st_time = datetime.timedelta(hours=int(st[0]), minutes=int(st[1]))
        et_time = datetime.timedelta(hours=int(et[0]), minutes=int(et[1]))
        for t in reserved_times:
            ts_time = datetime.timedelta(hours=t.start_time.hour, minutes=t.start_time.minute)
            te_time = datetime.timedelta(hours=t.end_time.hour, minutes=t.end_time.minute)
            if check_invalidity(st_time, et_time, ts_time, te_time):
                is_valid = False
                err_mess['time_err'] = err_mess['time_err'] + ' ' + 'Your time choice is overlapping with someone else\'s!'
    return (is_valid, err_mess)


def check_invalidity(st, et, ts, te):
    if ts < st < te or ts < et < te or st < ts and et > te:
        return True
    else:
        return False

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated,])
def order(request):
    if request.method == 'POST':
        new_order = OrderHistory.objects.create(user=request.user, 
                                                items_list=request.data['item_list'],
                                                items_quantity_list=request.data['quantity_list'],
                                                price=request.data['price'],
                                                delivery_fee=request.data['delivery_fee'])
        new_order.save()
        total_expense = 0
        for order in request.user.orders.all():
            total_expense += order.price
        for bonus in Bonus.objects.all().order_by('-value'):
            if total_expense >= bonus.threshold:
                user_bonus = request.user.user_bonus
                user_bonus.bonus = bonus
                user_bonus.save()
                break
        order_item = {
            'id': new_order.id,
            'totalCost': int(new_order.price) + int(new_order.delivery_fee),
            'created_date': new_order.created_date
        }
        item_list = []
        counter = 0
        for id in new_order.get_item_list():
            food = Food.objects.get(pk=id)
            i_dic = {
                'id': counter,
                'name': food.name,
                'quantity': new_order.get_quantity_list()[counter],
                'price': food.price
            }
            item_list.append(i_dic)
            counter += 1
        order_item['items'] = item_list
        return Response(data=order_item, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def get_user_orders(request):
    if request.method == 'GET':
        orders = request.user.orders.all()
        order_list = []
        if orders:
            order_counter = 0
            for order in orders:
                o_dic = {
                    'id': order_counter,
                    'totalCost': order.price + order.delivery_fee,
                    'created_date': order.created_date,
                }
                item_list = []
                counter = 0
                for id in order.get_item_list():
                    food = Food.objects.get(pk=id)
                    i_dic = {
                        'id': counter,
                        'name': food.name,
                        'quantity': order.get_quantity_list()[counter],
                        'price': food.price
                    }
                    item_list.append(i_dic)
                    counter += 1
                o_dic['items'] = item_list
                order_list.append(o_dic)
                order_counter += 1
        return Response(order_list)
