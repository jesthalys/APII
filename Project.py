import sqlite3

def verificar_e_criar_banco():
    conn = sqlite3.connect('portal_saude.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS unidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cidade TEXT NOT NULL,
        especialidade TEXT,
        endereco TEXT
    )
    ''')
    conn.commit()
    conn.close()

def conectar():
    return sqlite3.connect('portal_saude.db')

def cadastrar():
    print("\n--- NOVO CADASTRO ---")
    nome = input("Nome da Unidade: ")
    cidade = input("Cidade (Crato/Juazeiro/Barbalha): ").strip().title()
    esp = input("Especialidade: ")
    end = input("Endereço: ")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO unidades (nome, cidade, especialidade, endereco) VALUES (?, ?, ?, ?)", 
                   (nome, cidade, esp, end))
    conn.commit()
    conn.close()
    print(f"\n✅ {nome} cadastrado com sucesso!")

def listar_todas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unidades")
    dados = cursor.fetchall()
    conn.close()
    
    if dados:
        exibir_tabela(dados)
    else:
        print("\n📭 O banco de dados está vazio.")

def excluir_unidade():
    listar_todas()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM unidades")
    tem_dados = cursor.fetchone()
    conn.close()

    if not tem_dados:
        return

    id_unidade = input("\nDigite o ID da unidade que deseja EXCLUIR: ")
    confirmar = input(f"Tem certeza que deseja excluir a unidade ID {id_unidade}? (s/n): ").lower()
    
    if confirmar == 's':
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM unidades WHERE id = ?", (id_unidade,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"\n🗑️ Unidade ID {id_unidade} removida com sucesso!")
        else:
            print("\n⚠️ ID não encontrado.")
        conn.close()
    else:
        print("\nOperação cancelada.")

def exibir_tabela(dados):
    print("\n" + "="*75)
    print(f"{'ID':<3} | {'NOME':<25} | {'CIDADE':<15} | {'ESPECIALIDADE':<20}")
    print("-" * 75)
    for linha in dados:
        print(f"{linha[0]:<3} | {linha[1]:<25} | {linha[2]:<15} | {linha[3]:<20}")
    print("="*75)

def menu():
    verificar_e_criar_banco()
    
    while True:
        print("\n🏥 PORTAL SAÚDE CONECTADA - TRILINK CARIRI")
        print("1. Cadastrar nova unidade")
        print("2. Listar todas as unidades")
        print("3. Excluir unidade")
        print("4. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            cadastrar()
        elif opcao == '2':
            listar_todas()
        elif opcao == '3':
            excluir_unidade()
        elif opcao == '4':
            print("\nEncerrando o portal... Até logo!")
            break
        else:
            print("\n⚠️ Opção inválida.")

if __name__ == "__main__":
    menu()
