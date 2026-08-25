from django.shortcuts import render

# Create your views here.
def categorias(request, club_id):
    # Aquí puedes realizar la lógica para obtener las categorías del club con el ID proporcionado
    # Por ejemplo, podrías consultar la base de datos para obtener las categorías asociadas al club_id

    # Supongamos que tienes un modelo llamado Categoria y quieres obtener todas las categorías del club
    # categorias = Categoria.objects.filter(club_id=club_id)

    # Para este ejemplo, simplemente devolveremos un diccionario vacío como contexto
     
    context = {
        'club_id': club_id,
        # 'categorias': categorias,  # Descomenta esta línea si tienes un modelo Categoria
    }

    return render(request, 'clubes/categorias.html', context)