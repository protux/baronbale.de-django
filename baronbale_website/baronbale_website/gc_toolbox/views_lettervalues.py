from django.shortcuts import render

from .forms import LetterValueCalculatorForm
from .tools import lettervalues


def letter_value_calculator(request):
    render_context = dict()

    if request.method == 'POST':
        form = LetterValueCalculatorForm(request.POST)
        render_context['form'] = form
        if form.is_valid():
            result = lettervalues.count(
                form.cleaned_data['message'],
                form.cleaned_data['extra_values'],
                form.cleaned_data['offset'],
                form.cleaned_data['direction'],
                form.cleaned_data['include_numeric']
            )
            result['relevant_values'] = " | ".join(str(value) for value in result['relevant_values'])
            render_context['result'] = result
    else:
        render_context['form'] = LetterValueCalculatorForm()

    return render(request, 'gc_toolbox/letter_value.html', render_context)
