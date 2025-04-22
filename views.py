# views.py
from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils.timezone import now
import calendar

# Importa tu modelo Cliente (ajústalo al nombre real de tu app si es necesario)
from .models import Cliente

def dashboard(request):
    # Obtenemos los últimos 6 meses para el gráfico
    today = now()
    six_months_ago = today.replace(month=today.month - 5) if today.month > 5 else today.replace(year=today.year - 1, month=12 - (5 - today.month))

    clientes_por_mes_qs = Cliente.objects.filter(fecha_registro__gte=six_months_ago).annotate(
        mes=TruncMonth('fecha_registro')
    ).values('mes').annotate(total=Count('id')).order_by('mes')

    meses = []
    cantidades = []

    for entry in clientes_por_mes_qs:
        mes_nombre = calendar.month_name[entry['mes'].month]
        meses.append(mes_nombre)
        cantidades.append(entry['total'])

    # Aquí puedes agregar más datos si lo necesitas después
    context = {
        'meses': meses,
        'clientes_mes': cantidades,
    }

    return render(request, 'dashboard.html', context)
