from django.shortcuts import render, redirect
from .forms import TypePosteForm
from .models import TypePoste
from accounts.decorators import admin_required


@admin_required
def create_type_poste(request):
    if request.method == "POST":
        form = TypePosteForm(request.POST)
        if form.is_valid():
            # save entry in database
            form.save()
            return redirect('type_poste_list')
    else:
        form = TypePosteForm()

    return render(request, 'types_poste/create.html', {'form': form})

@admin_required
def list_type_poste(request):
    postes = TypePoste.objects.order_by('label')
    print(f"Retrieved {postes.count()} postes from the database.")
    return render(request, 'types_poste/list.html', {'postes': postes})