from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from json import loads, dumps, JSONDecodeError
from datetime import timedelta
from smallurl.models import URL
from smallurl.forms import URLForm
from re import sub

# Create your views here.
# TODO: 
# implement homepage
# disable debug mode
# write api docs

def app(request):
    fullhostname = request.get_host()
    hostname = sub(r':\d{0,5}$', '', fullhostname)
    form = URLForm(initial={'tls': True})
    context = {
        'form': form,
        'hostname': hostname,
        'fullhostname': fullhostname,
        'error': False,
        'error_message': None,
        'new_url': None,
        'old_url': None
        }
    
    if request.method == 'POST':
        form = URLForm(request.POST)
        
        if form.is_valid():
            url = form.cleaned_data['url']
            tls = form.cleaned_data['tls']
            custom_id = form.cleaned_data['custom_id']

            context['old_url'] = url

            # Validate URL
            if tls:
                uri = f'https://{url}'
            else:
                uri = f'http://{url}' 
                
            validator = URLValidator(schemes=['http', 'https'])
            try:
                validator(uri)
                
                # If custom id is given
                if custom_id != '':
                    # Check if id is already in database
                    d = URL.objects.filter(id=custom_id)
                    if len(d) == 1:
                        form = URLForm(initial={
                            'url': url,
                            'tls': tls
                            })
                        
                        context['form'] = form
                        context['error'] = True
                        context['error_message'] = 'Alias already taken'
                    else:
                        new_url = URL(id=custom_id, url=url, tls=tls)
                        new_url.save()
                        context['new_url'] = f'{request.build_absolute_uri("/")}{new_url.id}'
                        
                else:
                    new_url = URL(url=url, tls=tls)
                    new_url.save()
                    context['new_url'] = f'{request.build_absolute_uri("/")}{new_url.id}'
            except ValidationError:
                form = URLForm(initial={
                    'url': url,
                    'tls': tls
                    })
                
                context['form'] = form
                context['error'] = True
                context['error_message'] = 'Invalid URL'
        
    return render(request, 'smallurl/app.html', context)

def redirect(request, **kwargs):
    id = kwargs['id']
    
    url = URL.objects.filter(id=id)

    if len(url) == 0:
        return HttpResponseNotFound()
    
    url = url[0]
    if url.expires != None:
        if url.expires <= timezone.now():
            url.delete()
            return HttpResponseNotFound()
    
    protocol = 'http'
    if url.tls:
        protocol = 'https'
        
    return HttpResponseRedirect(f'{protocol}://{url.url}')

def shortenURLv1(request):
    if request.method == 'POST':
        try:
            try:
                body = request.body.decode()
            except (UnicodeDecodeError, AttributeError):
                pass

            print(body)
            body = loads(request.body)
        except JSONDecodeError:
            return HttpResponseBadRequest('Invalid request body')
        
        url = body['url']
        if url == None:
            return HttpResponseBadRequest('Missing URL')
        
        # Validate URL
        validator = URLValidator(schemes=['http', 'https'])
        try:
            validator(url)
        except ValidationError:
            return HttpResponseBadRequest('Malformed URL')
        
        # Check url protocol, default is HTTPS
        tls = True
        if 'http://' in url.lower():
            tls = False
        
        if tls:
            url = url.replace('https://', '')
        else:
            url = url.replace('http://', '')
            
        # Parse link expiry time, defaults to no expiry if not provided
        try:
            seconds = body['expires_in']
        except KeyError:
            seconds = None
        
        expires = None
        if seconds != None:
            try:
                seconds = int(seconds)
            except ValueError:
                return HttpResponseBadRequest('expires_in must be a valid integer greater than 0')
                
            if seconds > 0:
                expires = timezone.now() + timedelta(seconds=seconds)
            else:
                return HttpResponseBadRequest('expires_in must be a valid integer greater than 0')
        
        # If custom id is given
        try:
            custom_id = body['custom_id']
            # Check if id is already in database
            d = URL.objects.filter(id=custom_id)
            if len(d) == 1:
                return HttpResponseBadRequest('custom_id already exists')
            else:
                new_url = URL(id=custom_id, url=url, tls=tls, expires=expires)
        except KeyError:
            # Check if url already in database, return link if true (prevent duplicates)
            d = URL.objects.filter(url=url, tls=tls, expires=expires)
            if len(d) == 1:
                return HttpResponse(dumps({'url': f'{request.build_absolute_uri("/r/")}{d[0].id}'}))
            else:
                new_url = URL(url=url, tls=tls, expires=expires)
                
        # Create and save record
        new_url.save()
        return HttpResponse(dumps({'url': f'{request.build_absolute_uri("/")}{new_url.id}'}), content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid request method')