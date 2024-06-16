from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import *
from django.db.models import Q    ## for storing code like (if esle)
import razorpay
from django.core.mail import send_mail

# Create your views here.
def product(request):
    # p = Product.objects.all()
    # context = {'data'}
    
    p = Product.objects.filter(is_active = True)   ### to show only active product
    # print(p)
    context = {}
    context['data']= p
    return render(request, 'index.html',context)

context = {}
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        un = request.POST['uname']
        ue = request.POST['uemail']
        p = request.POST['upass']
        pc = request.POST['ucpass']
        # print(un)
        # print(ue)
        # print(p)
        # print(pc)
        if un == '' or ue == '' or p =='' or pc == '':
            # print('feild cant be blank ')
            context['errmsg']='feild cant be blank '
            return render(request, 'register.html',context)
        elif p != pc:
            # print('password and confirm passsword should be same') 
            context['errmsg']='password and confirm passsword should be same'
            return render(request, 'register.html',context)
        elif len(p) < 8:
            # print('password should be greater than 8..')
            context['errmsg']='password should be greater than 8..'
            return render(request, 'register.html',context)
        else:
            m = User.objects.create(username = un,  email = ue )
            m.set_password(p)    ## for password encription
            m.save()
            context['success']='Data inserted succesfully........!'
            return render(request, 'register.html',context)
def ulogin(request):
    context = {}
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        n = request.POST['uname']
        p = request.POST['upass']
        # print(n)
        # print(p)
        e = authenticate(username=n,password=p)
        # print(e)
        if e is not None:
            login(request,e)
            return redirect('/product')
        else:
            context['ermsg']='Invalid Username or Password'
            return render(request,'login.html',context)

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def user_logout(request):
    logout(request)
    return redirect('/product') 


def catfilter(request, cv):
    # print(cv)
    q1 = Q(is_active = True)   
    q2 = Q(cat = cv)
    p = Product.objects.filter(q1 & q2)   ## to show the product carogary wise in filter
    context = {}
    context['data'] = p
    return render(request,'index.html',context) 

def sortfilter(request,sv):
    context = {}
    if sv == '1':
        # p = Product.objects.order_by('-price').filter(is_active = True)    ## for soting price high to low
        t = '-price'
        
    else:
        # p = Product.objects.order_by('price').filter(is_active = True)    ## for soting price low to high
        t = 'price'
        # context = {}
        # context['data'] = p
        # return render(request,'index.html',context)
        
    p = Product.objects.order_by(t).filter(is_active = True)
    context['data'] = p
    return render(request,'index.html',context)

def pricefilter(request):
    min = request.GET['min']
    max = request.GET['max']
    # print(min)
    # print(max)
    q1 = Q(price__gte = min)   ## price is greater than equal to min
    q2 = Q(price__lte = max)
    p = Product.objects.filter(q1 & q2).filter(is_active = True)
    context = {}
    context['data'] = p 
    return render(request,'index.html',context)

def search(request):
    s = request.GET['search']
    # print(s)
    pname = Product.objects.filter(name__icontains= s)   ## icontains for like for sarching the ccontent
    pcat = Product.objects.filter(cat__icontains= s)
    pdet = Product.objects.filter(pdetail__icontains= s)
    allprod = pname.union(pcat, pdet)
    context = {}
    if allprod.count() == 0:    ## checking product list count
        context['errmsg'] = 'Opps Product Not found ......!!!!'

    context['data'] =  allprod     ## else this will be right
    return render(request,'index.html',context)


def product_detail(request, pid):
    context = {}
    p = Product.objects.filter(id=pid)
    context['data'] = p
    return render(request,'product_detail.html',context)

def addtocard(request,pid):
    # print(pid)
    
    if request.user.is_authenticated:  # if u want add cart in product at that time it will check user in loged in or not 
        # print('User is logged in')
        u = User.objects.filter(id = request.user.id)
        p = Product.objects.filter(id = pid)
        context = {}
        context['data'] = p
        q1 = Q(uid = u[0])  
        q2 = Q(pid = p[0])
        c = Cart.objects.filter(q1 & q2)   ## for single card
        n = len(c)

        if n == 0 :
            c = Cart.objects.create(uid = u[0], pid = p[0])    ## u[0] for all data from user 
            c.save()
            context['success'] = 'Product succesfully added in cart....'
            return render(request,'product_detail.html',context)
        else:
            context['errmsg'] = 'Product already added in in cart.....! '
        return render(request,'product_detail.html',context)

    else:
        return redirect('/login')


def cart(request):
    c = Cart.objects.filter(uid = request.user.id)   ##
    # print(c)
    # print(c[0].pid.name)  ## for product name
    context = {}
    s = 0
    for i in c:
        s = s+i.pid.price*i.qty   ## from price addtion logic

    context['total'] = s
    context['n'] = len(c)    ## for length of product
    context['data']= c
    return render(request,'cart.html',context)


def updateqty(request,u,cid):
    c = Cart.objects.filter(id = cid)
    q = c[0].qty
    if u == '1':
        q = q + 1
    elif q>1:
        q = q - 1
    c.update(qty =  q)
    # print(type(c))
    return redirect('/viewcart')

def remove(request,cid):
    c = Cart.objects.filter(id = cid)
    c.delete()
    return redirect('/viewcart')

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    #print(c)
    for i in c:
        amount=i.qty*i.pid.price
        o=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=amount)
        o.save()
        i.delete()
         
    #return render(request,'placeorder.html')
    return redirect('/fetchorder')

def fetchorder(request):
    o = Order.objects.filter(uid = request.user.id)
    context = {}
    context['data'] = o
    q=0
    tamount=0
    for i in o:
        q=q+i.qty
        tamount=tamount+(i.qty*i.pid.price)

    context['data']=o
    context['total']=tamount
    context['n']=q
    return render(request,'placorder.html',context)

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_IC8L83MtJlRjzB", "8IYbz2xMiHDD1W3D9yWUBKUB"))
    o = Order.objects.filter(uid = request.user.id)
    s = 0
    for i in o:
        s =s +i.amt
    # data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    data = { "amount": s, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    # print(payment)
    context['payment'] = payment
    return render(request,'pay.html',context)


## for payment
def paymentsucess(request):
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    sub='E-commerce Order Status'
    msg='Thanks for Shopping...!!!!'
    frm='hrikeshyadav1999@gmail.com'
    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )
    return render(request,'paymentsuccess.html')

