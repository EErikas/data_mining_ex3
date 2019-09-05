from django.shortcuts import render
from django.contrib import messages
from .forms import UploadForm, IdCarverForm
from .algorithms.decision_tree import DecisionTree
from .algorithms.id_code_detection import text_sanitizer, get_company_data, get_personal_description, id_checker


def view_decision_tree(request):
    context = {
        'title': 'Upload Data File',
        'form': UploadForm()
    }
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dt = DecisionTree(request.FILES['docfile'])
                dt.set_classifier_column(request.POST['selector'])
                image = dt.create_decision_tree(criterion=request.POST['criterion'],
                                                splitter=request.POST['splitter'])
                context = {'title': 'Decision Tree',
                           'form': form,
                           'image_data': image}
            except:
                context['title'] = 'Error occurred'
                messages.add_message(request, messages.WARNING,
                                     'Error occurred, please choose different file or different classifier')

    return render(request, 'decision_tree.html', context=context)


def text_mining(request):
    context = {
        'title': 'ID carver',
        'form': IdCarverForm()
    }
    if request.method == 'POST':
        form = IdCarverForm(request.POST)
        if form.is_valid():
            results = text_sanitizer(request.POST['text'])
            context = {
                'title': 'ID carver',
                'form': form,
                'results': results,
            }
            if all(len(value) == 0 for value in results.values()):
                messages.add_message(request, messages.WARNING,
                                     'No strings resembling personal or corporate IDs were found')

    return render(request, 'id_carver.html', context=context)


def personal_id_data(request, personal_id):
    return render(request, 'personal_data_viewer.html',
                  context={'data': get_personal_description(personal_id)})


def corporate_id_checker(request, corporate_id):
    context = {
        'title': 'Corporate ID data',
        'corporate_data': get_company_data(corporate_id)
    }
    return render(request, 'corporate_data_viewer.html', context)


def homepage(request):
    return render(request, 'homepage.html')
