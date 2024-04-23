def salesreport_graph(request):
    if 'staff_id' in request.session:
        staff_id = request.session['staff_id']
    else:
        return redirect('/')

    staff = staff_details.objects.get(id=staff_id)
    company_instance = company.objects.get(id=staff.company.id)
    
    # Retrieve monthly sales data
    monthly_sales_data = defaultdict(int)
    for month in range(1, 13):
        monthly_sales_data[month] = (
            SalesInvoice.objects
            .filter(date__month=month)
            .aggregate(total_sales=Sum('grandtotal'))['total_sales'] or 0
        )

    # Retrieve yearly sales data
    current_year = datetime.now().year
    yearly_sales_data = defaultdict(int)
    for year in range(2022, current_year + 1):
        yearly_sales_data[year] = (
            SalesInvoice.objects
            .filter(date__year=year)
            .aggregate(total_sales=Sum('grandtotal'))['total_sales'] or 0
        )

    # Prepare data for chart
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_labels = [month_names[month - 1] for month in range(1, 13)]
    monthly_sales = [monthly_sales_data[month] for month in range(1, 13)]

    yearly_labels = [str(year) for year in range(2014, current_year + 1)]
    yearly_sales = [yearly_sales_data[year] for year in range(2014, current_year + 1)]

    # Prepare data for chart
    chart_data = {'monthly_labels': monthly_labels, 'monthly_sales': monthly_sales,
                  'yearly_labels': yearly_labels, 'yearly_sales': yearly_sales}
    return render(request, 'saleschart.html', {'chart_data': chart_data, 'staff': staff})