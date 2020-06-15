from django.shortcuts import render_to_response, RequestContext
from django.views.generic import FormView, ListView
from django.views.generic.edit import FormMixin

from crispy_forms.utils import render_crispy_form
from django.core.context_processors import csrf

from MATOM.models import TranscriptionFactor
from search.search_code import *
from search.forms import *
from jsonview.decorators import json_view
from django.utils.decorators import method_decorator

from MATOM.views import AjaxableResponseMixin


def search_fun(request):
    query_string = ''
    found_items = []
    not_found = ''
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query_string = form.cleaned_data.get('search')

            entry_query = get_query(query_string, ['tf_name', 'alt_tf_name', ])

            found_entries = TranscriptionFactor.objects.filter(entry_query)
            print(found_entries)
            if len(found_entries) > 0:
                for items in found_entries:
                    if found_entries is not None:
                        found_items.append(items.tf_name)
                        if items.alt_tf_name in found_items:
                            continue
                        else:
                            found_items.append(items.alt_tf_name)
                    else:
                        found_items.append("No results found")
            else:
                not_found = "No results found"
        return render_to_response('search/search.html',
                                  {'form': form, 'query_string': query_string, 'found_entries': found_items,
                                   'not_found': not_found}, context_instance=RequestContext(request))
    else:
        form = SearchForm()
        return render_to_response('search/search.html', {'form': form, 'not_found': not_found},
                                  context_instance=RequestContext(request))


class SearchView(AjaxableResponseMixin, FormView):
    template_name = 'search/search.html'
    model = TranscriptionFactor
    success_url = "/search"
    form_class = SearchForm
    not_found = ''
    found_items = []

    @method_decorator(json_view)
    def get(self, request, *args, **kwargs):
        print("This is our path")
        form = SearchForm(self.request.GET)
        #if self.request.method == 'GET':
        if request.is_ajax():
            print("then here")
            #if form.is_valid():

            query_string = form.cleaned_data.get('search')
            self.found_items = []  # empty found item s after each iteration
            entry_query = get_query(query_string, ['tf_name', 'alt_tf_name', ])
            found_entries = TranscriptionFactor.objects.filter(entry_query)
            if len(found_entries) > 0:
                for items in found_entries:
                    if found_entries is not None:
                        print(items.tf_id)
                        self.found_items.append(items.tf_name)
                        if items.alt_tf_name in self.found_items:
                            continue
                        else:
                            self.found_items.append(items.alt_tf_name)
                    else:
                        self.found_items = []
            else:
                self.not_found = "No results found"

            #form_html = self.render_to_response(self.get_context_data(form=form))
            #form_html = render_to_string('search/search.html', context=data, request=request)
            #return self.render_to_response(self.get_context_data(form=form))
            return {'success': True, 'form_html': form_html}
        ctx = {}
        ctx.update(csrf(request))
        #print ctx
        form_html = render_crispy_form(form, context=ctx)

        return self.render_to_response(self.get_context_data(form=form))
        #return {'success': False, 'form_html': form_html}

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'found_entries': self.found_items,
            'not_found': self.not_found,
        })
        print(context)
        
        return context


class SearchView2(FormMixin, ListView):
    template_name = 'search/search.html'
    model = TranscriptionFactor
    success_url = "/search"
    form_class = SearchForm
    not_found = ''
    found_items = []

    def get_form_kwargs(self):
        return {
          'initial': self.get_initial(),
          'prefix': self.get_prefix(),
          'data': self.request.GET or None
        }

    def get(self, request, *args, **kwargs):
        form = SearchForm(self.request.GET)
        #if self.request.method == 'GET':

        if form.is_valid():
            query_string = form.cleaned_data.get('search')
            self.found_items = []  # empty found item s after each iteration
            entry_query = get_query(query_string, ['tf_name', 'alt_tf_name', ])
            print(entry_query)
            found_entries = TranscriptionFactor.objects.filter(entry_query)
            if len(found_entries) > 0:
                for items in found_entries:
                    if found_entries is not None:
                        print(items.tf_id)
                        self.found_items.append(items.tf_name)
                        if items.alt_tf_name in self.found_items:
                            continue
                        else:
                            self.found_items.append(items.alt_tf_name)
                    else:
                        self.found_items = []
            else:
                self.not_found = "No results found"
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'found_entries': self.found_items,
            'not_found': self.not_found,
        })
        return context

