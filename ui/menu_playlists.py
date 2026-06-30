from services.playlist_servico import PlaylistServico
from services.musica_servico import MusicaServico
from ui.helpers import cabecalho, secao, opcoes, ler_int, ler_bool, pausar

_servico = PlaylistServico()
_musica_servico = MusicaServico()

def menu_playlists(usuario_logado):
    while True:
        cabecalho("📋  MINHAS PLAYLISTS")
        opcoes([
            ("1", "Ver minhas playlists"),
            ("2", "Criar playlist"),
            ("3", "Ver músicas de uma playlist"),
            ("4", "Adicionar música à playlist"),
            ("5", "Remover música da playlist"),
            ("6", "Editar playlist"),
            ("7", "Excluir playlist"),
            ("0", "Voltar"),
        ])
        op = input("  Opção: ").strip()
        if op == "1":
            _listar(usuario_logado)
        elif op == "2":
            _criar(usuario_logado)
        elif op == "3":
            _ver_musicas(usuario_logado)
        elif op == "4":
            _adicionar(usuario_logado)
        elif op == "5":
            _remover(usuario_logado)
        elif op == "6":
            _editar(usuario_logado)
        elif op == "7":
            _excluir(usuario_logado)
        elif op == "0":
            break
        else:
            print("  ⚠  Opção inválida.")
        pausar()

def _listar(usuario):
    secao("Minhas Playlists")
    playlists = _servico.listar_do_usuario(usuario.id)
    if not playlists:
        print("  Você não tem playlists.")
        return
    for pl in playlists:
        print(f"  [{pl.id:>3}] {pl}")

def _criar(usuario):
    secao("Criar Playlist")
    nome = input("  Nome: ").strip()
    descricao = input("  Descrição (opcional): ").strip() or None
    publica = ler_bool("  Tornar pública?")
    try:
        pl = _servico.criar(nome, usuario.id, descricao, publica)
        print(f"  ✅  Playlist '{pl.nome}' criada com id={pl.id}.")
    except Exception as e:
        print(f"  ⚠  {e}")

def _ver_musicas(usuario):
    secao("Músicas da Playlist")
    _listar(usuario)
    id_ = ler_int("  ID da playlist: ", minimo=1)
    try:
        midias = _servico.listar_midias(id_)
        if not midias:
            print("  Playlist vazia.")
            return
        total = sum(m.duracao_segundos for m in midias)
        for i, m in enumerate(midias, 1):
            print(f"  {i:>2}. {m}")
        minutos = total // 60
        segundos = total % 60
        print(f"\n  Total: {len(midias)} faixa(s) — {minutos}min {segundos:02d}s")
    except Exception as e:
        print(f"  ⚠  {e}")

def _adicionar(usuario):
    secao("Adicionar Música à Playlist")
    _listar(usuario)
    pl_id = ler_int("  ID da playlist: ", minimo=1)

    midias = _musica_servico.listar_midias()
    if not midias:
        print("  ⚠  Nenhuma mídia cadastrada no sistema.")
        return
    print("  Mídias disponíveis:")
    for m in midias:
        print(f"    [{m.id}] {m}")

    m_id = ler_int("  ID da mídia: ", minimo=1)
    try:
        _servico.adicionar_musica(pl_id, m_id, usuario.id)
        print("  ✅  Mídia adicionada à playlist.")
    except (ValueError, PermissionError) as e:
        print(f"  ⚠  {e}")

def _remover(usuario):
    secao("Remover Música da Playlist")
    _listar(usuario)
    pl_id = ler_int("  ID da playlist: ", minimo=1)
    midias = _servico.listar_midias(pl_id)
    if not midias:
        print("  Playlist vazia.")
        return
    for m in midias:
        print(f"    [{m.id}] {m}")
    m_id = ler_int("  ID da mídia a remover: ", minimo=1)
    try:
        _servico.remover_musica(pl_id, m_id, usuario.id)
        print("  ✅  Mídia removida.")
    except (ValueError, PermissionError) as e:
        print(f"  ⚠  {e}")

def _editar(usuario):
    secao("Editar Playlist")
    _listar(usuario)
    id_ = ler_int("  ID da playlist: ", minimo=1)
    nome = input("  Novo nome (ENTER para manter): ").strip() or None
    desc = input("  Nova descrição (ENTER para manter): ").strip() or None
    pub_str = input("  Pública? (s/n/ENTER para manter): ").strip().lower()
    publica = True if pub_str == "s" else (False if pub_str == "n" else None)
    try:
        _servico.atualizar(id_, usuario.id, nome, desc, publica)
        print("  ✅  Playlist atualizada.")
    except (ValueError, PermissionError) as e:
        print(f"  ⚠  {e}")

def _excluir(usuario):
    secao("Excluir Playlist")
    _listar(usuario)
    id_ = ler_int("  ID da playlist: ", minimo=1)
    if not ler_bool("  Confirmar exclusão?"):
        print("  Operação cancelada.")
        return
    try:
        _servico.excluir(id_, usuario.id)
        print("  ✅  Playlist excluída.")
    except (ValueError, PermissionError) as e:
        print(f"  ⚠  {e}")
