from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Customer

# Create your views here.


@login_required
def records(request):
    customers = Customer.objects.filter(created_by=request.user)

    return render(
        request,
        "customers/records.html",
        {
            "customers": customers,
        },
    )


@login_required
def add_records(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        country = request.POST.get("country", "")

        if first_name and last_name and address and city and country:
            Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                address=address,
                city=city,
                country=country,
                created_by=request.user,
            )

            return redirect("/")

    return render(request, "customers/add_records.html", {})


@login_required
def record(request, pk):
    customer = Customer.objects.filter(created_by=request.user).get(pk=pk)
    return render(
        request,
        "customers/record.html",
        {
            "customer": customer,
        },
    )


# Individual Customer


@login_required
def edit(request, pk):
    customer = Customer.objects.filter(created_by=request.user).get(pk=pk)

    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        country = request.POST.get("country", "")

        if first_name and last_name and address and city and country:
            customer.first_name = first_name
            customer.last_name = last_name
            customer.address = address
            customer.city = city
            customer.country = country
            customer.save()

            return redirect(f"/customers/{customer.id}")

    return render(request, "customers/edit.html", {"customer": customer})


@login_required
def delete(request, pk):
    customer = Customer.objects.filter(created_by=request.user).get(pk=pk)
    customer.delete()

    return redirect("/customers/")
