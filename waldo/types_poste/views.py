from django.shortcuts import render, redirect
from .forms import TypePosteForm
from accounts.decorators import admin_required


@admin_required
def create_type_poste(request):
    if request.method == "POST":
        form = TypePosteForm(request.POST)
        if form.is_valid():
            # save entry in database
            form.save()
            return redirect('type_poste_create')
    else:
        form = TypePosteForm()

    return render(request, 'types_poste/create.html', {'form': form})
