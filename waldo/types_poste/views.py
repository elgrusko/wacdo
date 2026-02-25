from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.deletion import ProtectedError
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

@admin_required
def edit_type_poste(request, poste_id):
    poste = get_object_or_404(TypePoste, pk=poste_id)
    if request.method == "POST":
        # 'instance' is used to tell the form that we want to update the existing poste instead of creating a new one
        form = TypePosteForm(request.POST, instance=poste)
        if form.is_valid():
            form.save()
            return redirect('type_poste_list')
    else:
        # 'instance' is used to pre-populate the form with the existing data of the poste we want to edit
        form = TypePosteForm(instance=poste)

    return render(request, 'types_poste/edit.html', {'form': form, 'poste': poste})


@admin_required
def delete_type_poste(request, poste_id):
    poste = get_object_or_404(TypePoste, pk=poste_id)

    if request.method != "POST":
        return redirect("type_poste_edit", poste_id=poste.id)

    # try to delete the poste. If it is still referenced by an affectation, a ProtectedError will be raised
    try:
        poste.delete()
        return redirect("type_poste_list")
    except ProtectedError:
        form = TypePosteForm(instance=poste)
        delete_error = (
            f'Impossible de supprimer "{poste.label}" : '
            f"ce type de poste est encore utilisé dans {poste.affectations.count()} affectation(s)."
        )
        return render(
            request,
            "types_poste/edit.html",
            {
                "form": form,
                "poste": poste,
                "delete_error": delete_error,
            },
        )
