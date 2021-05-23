from django.shortcuts import render

from .forms import DuplicateRemoverForm
from .tools.duplicate_remover import clear_duplicates


def duplicate_remover(request):
    if request.method == "POST":
        form = DuplicateRemoverForm(request.POST)
        if form.is_valid():
            new_items = form.cleaned_data["new_items"]
            old_items = form.cleaned_data["old_items"]
            result = clear_duplicates(new_items, old_items)
            result["duplicate_items"] = ", ".join(result["duplicate_items"])
            result["unique_items"] = ", ".join(result["unique_items"])
            result_context = {"form": form, "result": result}
        else:
            result_context = {"form": DuplicateRemoverForm()}
    else:
        result_context = {"form": DuplicateRemoverForm()}

    return render(request, "toolbox/duplicate_remover.html", result_context)
