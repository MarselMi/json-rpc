from django.shortcuts import render
from .forms import JsonRpcForm
from .rpc_client import call_jsonrpc_method
import json

def jsonrpc_view(request):
    result = None
    if request.method == 'POST':
        form = JsonRpcForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data['method']
            params = form.cleaned_data['params']
            try:
                params = json.loads(params) if params else {}
            except json.JSONDecodeError:
                params = {}
            result = call_jsonrpc_method('https://slb.medv.ru/api/v2/', method, params)
    else:
        form = JsonRpcForm()
    return render(request, 'index.html', {'form': form, 'result': result})
