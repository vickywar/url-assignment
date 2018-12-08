from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from .models import URL
from .forms import URLForm
# Create your views here.

def index(request):

	urls = URL.objects.all()

	url_list = []

	if request.method == "POST":
		#print(request.POST)
		form = URLForm(request.POST)
		form.save()

	form = URLForm()

	for url in urls:

		urlinfo = requests.get(url).text
		urlparse = BeautifulSoup(urlinfo,'lxml')
		is_jquery_or_not = urlparse.find('script')
		string_is_jquery = str(is_jquery_or_not)

		c = {
			"url": "",
			"success": "",
			"uses_jquery": "",
			"version": "",
			"found_in_line": ""
		}

		if "jquery" in string_is_jquery:
			c["success"]+="True"
			c["uses_jquery"]+="Yes"
			c["found_in_line"]+=string_is_jquery
			c["url"]+=str(url)
		else:
			c["success"]+="False"
			c["uses_jquery"]+="No"
			c["found_in_line"]+="null"
			c["url"]+=str(url)


		split_string = string_is_jquery.split('/')

		for i in range(0,len(split_string)):
				if split_string[i]=='jquery':
					c["version"]+=split_string[i+1]


		url_list.append(c)
	print(url_list)

	context= {'url_list' : url_list, 'form': form}
	return render(request,"userinputpage.html",context)