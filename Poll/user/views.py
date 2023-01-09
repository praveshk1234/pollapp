from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .models import Poll,Choice,Vote
from django.contrib.auth.decorators import login_required
from .forms import PollAddForm,CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def logoutUser(request):
    logout(request)
    messages.info(request,'User is logged out')
    return redirect('login')
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=='POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'index')
        else:
            messages.error(request,'Username or Password is incorrect')
    return render(request,'login_register.html')
def registerUser(request):
    form = CustomUserCreationForm()
    page='register'
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            login(request,user)
            messages.success(request,"You login successfully")
            return redirect('index')
        else:
            messages.success(request," An errror occur during register")
    context = {'page':page,'form':form}
    return render(request,'login_register.html',context)

def index(request):
    poll=Poll.objects.all()
    return render(request,'polllist.html',{"polllist":poll})
def poll_create(request):
    if request.method == 'POST':
        form=PollAddForm(request.POST)
        if form.is_valid:
            poll=form.save(commit=False)
            poll.owner= request.user.profile
            poll.save()
            choice1 = Choice(
                    poll=poll, choice_value=form.cleaned_data['choice1']).save()
            choice2 = Choice(
                    poll=poll, choice_value=form.cleaned_data['choice2']).save()
            choice3 = Choice(
                    poll=poll, choice_value=form.cleaned_data['choice3']).save()
            choice3 = Choice(
                    poll=poll, choice_value=form.cleaned_data['choice4']).save()
            return redirect(reverse('poll-detail',args=[poll.id]))

    else:
        form=PollAddForm()
    return render(request,'poll_form.html',{'form':form})


def polldetail(request,pk):
    pollobj=Poll.objects.get(id=pk)
    if not pollobj.has_user_vote(request.user.profile):
        messages.info(request,'You already voted for this poll')
        return redirect("index")
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if choice_id:
            choice= Choice.objects.get(id=choice_id)
            vote=Vote(user=request.user.profile,poll=pollobj,choices=choice)
            vote.save()
            return redirect(reverse('poll-result',args=[pollobj.id]))
    return render(request,'polldetail.html',{'pollobj':pollobj})

def pollresult(request,pk):
    pollobj=Poll.objects.get(id=pk)
    return render(request,'pollresult.html',{'pollobj':pollobj})
