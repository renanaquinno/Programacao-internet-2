"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer
from datetime import date, datetime


@api_view(['GET','POST'])
def game_list(request):
	if request.method == 'GET':
		games = Game.objects.all()
		games_serializer = GameSerializer(games, many=True)
		return Response(games_serializer.data)
	elif request.method == 'POST':

		gamesAll = Game.objects.all()
		for i in gamesAll:
			name = gamesAll[i].data['name']
			if name == request.data['name']:
				return Response("Nome ja existe",status=status.HTTP_400_BAD_REQUEST)
			else: 
				games_serializer = GameSerializer(data=request.data)
				if games_serializer.is_valid():
					games_serializer.save()
					return Response(games_serializer.data, status=status.HTTP_201_CREATED)
		return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'POST', 'DELETE'])
def game_detail(request, pk):
	try:
		game = Game.objects.get(pk=pk)
	except Game.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		games_serializer = GameSerializer(game)
		return Response(games_serializer.data)

	elif request.method == 'PUT':
		games_serializer = GameSerializer(game, data=request.data)		
		if games_serializer.is_valid():
			newName = request.data['name']
			oldName = games_serializer.data['name']
			if newName != oldName:
				games_serializer.save()
			else:
				return Response("Nome não pode ser igual ao antigo")
		return Response(games_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		today = date.today()
		#game.delete()
		games_serializer = GameSerializer(game, data=request.data)		
		if games_serializer.is_valid():
			release_date = games_serializer.data['release_date']
			release_date = datetime.strptime(release_date, '%Y-%m-%d').date() 
			if release_date < today:
				game.delete()
				return Response("Jogo Deletado")
			else: 
				return Response("Não pode deletar jogo ja lançado")
		return Response(release_date)
