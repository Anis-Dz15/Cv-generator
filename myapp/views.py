from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io


def accept(request):
    if request.method == "POST":
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        phone = request.POST.get("phone","")
        summary = request.POST.get("summary","")
        degree = request.POST.get("degree","")
        school = request.POST.get("school","")
        university = request.POST.get("university","")
        previous_work = request.POST.get("previous_work","")
        skills = request.POST.get("skills","")
        
        # Get the data from the forms front
        profile = Profile(name=name,
                          email=email,
                          phone=phone,
                          summary=summary,
                          degree=degree,
                          school=school,
                          university=university,
                          previous_work=previous_work,
                          skills=skills)
        # Save the data in the BDD
        profile.save()
    return render(request,'pdf/accept.html')


def resume(request,id):
    user_profile = Profile.objects.get(pk=id) 
    tempalte = loader.get_template('pdf/resume.html')
    html = tempalte.render({'user_profile':user_profile})
    options = {
        'page-size':'Letter',
        'encoding':'UTF-8',
    }
    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "resume.pdf"
    return response()