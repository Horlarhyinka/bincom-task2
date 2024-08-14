from django.shortcuts import render, redirect
from core.models import AnnouncedPUResults, PollingUnit
from django.db import models
from core.forms import ResultsForm


def results_table(request):
    results = AnnouncedPUResults.objects.filter(polling_unit_uniqueid=8)  # Query and limit the results
    return render(request, 'results_table.html', {'results': results})


def results_by_lga(request):
    lga_id = request.GET.get('lga_id') 
    total_score = 0
    if lga_id:
        polling_units = PollingUnit.objects.filter(lga_id=lga_id)
        unit_ids = polling_units.values_list('uniqueid', flat=True)
        results = AnnouncedPUResults.objects.filter(polling_unit_uniqueid__in=unit_ids)
        total_score = results.aggregate(total_score=models.Sum('party_score'))['total_score'] or 0

    lgas = PollingUnit.objects.values('lga_id').distinct()
    return render(request, 'results_by_lga.html', {'total_score': total_score, 'lgas': lgas})



def store_results(request):
    if request.method == 'POST':
        polling_units = PollingUnit.objects.all()
        polling_units_choices = [(unit.uniqueid, unit.polling_unit_name) for unit in polling_units]
        form = ResultsForm(request.POST, polling_units_choices=polling_units_choices)

        # Check if the form is valid
        if form.is_valid():
            print("Form is valid...")
            form.save()
            return redirect('store_results')  # Redirect to avoid resubmission
        else:
            print("Form is invalid...")
    else:
        # Handle GET request
        polling_units = PollingUnit.objects.all()
        polling_units_choices = [(unit.uniqueid, unit.polling_unit_name) for unit in polling_units]
        form = ResultsForm(polling_units_choices=polling_units_choices)

    return render(request, 'store_results.html', {'form': form})