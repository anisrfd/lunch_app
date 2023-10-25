import logging
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from restaurant_app.exceptions import RestaurantNotFoundException, MenuNotFoundException
from restaurant_app.models import Restaurant, Menu, Employee, Vote
from restaurant_app.serializers import RestaurantSerializer, MenuSerializer, EmployeeSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
def register(request):
    logger.info('POST /register')
    if request.method == 'POST':
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            logger.error('Missing username or password in request data')
            return Response({"message": "Missing username or password"}, status=status.HTTP_400_BAD_REQUEST)
        logger.info(f'Creating a new user {username}')
        User.objects.create_user(username=username, password=password)
        logger.debug(f'Successfully created a new user {username}')
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def restaurant_create(request):
    logger.info('POST /restaurant/create')
    serializer = RestaurantSerializer(data=request.data)
    print("request data", request.data)
    logger.debug(f'Creating a new restaurant {request.data.get("name", "")}')
    if serializer.is_valid():
        serializer.save()
        logger.debug(f'Successfully created restaurant {request.data.get("name")}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.error(f'Failed to create restaurant {request.data.get("name", "")} for reason {serializer.errors}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def menu_upload(request, id):
    logger.info(f'POST /restaurant/{id}/menu/upload')
    try:
        restaurant = _get_restaurant(id)
    except RestaurantNotFoundException:
        return Response({"message": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = MenuSerializer(data=request.data)
    if serializer.is_valid():
        logger.debug(f'Uploading menu for restaurant {id}')
        serializer.validated_data['restaurant'] = restaurant
        serializer.save()
        logger.debug(f'Successfully uploaded menu for restaurant {id}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.error(f'Failed to upload menu for restaurant {id} reason {serializer.errors}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def employee_create(request):
    logger.info('POST /employee/create')
    serializer = EmployeeSerializer(data=request.data)
    logger.info(f'Creating a new restaurant {request.data.get("name", "")}')
    if serializer.is_valid():
        serializer.save()
        logger.debug(f'Successfully created restaurant {request.data.get("name")}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.error(f'Failed to create restaurant {request.data.get("name", "")} for reason {serializer.errors}')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def today_menu(request):
    logger.info('GET /menu/today')
    today_date = date.today()
    logger.debug(f'Fetching menu for date {today_date}')
    menus = Menu.objects.filter(date=today_date)
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vote_for_menu(request, menu_id):
    logger.info(f'POST /menu/{menu_id}/vote')
    try:
        menu = _get_menu(menu_id)
    except MenuNotFoundException:
        return Response({"message": "Menu not found"}, status=status.HTTP_404_NOT_FOUND)
    logger.debug(f'Voting for menu {menu_id} by user {request.user}')
    employee = Employee.objects.get(user=request.user)
    vote = Vote(menu=menu, employee=employee)
    vote.save()
    logger.info(f'Successfully Voted for menu {menu_id} by user {request.user}')
    return Response({"message": "Vote registered"})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_winner(request):
    logger.info('GET /menu/results')
    today = date.today()
    logger.debug(f'Fetching winning restaurant for date {today}')
    previous_winner = _get_previous_winner(today)
    day_before_previous_winner = _get_day_before_previous_winner(today)

    exclude_restaurants = []
    if previous_winner and previous_winner['wins'] >= 3:
        exclude_restaurants.append(previous_winner['restaurant'])
    if day_before_previous_winner and day_before_previous_winner['wins'] >= 3:
        exclude_restaurants.append(day_before_previous_winner['restaurant'])

    today_winner = Menu.objects.filter(date=today).exclude(
        restaurant__in=exclude_restaurants).values('restaurant').annotate(
        wins=Count('restaurant')).order_by('-wins').first()

    winner_name = None
    if today_winner:
        winner_name = Restaurant.objects.get(id=today_winner['restaurant']).name
    logger.debug(f'Successfully fetched winning restaurant for date {today}')
    return Response({"winning_restaurant": winner_name})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logger.info('POST /logout')
    logger.debug(f'Deleting user {request.user.username} token to log out')
    Token.objects.filter(user=request.user).delete()
    logout(request)
    logger.debug(f'successfully deleted user {request.user.username} token to log out')
    return Response({"message": "Logout successful"})


def _get_restaurant(restaurant_id):
    """
    Takes restaurant_id and fetch restaurant information

    :param restaurant_id: string object
    :return: restaurant or raise RestaurantNotFoundException
    """
    logger.debug(f'Fetching restaurant {restaurant_id} information')
    try:
        return Restaurant.objects.get(pk=restaurant_id)
    except Exception as e:
        logger.error(f'Failed to fetch restaurant {restaurant_id} information for reason {e}')
        raise RestaurantNotFoundException


def _get_menu(menu_id):
    """
    Takes menu_id and fetch restaurant menu information

    :param menu_id: string object
    :return: menu or raise MenuNotFoundException
    """
    logger.debug(f'Fetching menu {menu_id} information')
    try:
        return Menu.objects.get(pk=menu_id)
    except Exception as e:
        logger.error(f'Failed to fetch menu {id} for reason {e}')
        raise MenuNotFoundException


def _get_previous_winner(current_date):
    """
    Takes current_date and fetch previous winning restaurant

    :param current_date: date object
    :return: restaurant
    """
    previous_day = current_date - timedelta(days=1)
    return _get_winner_restaurant(previous_day)


def _get_day_before_previous_winner(current_date):
    """
    Takes current_date and fetch day before previous winning restaurant

    :param current_date: date object
    :return: restaurant
    """
    day_before_previous = current_date - timedelta(days=2)
    return _get_winner_restaurant(day_before_previous)


def _get_winner_restaurant(winning_date):
    """
    Takes winning_date and fetch winning restaurant

    :param winning_date: date object
    :return: restaurant
    """
    logger.debug(f'Fetching winning restaurant for date {winning_date}')
    return Menu.objects.filter(date=winning_date).values('restaurant').annotate(
        wins=Count('restaurant')).order_by('-wins').first()
