from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Item, Profile
from django.urls import reverse
from .forms import ItemForm, ProfileForm
from .utils import detect_labels
from django.contrib.auth.decorators import login_required

#Home Function for home page all object view.
@login_required
def home(request):
    items = Item.objects.all()
    return render(request, 'lf_box/home.html', {'items' : items})  #passing home.html as template and items is a dictionary getting all data from items model. Django will render this page with all details and send it back to user

def register(request):
    if request.method == 'POST':                        #When USer fills the form registers it would be post with all info.
        form = UserCreationForm(request.POST)
        if form.is_valid():                             #THis if block will save user information after validation.
            user = form.save()
            Profile.objects.get_or_create(user=user)
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

def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    items = Item.objects.filter(user=request.user)      #Getting all items posted by the user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', profile_id=profile.id)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'lf_box/profile.html', {'form' : form, 'items' : items, 'profile': profile})

    
def view_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    items = Item.objects.filter(user=profile.user)
    return render(request, 'lf_box/view_profile.html', {'profile': profile, 'items' : items})

def edit_items(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)
    profile = get_object_or_404(Profile, user=request.user)  # Get the user's profile
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(reverse('view_profile', kwargs={'profile_id': profile.id}))
    else:
        form = ItemForm(instance=item)
    return render(request, 'lf_box/edit_item.html', {'form': form})

@login_required
def delete_item(request, item_id, profile_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)  # Ensure user owns the item
    profile = get_object_or_404(Profile, id=profile_id)  # Ensure profile exists

    if request.method == 'POST':
        item.delete()
        return redirect('view_profile', profile_id=profile.id)  # Redirect to correct profile
    return render(request, 'lf_box/confirm_delete.html', {'item': item, 'profile': profile})