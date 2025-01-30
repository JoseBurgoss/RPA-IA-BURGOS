import pandas as pd
from twilio.rest import Client
import matplotlib.pyplot as plt

account_sid = 'AC45ae07a2e090e21a6ce8024700e38dd3'
auth_token = '0d210a195c31c53c3e165694edb52ce2'
client = Client(account_sid, auth_token)

lista_meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio']
vendedores = []
ventas_totales = []

for mes in lista_meses:
    tabla_ventas = pd.read_excel(f'RPA-IA-BURGOS/Ventas/{mes}.xlsx')
    
    idx_max = tabla_ventas['Ventas'].idxmax()
    vendedor = tabla_ventas.loc[idx_max, 'Vendedor']
    ventas = tabla_ventas.loc[idx_max, 'Ventas']
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+584140629243',
        body=f'En el mes de {mes}, {vendedor} llevo a cabo mas ventas, Ventas: {ventas}$'
    )
    print(message.sid)
    
    if vendedor not in vendedores:
        vendedores.append(vendedor)
        ventas_totales.append(ventas)
    else:
        index = vendedores.index(vendedor)
        ventas_totales[index] += ventas

plt.figure(figsize=(10, 6))
plt.bar(vendedores, ventas_totales, color='skyblue')
plt.xlabel('Vendedores')
plt.ylabel('Ventas Totales ($)')
plt.title('Ventas Totales por Vendedor')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

ventas_por_mes = []
for mes in lista_meses:
    tabla_ventas = pd.read_excel(f'RPA-IA-BURGOS/Ventas/{mes}.xlsx')
    ventas_mes = tabla_ventas['Ventas'].sum()
    ventas_por_mes.append(ventas_mes)

plt.figure(figsize=(10, 6))
plt.plot(lista_meses, ventas_por_mes, marker='o', linestyle='-', color='b')
plt.xlabel('Meses')
plt.ylabel('Ventas Totales ($)')
plt.title('Evolución de las Ventas Totales por Mes')
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 8))
plt.pie(ventas_totales, labels=vendedores, autopct='%1.1f%%', startangle=140)
plt.title('Proporción de Ventas Totales por Vendedor')
plt.show()
