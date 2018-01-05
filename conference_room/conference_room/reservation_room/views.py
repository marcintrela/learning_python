from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from reservation_room.models import Room, Reservation
from django.http import HttpResponse
from datetime import date

inputs_for_room = '''<label>Podaj nazwę sali</label><br>
                        <input name="name" type="text"><br>
                        <label>Pojemność</label><br>
                        <input name="capacity" type="number"><br>
                        <input name="projector" type="checkbox">
                        <label>Sala z rzutnikiem</label><br>'''

back_to_main = '<br><a href="/"><h4>Pwrót do strony głównej</h4></a>'


class AllRooms(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        html = ''' <h2>Dostępne sale:</h2>
                            <table>'''
        rooms = Room.objects.all()
        Reservation.objects.all()
        for room in rooms:
            if room.reservation_set.filter(date=date.today()).exists():
                html += '''<tr>
                            <td><a href="/room/{}"><b>{}</b></a></td>
                            <td>ZAJĘTA</td>
                            <td><a href="/modify/{}">Modyfikuj</a></td>
                            <td><a href="/room/delete/{}">Usuń</a></td>
                            </tr>'''.format(room.id, room.name, room.id, room.id)
            else:
                html += '''<tr>
                            <td><a href="/room/{}"><b>{}</b></a></td>
                            <td>WOLNA</td>
                            <td><a href="/modify/{}">Modyfikuj</a></td>
                            <td><a href="/room/delete/{}">Usuń</a></td>
                            </tr>'''.format(room.id, room.name, room.id, room.id)
        html += '</table>'

        html += '<a href="/room/new"><button name="new_room">Dodaj salę</button></a>'
        html += '''
                <form action="/search/" method='get'>
                <h3>Wyszukiwarka sal</h3>
                <label>Podaj datę</label><br>
                <input name="date" type="date"><br>
                <label>Podaj ilość osób</label><br>
                <input name="capacity" type="number"><br>
                <input name="projector" type="checkbox">
                <label>Projektor</label><br>
                <button name="search" type="submit">Szukaj</label>
                </form>
                '''
        return HttpResponse(html)


class Search(View):
    def get(self, request):
        if request.GET.get('date'):
            data = str(request.GET.get('date'))
        else:
            data = str(date.today())
        try:
            capacity = int(request.GET.get('capacity'))
        except ValueError:
            capacity = 0
        print(capacity)
        if request.GET.get('projector'):
            projector = True
        else:
            projector = False
        rooms = Room.objects.filter(projector=projector, capacity__gte=capacity)
        html = '''
                <h2>Dostępne sale:</h2>
                <ul>
                '''
        for room in rooms:
            if not room.reservation_set.filter(date=data).exists():
                if room.projector:
                    html += '<li><a href="/room/{}">{} o pojemności {} z projektorem</a></li>'.format(room.id,
                                                                                                      room.name,
                                                                                                      room.capacity)
                else:
                    html += '<li><a href="/room/{}">{} o pojemności {} bez projektora</a></li>'.format(room.id,
                                                                                                       room.name,
                                                                                                       room.capacity)
        html += back_to_main
        return HttpResponse(html)


class AddRoom(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    html = '''
                <h2>Dodaj salę</h2>
                <form method='POST'>''' + inputs_for_room + \
           '''<button name="submit" type="submit">Dodaj salę</button><br>
                    </form>
                        '''

    def get(self, request):
        return HttpResponse(self.html)

    def post(self, request):
        name = request.POST.get('name')
        try:
            capacity = int(request.POST.get('capacity'))
        except ValueError:
            return HttpResponse('Pojemność sali musi być liczbą <br><a href="/"><h4>Powrót do strony głównej</h4></a>')
        projector = True if request.POST.get('projector') else False
        Room.objects.create(name=name, capacity=capacity, projector=projector)
        return HttpResponse(self.html)

    html += back_to_main


class DeleteRoom(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        room.delete()
        return HttpResponse('Sala została usunięta <br>' + back_to_main)


class ShowRoom(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        if room.projector is True:
            html = '<h2>Sala {} o pojemności {} ma rzutnik</h2>'.format(room.name, room.capacity)
        else:
            html = '<h2>Sala {} o pojemności {} nie ma rzutnika</h2>'.format(room.name, room.capacity)
        html +='''
                <h3>Sala ma następujące rezerwacje:</h3>
                <ul>
                '''
        if len(room.reservation_set.filter(date__gte=date.today()).all()) > 0:
            for r in room.reservation_set.filter(date__gte=date.today()).all():
                html += '<li>Data rezerwacji: {} przez {}. Temat spotkania: <b>"{}"</b></li>'.format(r.date, r.surname, r.description)
        else:
            return HttpResponse('''
                                <h3>Brak rezerwacji</h3>
                                <br><a href="/reservation/{}">Zarezerwuj tą salę</a>'''.format(room.id) + back_to_main)
        html += '''
                </ul>
                <br><a href="/reservation/{}">Zarezerwuj tą salę</a>'''.format(room.id) + back_to_main
        return HttpResponse(html)


class ModifyRoom(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        if room.projector is True:
            html = '<h2>Sala {} o pojemności {} ma rzutnik</h2>'.format(room.name, room.capacity)
        else:
            html = '<h2>Sala {} o pojemności {} nie ma rzutnika</h2>'.format(room.name, room.capacity)
        html += '''
                <br>
                <h3>Modyfikuj dane sali</h3>
                <form method='POST'>''' + inputs_for_room + \
                '''
                <input name="del_projector" type="checkbox">
                <label>Usuń projektor</label><br>
                <button name="submit" type="submit">Aktualizuj dane sali</button>
                </form>'''
        html += back_to_main
        return HttpResponse(html)

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        if request.POST.get('name'):
            name = request.POST.get('name')
            room.name = name
        if request.POST.get('capacity'):
            capacity = request.POST.get('capacity')
            room.capacity = capacity
        if request.POST.get('projector'):
            projector = True
            room.projector = projector
        if request.POST.get('del_projector'):
            projector = False
            room.projector = projector
        room.save()
        return HttpResponse(self.get(request, id))


class ReservationRoom(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    html_reserv = '''
                    <h2>Podaj datę rezerwacji</h2>
                    <form method='POST'>
                    <input name="date" type="date"><br>
                    <label>Nazwisko rezerwującego</label><br>
                    <input name="surname" type="text"><br>
                    <label>Tytuł spotkania</label><br>
                    <input name="description" type="text"><br>
                    <button name="reserv" type="submit">Rezerwuj</button>'''

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        if room.projector is True:
            html = '<h2>Sala {} o pojemności {} ma rzutnik</h2>'.format(room.name, room.capacity)
        else:
            html = '<h2>Sala {} o pojemności {} nie ma rzutnika</h2>'.format(room.name, room.capacity)
        html += '''
                       <h3>Sala ma następujące rezerwacje:</h3>
                       <ul>
                       '''
        if len(room.reservation_set.filter(date__gte=date.today()).all()) > 0:
            for r in room.reservation_set.filter(date__gte=date.today()).all():
                html += '<li>Data rezerwacji: {} przez {}. Temat spotkania: <b>"{}"</b></li>'.format(r.date, r.surname,
                                                                                                     r.description)
            html += '</ul>'
        else:
            return HttpResponse('''<h3>Brak rezerwacji</h3>''' + self.html_reserv + '<br>' + back_to_main)
        html += self.html_reserv + '<br>' + back_to_main

        return HttpResponse(html)

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        busy = room.reservation_set.filter(date__gte=date.today())
        if request.POST.get('date') and request.POST.get('description') and request.POST.get('surname'):
            choosen_date = request.POST.get('date')
            surname = request.POST.get('surname')
            description = request.POST.get('description')
            if choosen_date < str(date.today()):
                html = '''
                        <h2>Podałeś datę z przeszłości<h2>'''
                html += self.html_reserv + back_to_main
                return HttpResponse(html)
            for r in busy:
                if choosen_date == str(r.date):
                    html = '''
                            <h2>W tym terminie sala jest zarezerwowana<h2>'''
                    html += self.html_reserv + back_to_main
                    return HttpResponse(html)
            Reservation.objects.create(surname=surname, description=description, date=choosen_date, room=room)
            return redirect('allRooms')
        else:
            html = '''
                    <h2>Nie wypełniłeś poprawnie formularza<h2>'''
            html += self.html_reserv + back_to_main
            return HttpResponse(html)


