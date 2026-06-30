def linha(char="─", largura=55):
    print(char * largura)

def cabecalho(titulo: str):
    linha("═")
    print(f"  {titulo}")
    linha("═")

def secao(titulo: str):
    linha()
    print(f"  {titulo}")
    linha()

def opcoes(itens: list[tuple[str, str]]):
    for tecla, desc in itens:
        print(f"  [{tecla}] {desc}")
    linha()

def ler_int(prompt: str, minimo: int = None, maximo: int = None) -> int:
    while True:
        try:
            valor = int(input(prompt).strip())
            if minimo is not None and valor < minimo:
                print(f"  ⚠  Valor mínimo: {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠  Valor máximo: {maximo}")
                continue
            return valor
        except ValueError:
            print("  ⚠  Digite um número inteiro.")

def ler_bool(prompt: str) -> bool:
    resp = input(f"{prompt} (s/n): ").strip().lower()
    return resp in ("s", "sim", "y", "yes")

def pausar():
    input("\n  ↵  Pressione ENTER para continuar...")
