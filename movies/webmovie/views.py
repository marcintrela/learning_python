from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from webmovie.models import Person, Role, Movie


# Create your views here.

class Movies(View):
    def get(self, request):
        html = '<h3>W naszej filmotece znajdują się następujące filmy</h3>'
        movies = Movie.objects.order_by('-year')
        html += '<table>'
        for movie in movies:
            html += '''<tr>
                        <td><a href="/movie_details/{}">{} nakręcony w {}, reżyseria {}</a></td>
                        <td><a href="{}/">Edytuj</a></td>
                        <td><a href="del/{}/">Usuń</a></td>
                        </tr>'''.format(movie.id, movie.title, movie.year, movie.director, movie.id, movie.id)
        html += '</table>'
        html += '<a href="add_movie/"><button name="add_movie" type="submit">Dodaj film</button></a>'
        return HttpResponse(html)


class MovieEdit(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        movie = Movie.objects.get(pk=id)
        html = '''
                <h2>Możesz zaktualizować dane filmu</h2>
                <form method='POST'>
                <label>Tytuł filmu</label><br>
                <input name="title" type="text" value="{}"><br>
                <label>Rok ekranizacji</label><br>
                <input name="year" type="number" value="{}"><br>
                <label>Gwiazdki</label><br>
                <input name="ranking" type="number" value="{}"><br>
                <label>Reżyser</label><br>
                <input name="director" type="text" value="{}"><br>
                <label>Scenariusz</label><br>
                <input name="screenplay" type="text" value="{}"><br>
                <button name="apply" type="submit">Aktualizuj</button>
                </form>
                '''.format(movie.title, movie.year, movie.ranking, movie.director.last_name, movie.screenplay.last_name)
        return HttpResponse(html)

    def post(self, request, id):
        movie = Movie.objects.get(pk=id)
        movie.title = request.POST.get('title')
        movie.year = request.POST.get('year')
        movie.ranking = request.POST.get('ranking')
        if request.POST.get('director'):
            try:
                director = Person.objects.filter(last_name__icontains=request.POST.get('director')).get()
                movie.director = director
            except Person.DoesNotExist:
                return HttpResponse("Reżyser - nie ma takiej osoby w bazie")
        if request.POST.get('screenplay'):
            try:
                screenplay = Person.objects.filter(last_name__icontains=request.POST.get('screenplay')).get()
                movie.screenplay = screenplay
            except Person.DoesNotExist:
                return HttpResponse("Scenariusz - nie ma takiej osoby w bazie")
        movie.save()
        return HttpResponse('Dokonano zmiany<br><a href="/movies/"><h4>Pwrót do strony głównej</h4></a>')


class AddMovie(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    html = '''
            <h2>Dodaj film do bazy</h2>
            <form method='POST'>
            <label>Tytuł</label><br>
            <input name="title" type="text"><br>
            <label>Rok ekranizacji</label><br>
            <input name="year" type="number"><br>
            <label>Ranking (0-5)</label><br>
            <input name="ranking" type="number"><br>
            <label>Reżyseria</label><br>
            <input name="director" type="text"><br>
            <label>Scenariusz</label><br>
            <input name="screenplay" type="text"><br>
            <button name="add_movie" type="submit">Zapisz film do bazy</button>
            </form>
            '''
    def get(self, request):
        return HttpResponse(self.html)

    def post(self, request):
        title = request.POST.get('title')
        year = request.POST.get('year')
        ranking = request.POST.get('ranking')
        if request.POST.get('director'):
            try:
                director = Person.objects.filter(last_name__icontains=request.POST.get('director')).get()
            except Person.DoesNotExist:
                return HttpResponse("Reżyser - nie ma takiej osoby w bazie")
        if request.POST.get('screenplay'):
            try:
                screenplay = Person.objects.filter(last_name__icontains=request.POST.get('screenplay')).get()
            except Person.DoesNotExist:
                return HttpResponse("Scenariusz - nie ma takiej osoby w bazie")
        Movie.objects.create(title=title, year=year, ranking=ranking, director=director, screenplay=screenplay)
        return HttpResponse('Film dodany do bazy <br><br><a href="/movies/"><h4>Pwrót do strony głównej</h4></a>')


class MovieDetails(View):
    def get(self, request, id):
        movie = Movie.objects.get(pk=id)
        html = '''<h2>{} nakręcony w {}:</h2>
                    <h3>Reżyseria {}, scenariusz {}</h3>
                    Obsada:<br>
                    <ul>
                '''.format(movie.title, movie.year, movie.director, movie.screenplay)
        for m in movie.role_set.all():
            html += '<li>{} {} jako {}</li>'.format(m.person.first_name, m.person.last_name, m.role)
        html += '</ul>'
        if movie.ranking in (0, 5):
            html += '<h4>Film otrzymał {} gwiazdek</h4>'.format(movie.get_ranking_display())
        elif movie.ranking == 1:
            html += '<h4>Film otrzymał {} gwiazdkę</h4>'.format(movie.get_ranking_display())
        elif movie.ranking in (2, 3, 4):
            html += '<h4>Film otrzymał {} gwiazdki</h4'.format(movie.get_ranking_display())
        return HttpResponse(html)


class DeleteMovie(View):
    def get(self, request, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()
        return HttpResponse('Film usunięto z bazy<br><a href="/movies/"><h4>Pwrót do strony głównej</h4></a>')

class PersonList(View):
    def get(self, request):
        persons = Person.objects.all()
        html = '''
                <h2>Lista osób w bazie</h2>
                <table>
                '''
        for person in persons:
            html += '''
                    <tr>
                        <td>{} {}</td>
                        <td><a href="{}">Edutuj</a></td>
                    </tr>
                    '''.format(person.first_name, person.last_name, person.id)
        html += '</table>'
        html += '<a href="new"><button name="new_person">Dodaj osobę</button></a>'
        return HttpResponse(html)


class PersonAdd(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    html = '''
            <h3>Dodaj osobę do bazy</h3>
            <form method='POST'>
            <label>Imię</label><br>
            <input name="first_name" type="text"><br>
            <label>Nazwisko</label><br>
            <input name="last_name" type="text"><br>
            '''
    movies = Movie.objects.all()
    html += '''
            <input name="played" type="checkbox">
            <label>Film - zaznacz jeśli grał/a w:</label><br>
            <select name="movie_select">
            '''
    for movie in movies:
        html += '<option value="{}">{}</option>'.format(movie.id, movie.title)
    html += '''
            </select>
            <label>jako</label>
            <input name="role" type="text"><br>
            <button name="add_person" type="submit">Dodaj osobę</button>
            </form>'''

    def get(self, request):
        return HttpResponse(self.html)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        new = Person.objects.create(first_name=first_name, last_name=last_name)
        if request.POST.get('played'):
            movie = request.POST.get('movie_select')
            m_tmp = Movie.objects.get(pk=movie)
            role = request.POST.get('role')
            r_tmp = Role(person=new, movie=m_tmp, role=role)
            r_tmp.save()
        return HttpResponse(self.html)

    html += '<br><a href="/person_list/"><h4>Pwrót do listy</h4></a>'


class PersonEdit(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        person = Person.objects.get(pk=id)
        html = '''
                <h2>{} {}</h2>
               <h3>Edytuj dane osobowe</h3>
                <form method='POST'>
                <label>Popraw imię:</label><br>
                <input name="first_name" type="text"><br>
                <label>Popraw nazwisko:</label><br>
                <input name="last_name" type="text"><br>
                <button name="edit" type="submit">Aktualizuj dane</button>
                '''.format(person.first_name, person.last_name)
        html += '<h3>Znany z:</h3><ul>'
        for movie in person.movie_set.all():
            for role in movie.role_set.filter(person=person):
                html += '<li>{} jako {}</li>'.format(movie.title, role.role)
        html += '</ul>'
        movies = Movie.objects.all()
        html += '''
                <input name="played" type="checkbox">
                <label>Dodaj rolę w filmie:</label><br>
                <select name="movie_select">
                '''
        for movie in movies:
            html += '<option value="{}">{}</option>'.format(movie.id, movie.title)
        html += '''
                </select>
                <label>jako</label>
                <input name="role" type="text"><br>
                <button name="add_role" type="submit">Dodaj rolę</button>
                </form>'''

        return HttpResponse(html)

    def post(self, request, id):
        update_person = Person.objects.get(pk=id)
        if request.POST.get('first_name'):
            first_name = request.POST.get('first_name')
            update_person.first_name = first_name
        if request.POST.get('last_name'):
            last_name = request.POST.get('last_name')
            update_person.last_name = last_name
        update_person.save()
        if request.POST.get('played'):
            movie = request.POST.get('movie_select')
            tmp_movie = Movie.objects.get(pk=movie)
            role = request.POST.get('role')
            tmp_role = Role(person=update_person, movie=tmp_movie, role=role)
            tmp_role.save()
        return HttpResponse(self.get(request, id))


