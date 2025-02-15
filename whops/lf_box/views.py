from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Item
from .forms import ItemForm
from .utils import detect_labels
from django.contrib.auth.decorators import login_required

#Home Function for home page all object view.
def home(request):
    items = Item.objects.all()
    return render(request, 'lf_box/home.html', {'items' : items})  #passing home.html as template and items is a dictionary getting all data from items model. Django will render this page with all details and send it back to user

def register(request):
    if request.method == 'POST':                        #When USer fills the form registers it would be post with all info.
        form = UserCreationForm(request.POST)
        if form.is_valid():                             #THis if block will save user information after validation.
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()                       #When User clicks on register, it would be a get request, loading the registeration form.
    return render(request, 'lf_box/register.html', {'form': form})

def post_item(request):
    if request.method == "POST":                        # Check if the request is a POST request.
        form = ItemForm(request.POST, request.FILES)    # Get form data and files from users POST request after submission .
        if form.is_valid():                             # Validate form
            item = form.save(commit=False)              # Save the form data to an Item object
            item.user = request.user                    # Assigns the logged in user to the item.
            image_bytes = item.image.read()             # Reads uploaded image in to bytes format
            #labels = detect_labels(image_bytes)         # Calling detect_labels function which will provide AWS Rekognition analysis output in form of Labels.
            #item.labels = ", ".join([label['Name'] for label in labels]) #Creates a comma sepated string of labels and assigns it to lebel field for that item.
            item.save()                                 # Saves the new item object to database.
            return redirect('home')                     # Redirects back to home page.
    else:
        form = ItemForm()                               #When user reaches the for for the first time, means its a get method, not post, this will show a blank form to fill.
    return render(request, 'lf_box/post_item.html', {'form' : form})