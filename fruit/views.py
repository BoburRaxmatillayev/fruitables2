from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse

from .forms import ContactForm
from .bot import send_message
from .models import Contact,Product,Category,Comment
from django.views.generic import View,TemplateView,DetailView


def add_comment(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        comment = request.POST['comment']

        # Save the comment to the database
        new_comment = Comment(name=name, email=email, comment=comment)
        new_comment.save()

        return redirect('some-view-name')  # Redirect to a page after successful submission

    return HttpResponse("Invalid request", status=400)


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self,*args, **kwargs):
        context = super(HomeView, self).get_context_data(*args,**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        
        query = self.request.GET.get('q')
        if query:
            context['products'] = Product.objects.filter(title__icontains=query)

        return context

    
class ShopDetailView(DetailView):
    model = Product
    template_name = "shop-detail.html"
    context_object_name = "product"

def shop_view(request):
    return render(request,"shop.html")

class ContactView(View):
    template_name = "contact.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs): 
        name = request.POST.get('first_name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('description', '')
        contact = Contact(first_name=name,email=email,description=message)
        contact.save()
        
        send_message(f"Ism: {name}\nEmail: {email}\nText:{message}")

        return HttpResponseRedirect(reverse('home-page'))   

# class ContactView(CreateView):
#     model = Contact
#     form_class = ContactForm
#     template_name = "contact.html"
#     success_url ='/'


# def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('first_name', '')
#         email = request.POST.get('email', '')
#         message = request.POST.get('description', '')
#         contact = Contact(first_name=name,email=email,description=message)
#         contact.save()
        
#         send_message(f"Ism: {name}\nEmail: {email}\nText:{message}")

#         return render(request, 'contact.html')
        
#     else:
#         return render(request, "contact.html")