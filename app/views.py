"""
Definition of app views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from app import forms
from django.contrib import messages
from app import models
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from datetime import datetime as dt
from datetime import timedelta  
import itertools

#universal book limit constant to 5
bookLimit=5
#get required details from model to use them in view below
#gets the librairans 
def get_librarians():
    librarians={}
    for league in models.Librn.objects.all():
          if league.lb_id not in librarians.keys():
                    librarians[league.lb_id]=league
    return list(librarians.keys())

#get the book Ids and bks objects based on user selection from form
def getSelectedbooks(request,selectIndecies):    
    saelectedBooks={}
    books=get_valid_Books()
    for l in selectIndecies:          
           saelectedBooks[l]=books[l]
    return saelectedBooks
#get the borrowed books per use
def SetBorrowed(username,selectIndecies):    
    saelectedBooks={}
    books=get_valid_Books()
    for l in selectIndecies:          
           saelectedBooks[l]=books[l]
    return saelectedBooks

#Experimental method have not used any where 
#intended to  use as a reusable method to set the value based on model and column to change 
def SetValue(Pk,ModelName,ValueCoulumn,value):    
    Req=ModelName.objects.get(id=pk)
    Req.ValueCoulumn=value
    Req.save()
    return True
#gets the count of books borrowes by library memebers
def get_PerMemberbookCount():
    borrowedperStudent={}
    borrowed=get_Borrowed()
    for k,v in borrowed.items():
        composite=v.cwid.cwid.stu_id
        if composite not in borrowedperStudent.keys():
            borrowedperStudent[composite]=1
        else:
            li =borrowedperStudent[composite]
            li+=1
            borrowedperStudent[composite]=li
    return borrowedperStudent
#Experimental method have not used any where 
#intended to  use as a reusable method to get the values based on model 
def GetValue(Pk,Model,cwid):    
    ilist=[]
    if isinstance(Pk, (list,)):
        for k in Pk:
             ilist.append(Model.objects.get(cwid=Pk))
    else:
         ilist.append(Model.objects.get(cwid=Pk))
    return ilist
#logic to get hold of the user and the book borrowed and link
def AddBookToUser(username,Books):   
    myObj={}
    message="select a book"
    withinlimt=False
    inventory=[]
    #gets the books that are not 0-0 in location
    allbooks=get_valid_Books()
    avialble=False
    #gets the library member object
    libmember = models.Libmem.objects.get(cwid_id=username)   
    book_ids=Books.keys()
    for id in Books:
        inventory.append(models.Invt.objects.get(i_id_id=id))
        #decreasing qty available
        alreadytook=False
        #get the Inventory object based on ID
        thisobj =models.Invt.objects.get(i_id_id=id)
        if  thisobj.qty>0: 
            avialble=True
            message="success"
        else:
            message='The book is not avialable for borrowing .please contact the librarian for more details !!!'
            continue
        try:
            #get the borrowed object based on book.id
            ta= models.Bowed.objects.filter(b_id_id=thisobj.i_id.b_id)
            for t in ta:
                if t.cwid_id == libmember.id and t.b_id.b_id==id:
                    alreadytook=True
                    message="User :: "+t.cwid.cwid_id+" have already borrowed this book. you cannot borrow same book twice"
                    continue
                else:
                    alreadytook=False
            #get count for user 
            count=0
            #get the books count per user
            userbooks =get_PerMemberbookCount()
            if username in userbooks.keys():
                count=userbooks[username]
            else:
                count=0

            if count < bookLimit:
                withinlimt=True
            else:
                message="User :: "+username+" have already borrowed " +str(count)+ " books. you cannot borrow more than "+str(bookLimit)
            if not alreadytook and avialble and withinlimt:
                models.Bowed.objects.create(i_id=thisobj,cwid=libmember,b_id=thisobj.i_id,issue=dt.now(),due=dt.now()+timedelta(days=6))
                thisobj.qty=thisobj.qty-1
            thisobj.save()
        except Exception as e:
            print(e)
            pass
        



    #getting the cwid and libraryId for the user to add to the book to list
    
    return message



#getting all books 
def get_Books():
    books={}
    for league in models.Bks.objects.all():          
                    books[league.pk]=league
    return books
#get all books that location is not empty
def get_valid_Books():
    books={}
    for league in models.Bks.objects.all(): 
        if league.invt.rack != '0':
            books[league.pk]=league
    return books

#get all departments
def get_Dpts():
    Dpts={}
    for league in models.Dept.objects.all():          
                    Dpts[league.pk]=league
    return Dpts
#get all libray members
def get_libmems():
    libmem={}
    for league in models.Libmem.objects.all():          
                    libmem[league.pk]=league
    return libmem
#get inventories
def get_Inv():
    inv={}
    for league in models.Invt.objects.all():          
                    inv[league.pk]=league
    return inv
def get_Borrowed():
    inv={}
    for league in models.Bowed.objects.all():          
                    inv[league.pk]=league
    return inv
def get_LibrarianOrders():
    inv={}
    for league in models.Border.objects.all():          
                    inv[league.pk]=league
    return inv
           # This gives you all the users that are related to librarian

#views 
#Renders home if only logged in and enable the capability view inventory and report sections (index.html)                     
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    iscapable =False
    if request.user.username in get_librarians():
        iscapable=True;

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'iscapable':iscapable,
            'year':datetime.now().year,
        }
    )
#Renders forgot screen                      
def forgot(request):
    """Renders the loginpartial page."""
    assert isinstance(request, HttpRequest)   
    return HttpResponse("<ul><li><a href='/contact'> you need to contact your librarian to reset your password </a></li><li><a href='/'> Return to home to login or register</a></li></ul>", content_type="text/html"
    )
#Renders reports if only logged in and has the capability to view inventory and report sections                
def Reports(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    iscapable =False
    if request.user.username in get_librarians():
        iscapable=True;
    #getting books per each department
    booksperdepart={}
    borrowedperStudent={}
    ordersplacedbylibrairans={}
   
    books=get_valid_Books()
    invent=get_Inv()
    for k,v in books.items():
        if v.dpt_id.name not in booksperdepart.keys():
            booksperdepart[v.dpt_id.name]=v.invt.qty
        else:
            li =booksperdepart[v.dpt_id.name]
            li+=v.invt.qty
            booksperdepart[v.dpt_id.name]=li
    libmem =get_libmems()
    borrowed=get_Borrowed()
    for k,v in borrowed.items():
        composite=v.cwid.cwid.stu_name+" - "+v.cwid.cwid.stu_id
        if composite not in borrowedperStudent.keys():
            borrowedperStudent[composite]=1
        else:
            li =borrowedperStudent[composite]
            li+=1
            borrowedperStudent[composite]=li
    librianorders=get_LibrarianOrders()
    for k,v in librianorders.items():
        composite=v.lb_id.name+" - "+v.lb_id_id
        if composite not in ordersplacedbylibrairans.keys():
            ordersplacedbylibrairans[composite]=[list([v.i_id.i_id.title,v.qty,v.i_id.i_id.dpt_id.name,v.status])]
        else:
            li =ordersplacedbylibrairans[composite]
            li.append(list([v.i_id.i_id.title,v.qty,v.i_id.i_id.dpt_id.name,v.status]))
            ordersplacedbylibrairans[composite]=li

   


    

    return render(
        request,
        'app/reports.html',
        {
            'title':'Reports Page',
            'perdptbks':list(zip(booksperdepart.keys(),booksperdepart.values())),
            'peruserbks':list(zip(borrowedperStudent.keys(),borrowedperStudent.values())),
            'perlibrarian':list(zip(ordersplacedbylibrairans.keys(),ordersplacedbylibrairans.values())),
            'iscapable':iscapable,
            'year':datetime.now().year,
        }
    )


#Edit book Details
def EditbookDetails(request):
    """Add values to borrowtable""" 
    OldBookDetails=[]
    departments={}
    clearfilter=False
    message=""
    FormBookIds=[]
    OldBookDetails=[]
    modes=['manage','add','order']
    for league in models.Dept.objects.all():          
                        departments[league.pk]=league
    message=""
    bookId =request.POST.getlist('bookId')
    BookName =request.POST.getlist('bookName')
    bookDesc =request.POST.getlist('ebookdesc')
    AuthorName =request.POST.getlist('eAuthorName')
    Quantity =request.POST.getlist('eQuantity')
    RowRack =request.POST.getlist('eRowRack')
    Select =request.POST.getlist('edepart_select')
    for e in bookId:
            a=get_valid_Books()[e]
            OldBookDetails.append(a)
    for a,b,c,d,e,f,g,h in itertools.zip_longest(bookId,BookName,bookDesc,AuthorName,Quantity,RowRack,Select,OldBookDetails):
        if a==h.b_id:
            try:
                bookobj=models.Bks.objects.get(b_id=a)
                if bookobj.title.lower() != b.lower():
                    bookobj.title=b.strip()
                else:
                    message="book Name is empty .will not change"
                if bookobj.desc.lower() != c.lower():
                    bookobj.desc=c.strip()
                else:
                    message="book Desc is empty .will not change"
                if bookobj.a_id.name.lower() != d.lower():
                    atrobj=models.Atr.objects.get(a_id=bookobj.a_id.a_id)
                    atrobj.name=d.strip()
                    atrobj.save()
                else:
                    message="Author name  is empty .will not change"
                if int(bookobj.invt.qty) != int(e):
                    invobj=models.Invt.objects.get(id=bookobj.invt.id)
                    invobj.qty=int(e)
                    if bookobj.invt.shelf != f.lower():
                        splitv=f.split("-")
                        if(len(splitv)==3):                        
                               bookobj.invt.shelf=str(splitv[0])
                               bookobj.invt.rack=str(splitv[1])
                               bookobj.invt.row=int(splitv[2])                           
                        else:
                            message="Location is not in correct format .will not change it should be in  <shelf> - <rack> -<row>"
                    else:
                          message="Location information is empty .will not change"
                    invobj.save()

                else:
                    message="Quantity is empty .will not change"
               
                if bookobj.dpt_id_id.lower() != g.lower():
                      dptobj=models.Dept.objects.get(dpt_id=g)
                      bookobj.dptid=dptobj
                else:
                    message="book Name is empty .will not change"
                bookobj.save()
                message="Success"
            except Exception as e:
                message=e


    return render(
        request,
        'app/manageInv.html',
        {
            'title':'Manage Inventory',
            'invmodes':modes,
            'dispmode':'manage',
            'message':message,
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
             'books':get_valid_Books().values(),
             'clearfilter':clearfilter,
            'year':datetime.now().year,
        }
    )

#Renders books(about.html) and addthe selected book to user cart and mark it as borrowed
#if only logged in and has the capability to view books   
def AddtoBorrowList(request):
    """Add values to borrowtable""" 
    
    selectIndecies =request.POST.getlist('chooseBook')
    booksSelected =getSelectedbooks(request,selectIndecies)
    message =AddBookToUser(request.user.username,booksSelected)
    
    return render(
        request,
        'app/about.html',
        {
            'title':'Books',
            'message':message,
            'year':datetime.now().year,
        }
    )


def RemoveFromBorrowList(request):
    """Add values to borrowtable""" 
    
    BookDetails =request.POST.getlist('deletefrommylist')
    booksSelected =getSelectedbooks(request,BookDetails)
    username =request.user.username
    myObj={}
    message=""
    withinlimt=False
    inventory=[]
    #gets the books that are not 0-0 in location
    allbooks=get_valid_Books()
    avialble=False
    #gets the library member object
    libmember = models.Libmem.objects.get(cwid_id=username)   
    book_ids=allbooks.keys()
    for id,bookval in booksSelected.items():
        inventory.append(models.Invt.objects.get(i_id_id=id))
        #decreasing qty available
        alreadytook=False
        #get the Inventory object based on ID
        thisobj =models.Invt.objects.get(i_id_id=id)      
        try:
            
            #get count for user 
            count=0
            #get the books count per user
            bowedobj=models.Bowed.objects.filter(cwid_id=libmember.pk)
            for f  in bowedobj:
                if f.b_id_id == id:
                     reqbook=models.Bowed.objects.get(id=f.pk)
                     reqbook.delete()            
                     thisobj.qty=thisobj.qty+1
                     message="sucess"
            thisobj.save()
        except Exception as e:
            print(e)
            pass
    return render(
        request,
        'app/about.html',
        {
            'title':'Books',
            'message':message,
            'year':datetime.now().year,
        }
    )
#Renders manage inventory(manageInv.html) and the selected book to user cart and mark it as borrowed
#if only logged in and has the capability to view books and is a librarian      
def DelinInventory(request):
    """Delete from inventory on user slection"""
    departments={}
    clearfilter=False
    message=""
    FormBookIds=[]
    OldBookDetails=[]
    modes=['manage','add','order']
    for league in models.Dept.objects.all():          
                        departments[league.pk]=league
    Edits =request.POST.getlist('editS')
    if len(Edits)>0:
        message=""
        for e in Edits:
            a=get_valid_Books()[e]
            OldBookDetails.append(a)
        

        return render(
        request,
        'app/editInv.html',
        {
            'title':'Edit Details in Inventory',
            'invmodes':modes,
            'dispmode':'manage',
            'message':message,
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
             'books':OldBookDetails,
             'clearfilter':clearfilter,
            'year':datetime.now().year,
        }
    )

    else:
        for league in models.Dept.objects.all():          
                        departments[league.pk]=league

        message=""
        bookids = [x for x in  request.POST.getlist('delBook')]
        for s in bookids:
            models.Bks.objects.filter(b_id=s).delete()
            message="success"
   
    
    return render(
        request,
        'app/manageInv.html',
        {
            'title':'Manage Inventory',
            'invmodes':modes,
            'dispmode':'manage',
            'message':message,
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
             'books':get_valid_Books().values(),
             'clearfilter':clearfilter,
            'year':datetime.now().year,
        }
    )



#Renders manage inventory(manageInv.html) and gives libraian ablity to order for sepecified book
#if only logged in and has the capability to view books and is a librarian 
def OrderforInventory(request):
    """make order for books"""
    modes=['manage','add','order']
    departments={}
    clearfilter=False
    for league in models.Dept.objects.all():          
                    departments[league.pk]=league
    visited=False
    message=""
    nonemptyAuthors = [x for x in  request.POST.getlist('oAuthorName') if x!='']
    nonemptybooknames = [x for x in  request.POST.getlist('obookName') if x!='']
    nonemptybookDesc = [x for x in  request.POST.getlist('obookdesc') if x!='']
    nonemptyQuantities = [x for x in  request.POST.getlist('oQuantity') if x!='']
    nonemptyRows = [x for x in  request.POST.getlist('oRowRack') if x!='']
    nonemptyselectedDeparts = [x for x in  request.POST.getlist('odepart_select') if x!='NA']

 
    for j,k,h,fa,z,loc in itertools.zip_longest(nonemptyAuthors,nonemptybooknames,nonemptybookDesc,nonemptyselectedDeparts,nonemptyQuantities,nonemptyRows):
        visited=True
        shortname=k[1:5]  
        values=k.split("-")
        if len(values)==1:
            ye=dt.today().year
            values.extend(['I',ye,'0'])
        c=loc.split("-")
        if len(c)==1:
            c.extend(['0','0'])
        if len(values) >0:
            try:
                departmentDetails=models.Dept.objects.get(dpt_id=fa)
            except Exception as e:
                print(e)
                pass
            try:
                i=0
                testa = models.Atr.objects.values('a_id')
                for test in testa:
                    if i>int(test['a_id']):
                        i=i
                    else:
                        i=int(test['a_id'])
                    
                varas = models.Atr.objects.values('name')
                isin=False
                for f in list(varas):
                    if str(j) in f['name']:
                        isin=True
                        break
                if isin:
                    pass
                else:
                    models.Atr.objects.create(a_id=str(i+1),name=str(j),title="Mr.",email="library@mysite.edu")
            except Exception as e:
                if "does not" in str(e):
                    models.Atr.objects.create(a_id=str(i+1),name=str(j),title="Mr.",email="library@mysite.edu")
                print(e)
                pass
            varset=None
            try:
                bookop=None
                i=0;
                testab = models.Bks.objects.values('b_id')
                for test in testab:
                    if i>int(str(test['b_id']).split('_')[2]):
                        i=i
                    else:
                        i=int(str(test['b_id']).split('_')[2])
                if (models.Bks.objects.filter(title=str(values[0])).exists()):
                            try:                                
                                if not models.Bks.objects.filter(title=str(values[0]),edition=str(values[1]),p_year=str(values[2]),pub=str(values[3])).exists():
                                    models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=str(i+1),dpt_id_id=str(fa))
                                else:
                                    message="book with the same name already exists"
                                    bookop=models.Bks.objects.filter(title=str(values[0]),edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]))
                            except Exception as e:
                                    print(e)
                else:
                    if isin:
                        atrobj=models.Atr.objects.get(name=str(j))
                        models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=atrobj.a_id,dpt_id_id=str(fa))
                    else:
                        atrobj=models.Atr.objects.get(name=str(j))
                        models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=atrobj.a_id,dpt_id_id=str(fa))

            except Exception as e:
                if "Bks matching query does not" in str(e):
                    models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=str(i+1),dpt_id_id=str(fa))
                print(e)
                pass
            
            try:
                g=0
                bookobj =models.Bks.objects.filter(title=str(values[0]),edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]))
                testba = models.Invt.objects.values('id')   
                for test in testba:
                    if g>int(str(test['id'])):
                        g=g
                    else:
                        g=int(str(test['id']))
                               
                Invobj=models.Invt.objects.filter(i_id_id="IN_"+shortname+"_"+str(g+1))
                librarians=get_librarians()
                librnobj=None
                for u in librarians:
                    if request.user.username.lower() == u.lower():
                        librnobj=models.Librn.objects.get(lb_id=u)

                if len(bookobj) >= 0:
                    if(len(Invobj) == 0):
                          for s in bookobj:
                            models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id=s.b_id,shelf=str(c[0]),rack=str(0),row=int(0))
                            models.Border.objects.create(id=int(g+1),qty=int(z),status=loc,i_id_id=s.invt.id,lb_id_id=librnobj.lb_id)
                            message="Order placed successfully"
                    else:
                          for s in bookobj:
                            models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id=s.b_id,shelf=str(c[0]),rack=str(0),row=int(0))
                            models.Border.objects.create(id=int(g+1),qty=int(z),status=loc,i_id_id=s.invt.id,lb_id_id=librnobj.lb_id)
                            message="Order placed successfully"

                else:
                        models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id="IN_"+shortname+"_"+str(g+1),shelf=str(c[0]),rack=str(0),row=int(0))
                        models.Border.objects.create(id=int(g+1),qty=int(z),status=loc,i_id_id=int(g+1),lb_id_id=librnobj.lb_id)
                        message="Order placed successfully"
            except Exception as e:
                try:
                    if "does not" in str(e):                     
                        models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id="IN_"+shortname+"_"+str(g+1),shelf=str(c[0]),rack=str(0),row=int(0))
                    else:
                        t=models.Invt.objects.get(i_id_id="IN_"+shortname+"_"+str(g+1))
                        t.qty=  t.qty+int(z)
                        t.save()
                except Exception as e:
                     message="There is already an exisiting order for this book"
                     print(e)
             
            
        else:
            message="the book details are not given properly"
            pass
   
    if not visited:
        message="Fill the form properly and then press the SAVE "
    return render(
        request,
        'app/orderInv.html',
        {
            'title':'Order Inventory',
            'invmodes':modes,
            'dispmode':'order',
            'message':message,
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
             'books':get_Books().values(),
             'clearfilter':clearfilter,
            'year':datetime.now().year,
        }
    )



#Renders manage inventory(manageInv.html) and gives libraian ablity to Add books to inventory
#if only logged in and has the capability to view books and is a librarian 
def Addtoinventory(request):
    """Add values to db based on user input""" 
    modes=['manage','add','order']
    departments={}
    booklist=[]
    for league in models.Dept.objects.all():          
                    departments[league.pk]=league
    
    message=""
    nonemptyAuthors = [x for x in  request.POST.getlist('AuthorName') if x!='']
    nonemptybooknames = [x for x in  request.POST.getlist('bookName') if x!='']
    nonemptybookDesc = [x for x in  request.POST.getlist('bookdesc') if x!='']
    nonemptyQuantities = [x for x in  request.POST.getlist('Quantity') if x!='']
    nonemptyRows = [x for x in  request.POST.getlist('RowRack') if x!='']
    nonemptyselectedDeparts = [x for x in  request.POST.getlist('depart_select') if x!='NA']
   
    for j,k,h,fa,z,loc in itertools.zip_longest(nonemptyAuthors,nonemptybooknames,nonemptybookDesc,nonemptyselectedDeparts,nonemptyQuantities,nonemptyRows):
        shortname=k[1:5]  
        values=k.split("-")
        if len(values)==1:
            ye=dt.today().year
            values.extend(['I',ye,'0'])
       
        if loc is not None:
            c=loc.split("-")
            if len(c)==1:
                c.extend(['0','0'])
        else:
            #setting default value
            c=["20","10","1"]
        if len(values) >0:
            try:
                departmentDetails=models.Dept.objects.get(dpt_id=fa)
            except Exception as e:
                print(e)
                pass
            try:
                i=0
                testa = models.Atr.objects.values('a_id')
                for test in testa:
                    if i>int(test['a_id']):
                        i=i
                    else:
                        i=int(test['a_id'])
                    
                varas = models.Atr.objects.values('name')
                isin=False
                for f in list(varas):
                    if str(j).lower() == f['name'].lower():
                        isin=True
                        break
                if isin:
                    pass
                else:
                    models.Atr.objects.create(a_id=str(i+1),name=str(j),title="Mr.",email="library@mysite.edu")
            except Exception as e:
                if "does not" in str(e):
                    models.Atr.objects.create(a_id=str(i+1),name=str(j),title="Mr.",email="library@mysite.edu")
                print(e)
                pass
            varset=None
            try:
                i=0;
                testab = models.Bks.objects.values('b_id')
                for test in testab:
                    if i>int(str(test['b_id']).split('_')[2]):
                        i=i
                    else:
                        i=int(str(test['b_id']).split('_')[2])
                if (models.Bks.objects.filter(title=str(values[0])).exists()):
                            try:                                
                                if not models.Bks.objects.filter(title=str(values[0]),edition=str(values[1]),p_year=str(values[2]),pub=str(values[3])).exists():
                                    models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=str(i+1),dpt_id_id=str(fa))
                                else:
                                    message="book with the same name already exists"
                            except Exception as e:
                                    print(e)
                else:
                    if isin:
                        atrobj=models.Atr.objects.get(name=str(j))
                        models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=atrobj.a_id,dpt_id_id=str(fa))
                    else:
                        atrobj=models.Atr.objects.get(name=str(j))
                        models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=atrobj.a_id,dpt_id_id=str(fa))

            except Exception as e:
                if "does not" in str(e):
                    models.Bks.objects.create(b_id="IN_"+shortname+"_"+str(i+1),title=str(values[0]),desc=str(h),type="ref",edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]),email="library@mysite.edu",a_id_id=str(i+1),dpt_id_id=str(fa))
                print(e)
                pass
            
            try:
                g=0
                bookobj =models.Bks.objects.filter(title=str(values[0]),edition=str(values[1]),p_year=str(values[2]),pub=str(values[3]))
                testba = models.Invt.objects.values('id')   
                for test in testba:
                    if g>int(str(test['id'])):
                        g=g
                    else:
                        g=int(str(test['id']))
                               
                Invobj=models.Invt.objects.filter(i_id_id="IN_"+shortname+"_"+str(g+1))

                if len(bookobj) >= 0:
                    if(len(Invobj) == 0):
                          for s in bookobj:
                            models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id=s.b_id,shelf=str(c[0]),rack=str(c[1]),row=int(c[2]))
                    else:
                          for s in bookobj:
                            models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id=s.b_id,shelf=str(c[0]),rack=str(c[1]),row=int(c[2]))

                else:
                        models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id="IN_"+shortname+"_"+str(g+1),shelf=str(c[0]),rack=str(c[1]),row=int(c[2]))
            except Exception as e:
                try:
                    if "does not" in str(e):                     
                        models.Invt.objects.create(id=str(g+1),qty=int(z),i_id_id="IN_"+shortname+"_"+str(g+1),shelf=str(c[0]),rack=str(c[1]),row=int(c[2]))
                    else:
                        t=models.Invt.objects.get(i_id_id="IN_"+shortname+"_"+str(g+1))
                        t.qty=  t.qty+int(z)
                        t.save()
                except Exception as e:
                     print(e)
            
        else:
            message="the book details are not given properly"
            pass

    return render(
        request,
        'app/manageInv.html',
        {
           'title':'Manage Inventory',
            'invmodes':modes,
            'dispmode':'manage',
            'message':message,
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
             'books':get_valid_Books().values(),
            'year':datetime.now().year,
        }
    )


#Renders (index.html) and gives libraian ablity to order for sepecified book
#if only logged in and has the capability to view books and is a librarian 
def allbooks(request):
    """Renders the home page."""
    booklist=[]
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'books':get_valid_Books().keys(),
            'year':datetime.now().year,
        }
    )

#Renders (about.html) and gives user to search for books
#if only logged in and has the capability to view books
def genSearch(request):
    """Search for a book(S)"""
  
    assert isinstance(request, HttpRequest)
    booklist=[]
    form = request.GET.copy();
    searchvalue =form['query']
    for k,v in get_valid_Books().items():
        if searchvalue.lower() in v.title.lower() or searchvalue.lower() in v.desc.lower() or searchvalue.lower() in v.a_id.name.lower():
               booklist.append(v)
    if booklist is None:
         clearfilter="False"
    else:
        clearfilter="True"

    return render(
        request,
        'app/about.html',
        {
            'title':'Books',
            'books':booklist,
            'clearfilter':clearfilter,
            'year':datetime.now().year,
        }
    )
#Renders (about.html) and gives user to search for books in manage inv
#if only logged in and has the capability to view books 
def SearchdelInv(request):
    """Search for a book(S) to delete"""
  
    booklist=[]
    clearfilter=False
    form = request.GET.copy();
    searchvalue =form['query']
    
    for k,v in get_valid_Books().items():
        if searchvalue.lower() in v.title.lower() or searchvalue.lower() in v.desc.lower() or searchvalue.lower() in v.a_id.name.lower():
                booklist.append(v)
    if booklist is None:
            clearfilter="False"
    else:
        clearfilter="True"


    modes=['manage','add','order']
    departments={}
    for league in models.Dept.objects.all():          
                    departments[league.pk]=league
 
    displaymode="manage"
 
    
    return render(
        request,
        'app/manageInv.html',
        {
            'title':'Manage Inventory',
            'invmodes':modes,
            'dispmode':displaymode,
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
             'books':booklist,
             'clearfilter':clearfilter,
            'year':datetime.now().year,
        }
    )
#Renders (contact.html)
#Gives contact information
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Contact page.',
             'librarian':get_librarians(),
            'year':datetime.now().year,
        }
    )
#Renders (about.html) and gives user view books in inventory
#if only logged in and has the capability to view books 
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    booklist=[]
    if request.method == 'POST':
        form = request.GET.copy();
        searchvalue =form['query']
        for k,v in get_valid_Books().items():
            if searchvalue in k:
                   booklist.append(k)
    else:
         for k,v in get_valid_Books().items():
                 booklist.append(v)

    return render(
        request,
        'app/about.html',
        {
            'title':'Books',
            'message':'Application description With ability to search books and add to borrowlist.',
            'year':datetime.now().year,
            'books':booklist,
        }
    )
#Renders (manageInv.html) and gives librarian to view modules in inv
#if only logged in and has the capability to see inventory(meaning he should be a librarian)
def inv(request):
    """Renders the inventory page."""
    assert isinstance(request, HttpRequest)
    departments={}
    booklist=[]
    for league in models.Dept.objects.all():          
                    departments[league.pk]=league
    for k,v in get_valid_Books().items():
                 booklist.append(v)
    modes=['manage','add','order']
    postobj = request.POST.copy()
    modetype=""
    displaymode=""
    try:
        modetype=postobj['inventoryMode']
        if 'manage' in modetype.lower():
            
            return render(
        request,
        'app/manageInv.html',
        {
            'title':'Manage Inventory',
            'invmodes':modes,
            'dispmode':'manage',
            'message':'Manage Inventory details page.',
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
             'books':booklist,
            'year':datetime.now().year,
        }
    )
        elif 'add' in modetype.lower():
            return render(
        request,
        'app/addInv.html',
        {
            'title':'Add Inventory',
            'invmodes':modes,
            'dispmode':'add',
            'message':'Inventory page.',
             'librarian':get_librarians(),
             'le':list(range(1,11)),
             'DepartmentList':departments.keys(),
            'year':datetime.now().year,
        }
    )
        else:
            return render(
        request,
        'app/orderInv.html',
        {
            'title':'Order for new books',
            'invmodes':modes,
            'dispmode':'add',
            'message':'Order Books page (procurement).',
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
            'year':datetime.now().year,
        }
    )
    except Exception as e:
        return render(
        request,
        'app/manageInv.html',
        {
            'title':'Manage Inventory',
            'invmodes':modes,
            'dispmode':'manage',
            'message':'Manage Inventory details page.',
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
              'books':booklist,
             'year':datetime.now().year,
        }
    )
   
    return render(
        request,
        'app/inventory.html',
        {
            'title':'Inventory',
            'invmodes':modes,
            'dispmode':displaymode,
            'message':'Inventory details page.',
             'librarian':get_librarians(),
             'le':list(range(1,2)),
             'DepartmentList':departments.keys(),
            'year':datetime.now().year,
        }
    )



#Renders (profile.html) and gives logged in user his details
#if only logged in 
def profile(request):
    """Renders the profile page."""
    assert isinstance(request, HttpRequest)
    usera=[]
    myuser = request.user.username
    try:
        userdetails=models.Stud.objects.get(stu_id=myuser)
    except Exception as e:
        print(e)
    usera.append(userdetails.stu_name)
    usera.append(userdetails.short_id)
    usera.append(userdetails.dpt_id_id)
    usera.append(userdetails.gender)
    usera.append(userdetails.email)
    usera.append(userdetails.address)
    library_Cwid_id = models.Libmem.objects.get(cwid_id=myuser)
    borrowedbooks = models.Bowed.objects.filter(cwid_id=library_Cwid_id)
    
    



    return render(
        request,
        'app/profile.html',
        {
            'title':'User Details',
            'message':'profile page.',
            'year':datetime.now().year,
            'userdetails':usera,
            'borrowedbooks':list(borrowedbooks),
            'Active':User.is_active,
           
        }
    )
#Renders (signup.html) and gives user to view register mod
#if only logged in and has the capability to see inventory(meaning he should be a librarian)
def register(request,template_name="app/signup.html"):
   
    if request.method == 'POST':
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            postdata = request.POST.copy()
            username = postdata.get('username', '')[0:9]
            if len(postdata.get('username', ''))>9:
                messages.add_message(request,messages.INFO,"Error user name is has more charcter than specified going to trim  and fit ")
            email = postdata.get('email', '')
            password = postdata.get('password1','')
            
            if User.objects.filter(username=username).exists():
                username_unique_error = True
                
            if User.objects.filter(email=email).exists():
               email_unique_error = True
               
               
            else :
                collegename={}
                name=""
                if "cs" in  postdata.get('Department_ID','').lower():
                    name= "Computer Science"
                    collegename[name]="college of arts and science"
                elif "ce" in postdata.get('Department_ID','').lower():
                    name = "Computer engineering"
                    collegename[name]="college of Engineering"
                elif "ec" in postdata.get('Department_ID','').lower():
                    name = "Electrical comunication"
                    collegename[name]="college of Engineering"
                elif "ci" in postdata.get('Department_ID','').lower():
                    name = "Civil engineering"
                    collegename[name]="college of Engineering"
                else:
                    name="others"
                    collegename[name]="college of information science"
                deptObj = models.Dept(dpt_id=postdata.get('Department_ID',''),name= name,college_name=collegename[name])
                try:
                    deptObj.save()
                except:
                    print(Exception)
                dptinstance =models.Dept.objects.get(dpt_id=postdata.get('Department_ID',''))
                Stu_obj = models.Stud(stu_id=username,short_id=postdata.get('Short_ID',''),stu_name=postdata.get('Student_Full_Name',''),
                                      dpt_id=dptinstance,d_typ=postdata.get('Degree_type',''),gender=postdata.get('gender',''),
                                      email=postdata.get('email',''),address=postdata.get('address',''))
                try:
                    Stu_obj.save()
                except Exception as e:
                    print(e)
                Stuinstance =models.Stud.objects.get(short_id=postdata.get('Short_ID',''))
                Libmemobj = models.Libmem(cwid=Stuinstance,dpt_id=dptinstance)
                try:
                    Libmemobj.save()
                except Exception as e:
                    print(e)
                if "on" in postdata.get('libraian',''):
                    librarianobj = models.Librn(lb_id=username,name=postdata.get('Student_Full_Name',''),email=postdata.get('email',''),address=postdata.get('address',''),
                                                dpt_id=dptinstance,d_typ=postdata.get('Degree_type',''),gender=postdata.get('gender',''))

                    try:
                        librarianobj.save()
                    except Exception as e:
                          print(e)
                namefull= postdata.get('Student_Full_Name','')
                fname=namefull.split(" ")[0]
                lname=namefull.split(" ")[1]
                create_new_user = User.objects.create_user(username, email, password,last_name=lname,first_name=fname)
                create_new_user.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                if create_new_user is not None:
                    if create_new_user.is_active:
                        return redirect('home')
                    else:
                        print("The password is valid, but the account has been disabled!")

    else:
        form = forms.StudentForm()
     
    return render(request, template_name, {'form': form,'librarians':get_librarians()})