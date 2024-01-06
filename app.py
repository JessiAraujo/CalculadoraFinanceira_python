from flask import Flask, render_template, request

app = Flask(__name__)

def calcular_taxa_juros(renda_mensal):
    # Lógica para calcular a taxa de juros com base na renda mensal
    if renda_mensal < 5000:
        return 5.0
    else:
        return 3.0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular_emprestimo', methods=['POST'])
def calcular_emprestimo():
    renda_mensal = float(request.form['renda_mensal'])

    # Validação de Renda
    if renda_mensal < 3000 or renda_mensal > 10000:
        return render_template('index.html', mensagem_erro='A renda deve estar entre R$ 3000 e R$ 10000')

    # Cálculo de Empréstimo
    valor_emprestimo = float(request.form['valor_emprestimo'])
    prazo_emprestimo = int(request.form['prazo_emprestimo'])

    # Lógica de cálculo de taxa de juros 
    taxa_juros = calcular_taxa_juros(renda_mensal)

    # Cálculo das prestações mensais
    prestacoes_mensais = calcular_prestacoes_mensais(valor_emprestimo, prazo_emprestimo, taxa_juros)

    # Detalhes do Empréstimo
    valor_negociado = valor_emprestimo
    total_saldo_devedor = calcular_total_saldo_devedor(valor_emprestimo, prazo_emprestimo, taxa_juros)
    valor_entrada = calcular_valor_entrada(valor_emprestimo)
    numero_parcelas = prazo_emprestimo

    return render_template('resultado.html',
                           prestacoes_mensais=round(prestacoes_mensais, 2),
                           valor_negociado=round(valor_negociado, 2),
                           total_saldo_devedor=round(total_saldo_devedor, 2),
                           valor_entrada=round(valor_entrada, 2),
                           numero_parcelas=numero_parcelas,
                           taxa_juros=taxa_juros)


def calcular_prestacoes_mensais(valor_emprestimo, prazo_emprestimo, taxa_juros):
    taxa_juros_mensal = taxa_juros / 12 / 100
    prestacao_mensal = (valor_emprestimo * taxa_juros_mensal) / (1 - (1 + taxa_juros_mensal) ** -prazo_emprestimo)
    return prestacao_mensal

def calcular_total_saldo_devedor(valor_emprestimo, prazo_emprestimo, taxa_juros):
    taxa_juros_mensal = taxa_juros / 12 / 100
    total_saldo_devedor = 0
    for i in range(1, prazo_emprestimo + 1):
        total_saldo_devedor += calcular_prestacoes_mensais(valor_emprestimo, i, taxa_juros)
    return total_saldo_devedor

def calcular_valor_entrada(valor_emprestimo):
    return valor_emprestimo * 0.05  # 5% do valor total

def calcular_custo_total_emprestimo(prestacoes_mensais, prazo_emprestimo):
    custo_total_emprestimo = prestacoes_mensais * prazo_emprestimo
    return custo_total_emprestimo


if __name__ == '__main__':
    app.run(debug=True)


