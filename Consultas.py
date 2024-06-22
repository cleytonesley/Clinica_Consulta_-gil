import os 
import json
from datetime import datetime

#constantes
PACIENTES_FILE = 'pacientes.json'
AGENDAMENTOS_FILE = 'agendamentos.json'

#funcção carregar dados json
def carregar_dados(file):
    if os.path.exists(file):
        with open(file,'r') as f:
            return json.load(f)
    return []   
 
#função saltar dados
def salvar_dados(file, data):
    with open (file,'w')as f:
        json.dump(data, f, indent=4)

#função menu
def menu():
    print("1. Cadastrar um paciente")
    print("2. Marcar uma consulta")
    print("3. Cancelar uma consulta")
    print("4. sair ")

#função cadastro paciente
def cadastrar_paciente():
    nome = input("Digite o nome do paciente:")
    telefone = input("Digite o telefone do paciente:")

    #verifar duplicidade
    pacientes = carregar_dados(PACIENTES_FILE)
    for paciente in pacientes:
        if paciente ['telefone'] == telefone:
            print("paciente já cadastrado! ")
            return
        
    #cadastrar novo paciente
    pacientes.append({'nome' :nome, 'telefone': telefone})
    salvar_dados(PACIENTES_FILE, pacientes)
    print("Paciente cadastrado com sucesso!")

def marcar_consulta():
    pacientes = carregar_dados(PACIENTES_FILE)
    if not pacientes:
        print("Nenhum paciente cadastrado!")
        return

    # Exibir lista de pacientes
    print("Pacientes cadastrados:")
    for idx, paciente in enumerate(pacientes):
        print(f"{idx + 1}. {paciente['nome']} ({paciente['telefone']})")

    escolha = int(input("Escolha o número do paciente: ")) - 1
    if escolha < 0 or escolha >= len(pacientes):
        print("Escolha inválida.")
        return

    paciente = pacientes[escolha]
    data = input("Digite a data da consulta (DD/MM/AAAA): ")
    hora = input("Digite a hora da consulta (HH:MM): ")
    especialidade = input("Digite a especialidade da consulta: ")

    # Validar a data e hora
    try:
        data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
        if data_hora < datetime.now():
            print("Data ou Hora inválida.")
            return
    except ValueError:
        print("Data e Hora inválidas")
        return

    # Verificar disponibilidade
    agendamentos = carregar_dados(AGENDAMENTOS_FILE)
    if not isinstance(agendamentos, list):
        print(f"Erro: o arquivo {AGENDAMENTOS_FILE} não contém uma lista válida de agendamentos.")
        return

    for agendamento in agendamentos:
        if 'data_hora' in agendamento and agendamento['data_hora'] == data_hora.strftime('%d/%m/%Y %H:%M'):
            print("Data e hora já agendadas.")
            return

    # Marcar consulta
    agendamentos.append({
        'paciente': paciente,
        'data_hora': data_hora.strftime('%d/%m/%Y %H:%M'),
        'especialidade': especialidade
    })
    salvar_dados(AGENDAMENTOS_FILE, agendamentos)
    print("Consulta marcada com sucesso!")
    
#cancelar consulta
def cancelar_consulta():
    agendamentos = carregar_dados(AGENDAMENTOS_FILE)
    if not agendamentos:
        print("Nenhuma consulta agendada")
        return
    
    # exibir lista de agendamentos
    print("consultas agendadas:")
    for idx, agendamento in enumerate(agendamentos):
        paciente = agendamento['paciente']
        print(f"{idx + 1}. {agendamento ['data_hora']} - {paciente['nome']} ({paciente['telefone']})- {agendamento['especialidade']}")
    
    escolha = int(input("Escolha o nume da consulta a cancelar: ")) -1    
    if escolha < 0 or escolha >= len(agendamentos):
      print("Escolha inválida") 
      return

    agendamento = agendamentos[escolha]
    confirmacao = input(f"confirmar cancelamento da consulta em {agendamento ['data_hora']} (s/n)? ").lower()
    if confirmacao == 's':
        del agendamentos [escolha] 
        salvar_dados(AGENDAMENTOS_FILE, agendamentos)
        print("Consulta cancelada com sucesso!")
    else:
        print("Cancelamento abordado!")

def main():
    while True:
        menu()
        escolha = input("escolha uma opção:")

        if escolha == '1':
            cadastrar_paciente()
        elif escolha == '2':
            marcar_consulta()
        elif escolha == '3':
            cancelar_consulta()
        elif escolha == '4':
            print("Encarregado o programa...")
            break
        else:
            print("Opção Invalida. Tente novamente.")    

#execatar programa
main()
    
 




