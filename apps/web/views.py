from django.shortcuts import render
from django.views import View
# Create your views here.

class MainView(View):
    template_name = 'bajo_construccion.html'

    def get(self, request):
        return render(request, self.template_name)
