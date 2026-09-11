import streamlit as st
from groq import Groq
from datetime import datetime, date, timedelta
import json
import random

st.set_page_config(page_title="TUTOR DE CONCURSOS IA", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#FDFAF6; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#92400E,#78350F) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#78350F,#5C2D0A) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#3D2B1F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#FDF8F0,#FAF0E6); padding:20px; border-radius:14px; border:1px solid #D4B896; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#3D2B1F !important; }

    .card-dark { background:linear-gradient(135deg,#FAF0E6,#F5E6D3); padding:20px; border-radius:14px; border:1px solid #C4956A; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#3D2B1F !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #D4B896; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#3D2B1F !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #D4B896; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#3D2B1F !important; }

    .badge { background:#92400E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#D4B896,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #D4B896; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#3D2B1F !important; }

    .chat-persona { background:#FDFAF6; border:1px solid #D4B896; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#3D2B1F !important; }

    .questao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#3D2B1F !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#3D2B1F !important; }

    .meta-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#3D2B1F !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache_tutor():
    return {"perfis": {}}
_cache = get_cache_tutor()

# ─── NÍVEIS E XP ───
NIVEIS = [
    (0,    "Iniciante",   "🌱"),
    (100,  "Aprendiz",    "📚"),
    (300,  "Persistente", "💪"),
    (600,  "Estudioso",   "🎯"),
    (1000, "Especialista","⭐"),
    (1500, "Elite",       "🏆"),
    (2500, "Aprovado",    "🎓"),
]
XP_ATIVIDADES = {
    'questao_certa': 10, 'questao_errada': 2, 'resumo': 20,
    'flashcard': 15, 'simulado': 50, 'revisao': 15,
    'plano': 25, 'mapa_mental': 20, 'missao_dia': 30,
}

def calcular_nivel(xp: int):
    nivel_atual = NIVEIS[0]
    for req_xp, nome, emoji in NIVEIS:
        if xp >= req_xp:
            nivel_atual = (req_xp, nome, emoji)
    return nivel_atual

def xp_proximo_nivel(xp: int):
    for i, (req_xp, nome, emoji) in enumerate(NIVEIS):
        if xp < req_xp:
            return req_xp
    return NIVEIS[-1][0]

# ─── CONQUISTAS ───
CONQUISTAS_DEF = [
    ("primeira_questao",   "🎯 Primeira Questão",      "Respondeu sua primeira questão"),
    ("questoes_100",       "💯 Centenário",             "100 questões respondidas"),
    ("questoes_1000",      "🏆 Guerreiro",              "1.000 questões respondidas"),
    ("primeiro_resumo",    "📝 Primeiro Resumo",        "Criou seu primeiro resumo"),
    ("primeiro_plano",     "📅 Planejador",             "Criou seu primeiro plano de estudos"),
    ("primeiro_simulado",  "📊 Simulador",              "Realizou seu primeiro simulado"),
    ("streak_7",           "🔥 7 Dias",                 "7 dias consecutivos de estudo"),
    ("streak_30",          "⚡ 30 Dias",                "30 dias consecutivos de estudo"),
    ("horas_100",          "⏱️ 100 Horas",              "100 horas de estudo acumuladas"),
    ("acerto_90",          "🎯 Mira Certeira",          "Taxa de acerto acima de 90%"),
    ("especialista_mat",   "🔢 Especialista em Matemática", "Acerto >80% em Matemática"),
    ("especialista_port",  "📖 Especialista em Português",  "Acerto >80% em Português"),
    ("especialista_dir",   "⚖️ Especialista em Direito",    "Acerto >80% em Direito"),
    ("nivel_elite",        "🌟 Elite",                  "Atingiu o nível Elite"),
    ("aprovado",           "🎓 Aprovado",               "Atingiu o nível Aprovado"),
]

def verificar_conquistas():
    conquistadas = st.session_state.get('conquistas', [])
    novas = []
    q = st.session_state.questoes_respondidas
    xp = st.session_state.pontuacao_total
    streak = st.session_state.get('streak_atual', 0)
    horas = st.session_state.get('horas_acumuladas', 0)
    taxa = (st.session_state.questoes_certas / max(q,1)) * 100

    checks = [
        ("primeira_questao", q >= 1),
        ("questoes_100", q >= 100),
        ("questoes_1000", q >= 1000),
        ("primeiro_resumo", any(e['tipo']=='Resumo' for e in st.session_state.historico_estudos)),
        ("primeiro_plano", any(e['tipo']=='Plano' for e in st.session_state.historico_estudos)),
        ("primeiro_simulado", any(e['tipo']=='Simulado' for e in st.session_state.historico_estudos)),
        ("streak_7", streak >= 7),
        ("streak_30", streak >= 30),
        ("horas_100", horas >= 100),
        ("acerto_90", taxa >= 90 and q >= 20),
        ("nivel_elite", xp >= 1500),
        ("aprovado", xp >= 2500),
    ]
    for chave, condicao in checks:
        if condicao and chave not in conquistadas:
            conquistadas.append(chave)
            novas.append(chave)
    st.session_state['conquistas'] = conquistadas
    return novas

def calcular_indice_preparacao():
    q = st.session_state.questoes_respondidas
    xp = st.session_state.pontuacao_total
    streak = st.session_state.get('streak_atual', 0)
    horas = st.session_state.get('horas_acumuladas', 0)
    taxa = (st.session_state.questoes_certas / max(q,1)) * 100 if q > 0 else 0

    score = 0
    score += min(taxa * 0.35, 35)
    score += min((q / 500) * 25, 25)
    score += min((horas / 200) * 20, 20)
    score += min((streak / 30) * 10, 10)
    score += min((xp / 2000) * 10, 10)
    return int(min(score, 100))

def classificar_indice(idx):
    if idx >= 85: return "Elite", "Muito Alta", "#059669"
    if idx >= 70: return "Avançado", "Alta", "#16A34A"
    if idx >= 55: return "Intermediário", "Moderada", "#D97706"
    if idx >= 40: return "Básico", "Baixa", "#EA580C"
    return "Iniciante", "Muito Baixa", "#DC2626"

MOTIVACOES = [
    "Cada questão respondida hoje é um passo que seu concorrente não deu.",
    "A aprovação não acontece em um dia — ela acontece em cada dia.",
    "Disciplina é escolher, repetidamente, o que importa sobre o que é fácil.",
    "O estudo de hoje é o cargo de amanhã.",
    "Você não está competindo com os outros — está competindo com quem você era ontem.",
    "Consistência vence talento quando o talento não é consistente.",
    "Cada hora estudada reduz a distância entre você e a aprovação.",
    "A banca não mede esforço — mede domínio. Domine.",
    "O candidato que estuda agora é o servidor que comemora depois.",
    "Cansaço é temporário. Aprovação é permanente.",
]

# ─── PERSISTÊNCIA ───
CHAVES_SALVAR = [
    'usuario','historico_estudos','biblioteca_materiais',
    'concurso_foco','materias_foco','horas_disponiveis',
    'nivel_conhecimento','data_prova','cargo_foco','nota_necessaria',
    'dias_disponiveis','experiencia_anterior','maior_dificuldade',
    'maior_facilidade','metodo_preferido','instituicao',
    'pontuacao_total','questoes_respondidas','questoes_certas',
    'streak_atual','maior_streak','horas_acumuladas',
    'ultima_atividade','dias_estudo','conquistas',
    'radar_materias','missao_hoje','meta_semanal_h',
    'meta_semanal_q','horas_semana','questoes_semana',
    'historico_simulados',
]

def gerar_json_sessao():
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(u):
    _cache["perfis"][u] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(u):
    return _cache["perfis"].get(u)

def salvar_estudo(tipo, materia, conteudo):
    st.session_state.historico_estudos.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo, 'materia': materia, 'conteudo': conteudo,
    })
    st.session_state['ultima_atividade'] = f"{tipo} — {materia}"
    st.session_state['dias_estudo'] = st.session_state.get('dias_estudo', 0) + 1

def ganhar_xp(atividade: str, quantidade: int = 1):
    xp = XP_ATIVIDADES.get(atividade, 10) * quantidade
    st.session_state.pontuacao_total = st.session_state.get('pontuacao_total', 0) + xp
    novas = verificar_conquistas()
    return xp, novas

def atualizar_streak():
    hoje = date.today().isoformat()
    ultimo_dia = st.session_state.get('ultimo_dia_estudo', '')
    if ultimo_dia == hoje:
        return
    ontem = (date.today() - timedelta(days=1)).isoformat()
    if ultimo_dia == ontem:
        st.session_state.streak_atual = st.session_state.get('streak_atual', 0) + 1
    else:
        st.session_state.streak_atual = 1
    if st.session_state.streak_atual > st.session_state.get('maior_streak', 0):
        st.session_state.maior_streak = st.session_state.streak_atual
    st.session_state['ultimo_dia_estudo'] = hoje

# ─── DEFAULTS ───
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_estudos': [], 'biblioteca_materiais': [],
    'concurso_foco': "", 'materias_foco': "", 'horas_disponiveis': "2",
    'nivel_conhecimento': "Iniciante", 'data_prova': "", 'cargo_foco': "",
    'nota_necessaria': "", 'dias_disponiveis': "5", 'experiencia_anterior': "Nenhuma",
    'maior_dificuldade': "", 'maior_facilidade': "", 'metodo_preferido': "Misto",
    'instituicao': "",
    'pontuacao_total': 0, 'questoes_respondidas': 0, 'questoes_certas': 0,
    'streak_atual': 0, 'maior_streak': 0, 'horas_acumuladas': 0,
    'ultima_atividade': "Nenhuma", 'dias_estudo': 0, 'conquistas': [],
    'radar_materias': {}, 'missao_hoje': None, 'ultimo_dia_estudo': '',
    'meta_semanal_h': 10, 'meta_semanal_q': 100,
    'horas_semana': 0, 'questoes_semana': 0,
    'questoes_ativas': [], 'respondendo_idx': 0, 'respostas_sessao': [],
    'historico_simulados': [],
    'relampago_historico': [],
    'relampago_fase': 'menu',
    'relampago_tema': '',
    'relampago_modo': 'Desafio',
    'relampago_planejamento': {},
    'relampago_redacao': '',
    'relampago_aval_plano': '',
    'relampago_aval_redacao': '',
    'smc_fase': 'menu',
    'smc_questoes': [],
    'smc_respostas': {},
    'smc_inicio': 0,
    'smc_duracao': 3600,
    'smc_materia': '',
    'smc_n': 10,
    'smc_resultado': None,
    'smc_historico': [],

    'relampago_duracao': 0,
    'relampago_inicio': None,
    'simulado_ativo': False,
    'smc_escolha': None,
    'smc_idx': 0,
    'smc_vistas': None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── MOTOR DE IA ───
def tutor_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        perfil = (
            f"Aluno: {st.session_state.usuario}. "
            f"Concurso: {st.session_state.concurso_foco or 'não definido'}. "
            f"Cargo: {st.session_state.cargo_foco or 'não definido'}. "
            f"Nível: {st.session_state.nivel_conhecimento}. "
            f"Matérias foco: {st.session_state.materias_foco or 'não definidas'}. "
            f"Maior dificuldade: {st.session_state.maior_dificuldade or 'não informada'}. "
            f"Método preferido: {st.session_state.metodo_preferido}. "
            f"Índice de preparação: {calcular_indice_preparacao()}%. "
            f"XP: {st.session_state.pontuacao_total}. "
            f"Taxa de acerto: {int(st.session_state.questoes_certas/max(st.session_state.questoes_respondidas,1)*100)}%."
        )
        system = (
            f"Você é o Tutor de Concursos IA — um mentor estratégico de preparação para concursos públicos brasileiros. "
            f"Você acompanha toda a jornada do aluno, identifica padrões, explica o raciocínio por trás de cada decisão "
            f"e mantém o foco no objetivo final: a aprovação. "
            f"Sempre baseie conselhos no perfil real do aluno. Nunca seja genérico. "
            f"Português do Brasil. {perfil} {system_extra}"
        )
        response = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# ─── BARRA SALVAR ───
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_u = st.session_state.usuario.lower().replace(' ','_') or 'sessao'
    col_info, col_btn = st.columns([4, 2])
    with col_info:
        xp = st.session_state.pontuacao_total
        _, nivel_nome, nivel_emoji = calcular_nivel(xp)
        concurso = st.session_state.concurso_foco or "—"
        st.markdown(
            f"<div style='background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Salve seus dados antes de sair.</strong><br>"
            f"<span style='color:#D97706;font-size:0.88em;'>{nivel_emoji} {nivel_nome} · "
            f"{xp} XP · {concurso}</span>"
            f"</div>", unsafe_allow_html=True)
    with col_btn:
        st.download_button("💾 SALVAR DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"tutor_{nome_u}.json", mime="application/json", use_container_width=True, key="tutorcon26")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)


# ============================================================
# LOGIN
# ============================================================
if 'biblioteca_materiais' not in st.session_state: st.session_state['biblioteca_materiais'] = None
if 'cargo_foco' not in st.session_state: st.session_state['cargo_foco'] = None
if 'concurso_foco' not in st.session_state: st.session_state['concurso_foco'] = None
if 'data_prova' not in st.session_state: st.session_state['data_prova'] = None
if 'dias_disponiveis' not in st.session_state: st.session_state['dias_disponiveis'] = 0
if 'experiencia_anterior' not in st.session_state: st.session_state['experiencia_anterior'] = None
if 'historico_estudos' not in st.session_state: st.session_state['historico_estudos'] = []
if 'horas_acumuladas' not in st.session_state: st.session_state['horas_acumuladas'] = None
if 'horas_disponiveis' not in st.session_state: st.session_state['horas_disponiveis'] = None
if 'horas_semana' not in st.session_state: st.session_state['horas_semana'] = 0
if 'instituicao' not in st.session_state: st.session_state['instituicao'] = None
if 'maior_dificuldade' not in st.session_state: st.session_state['maior_dificuldade'] = None
if 'maior_facilidade' not in st.session_state: st.session_state['maior_facilidade'] = None
if 'maior_streak' not in st.session_state: st.session_state['maior_streak'] = None
if 'materias_foco' not in st.session_state: st.session_state['materias_foco'] = None
if 'meta_semanal_h' not in st.session_state: st.session_state['meta_semanal_h'] = 0
if 'metodo_preferido' not in st.session_state: st.session_state['metodo_preferido'] = None
if 'missao_hoje' not in st.session_state: st.session_state['missao_hoje'] = None
if 'nivel_conhecimento' not in st.session_state: st.session_state['nivel_conhecimento'] = None
if 'nota_necessaria' not in st.session_state: st.session_state['nota_necessaria'] = None
if 'pontuacao_total' not in st.session_state: st.session_state['pontuacao_total'] = 0
if 'questoes_certas' not in st.session_state: st.session_state['questoes_certas'] = []
if 'questoes_respondidas' not in st.session_state: st.session_state['questoes_respondidas'] = []
if 'questoes_semana' not in st.session_state: st.session_state['questoes_semana'] = []
if 'radar_materias' not in st.session_state: st.session_state['radar_materias'] = None
if 'relampago_aval_redacao' not in st.session_state: st.session_state['relampago_aval_redacao'] = None
if 'relampago_duracao' not in st.session_state: st.session_state['relampago_duracao'] = None
if 'relampago_fase' not in st.session_state: st.session_state['relampago_fase'] = None
if 'relampago_inicio' not in st.session_state: st.session_state['relampago_inicio'] = None
if 'relampago_redacao' not in st.session_state: st.session_state['relampago_redacao'] = None
if 'relampago_tema' not in st.session_state: st.session_state['relampago_tema'] = None
if 'simulado_ativo' not in st.session_state: st.session_state['simulado_ativo'] = False
if 'smc_duracao' not in st.session_state: st.session_state['smc_duracao'] = None
if 'smc_escolha' not in st.session_state: st.session_state['smc_escolha'] = None
if 'smc_fase' not in st.session_state: st.session_state['smc_fase'] = None
if 'smc_historico' not in st.session_state: st.session_state['smc_historico'] = []
if 'smc_idx' not in st.session_state: st.session_state['smc_idx'] = 0
if 'smc_inicio' not in st.session_state: st.session_state['smc_inicio'] = None
if 'smc_materia' not in st.session_state: st.session_state['smc_materia'] = None
if 'smc_questoes' not in st.session_state: st.session_state['smc_questoes'] = []
if 'smc_respostas' not in st.session_state: st.session_state['smc_respostas'] = {}
if 'smc_resultado' not in st.session_state: st.session_state['smc_resultado'] = None
if 'smc_vistas' not in st.session_state: st.session_state['smc_vistas'] = None
if 'streak_atual' not in st.session_state: st.session_state['streak_atual'] = None

if 'historico_redacoes' not in st.session_state: st.session_state['historico_redacoes'] = []
if 'quiz_banco' not in st.session_state: st.session_state['quiz_banco'] = []
if 'quiz_idx' not in st.session_state: st.session_state['quiz_idx'] = 0
if 'quiz_acertos' not in st.session_state: st.session_state['quiz_acertos'] = 0
if 'quiz_erros' not in st.session_state: st.session_state['quiz_erros'] = []
if 'quiz_respondida' not in st.session_state: st.session_state['quiz_respondida'] = False
if 'quiz_resposta_atual' not in st.session_state: st.session_state['quiz_resposta_atual'] = None
if 'historico_simulados' not in st.session_state: st.session_state['historico_simulados'] = []
if 'red_ativo' not in st.session_state: st.session_state['red_ativo'] = False

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 TUTOR DE CONCURSOS IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 quizcompremios.com.br</div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":

    atualizar_streak()


    # TABS — navegação nativa
    (_tab_Home, _tab_Questoes, _tab_Redacao, _tab_Simulado, _tab_Cronograma, _tab_Flashcards, _tab_Progresso, _tab_Legislacao, _tab_Informatica, _tab_Portugues, _tab_Matematica, _tab_Atualidades) = st.tabs(['🏠 Painel', '📝 Questões', '✍️ Redação', '🎯 Simulado', '📅 Cronograma', '🃏 Flashcards', '📈 Progresso', '⚖️ Legislação', '💻 Informática', '📖 Português', '🔢 Matemática', '📰 Atualidades'])

    with _tab_Home:
        col_u, col_r = st.columns([3,1])
        with col_u:
            st.title(f"🎓 Olá, {st.session_state.usuario}!")
            concurso = st.session_state.concurso_foco or "Não definido"
            xp = st.session_state.pontuacao_total
            _, nivel_nome, nivel_emoji = calcular_nivel(xp)
            st.markdown(f"<span class='badge'>{nivel_emoji} {nivel_nome}</span> <span class='badge-azul'>🎯 {concurso}</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="tutorcon3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if not st.session_state.concurso_foco:
            st.markdown("""<div style="background:#FFFBEB;border:2px solid #F59E0B;border-radius:12px;
            padding:16px 20px;margin-bottom:16px;">
            <span style='font-size:1em;font-weight:600;color:#92400E;'>
            ⚡ Comece pelo 📋 Perfil — configure seu concurso, matérias e data da prova para ativar todos os recursos.
            </span></div>""", unsafe_allow_html=True)
        else:
            # RECUPERAR BACKUP
            if len(st.session_state.historico_estudos) == 0:
                arq_home = st.file_uploader("Restaurar Backup (.json):", type=["json"], key="upload_home")
                if arq_home is not None:
                    try:
                        d = json.load(arq_home)
                        carregar_json_sessao(d)
                        salvar_perfil_cache(st.session_state.usuario)
                        st.success("✅ Backup restaurado!")
                        st.rerun()
                    except Exception:
                        st.error("Arquivo inválido.")

        # CABEÇALHO INSTITUCIONAL
        dias_restantes = "—"
        if st.session_state.data_prova:
            try:
                dp = datetime.strptime(st.session_state.data_prova, "%Y-%m-%d").date()
                dias_restantes = (dp - date.today()).days
                if dias_restantes < 0:
                    dias_restantes = "Prova passada"
            except Exception:
                dias_restantes = "—"

        ultima = st.session_state.get('ultima_atividade', 'Nenhuma')
        st.markdown(f"""
        <div class='painel-exec'>
            <div style='font-size:0.85em;opacity:0.7;letter-spacing:2px;margin-bottom:8px;'>🎓 MENTOR INTELIGENTE DE ESTUDOS</div>
            <div style='font-size:1.1em;opacity:0.7;margin-bottom:16px;'>Seu treinador pessoal com Inteligência Artificial · <span style='color:#22C55E;'>🟢 IA Online</span></div>
            <div style='display:flex;flex-wrap:wrap;gap:20px;'>
                <div><div style='font-size:0.75em;opacity:0.6;'>🎯 OBJETIVO</div><div style='font-size:1.1em;font-weight:700;'>{st.session_state.concurso_foco or "—"} {("— " + st.session_state.cargo_foco) if st.session_state.cargo_foco else ""}</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>📅 DIAS RESTANTES</div><div style='font-size:1.1em;font-weight:700;'>{dias_restantes}</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>🔥 SEQUÊNCIA</div><div style='font-size:1.1em;font-weight:700;'>{st.session_state.get("streak_atual",0)} dias</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>📖 ÚLTIMA ATIVIDADE</div><div style='font-size:1.1em;font-weight:700;'>{ultima}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ÍNDICE DE PREPARAÇÃO
        idx = calcular_indice_preparacao()
        nivel_idx, prob, cor = classificar_indice(idx)
        col_idx, col_mot = st.columns([1, 2])
        with col_idx:
            st.markdown(f"""
            <div class='indice-box'>
                <div style='font-size:0.85em;opacity:0.8;'>ÍNDICE DE PREPARAÇÃO</div>
                <div class='indice-numero'>{idx}%</div>
                <div style='font-size:0.9em;'>Nível: <strong>{nivel_idx}</strong></div>
                <div style='font-size:0.85em;opacity:0.8;'>Prob. estimada: {prob}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_mot:
            frase_mot = random.choice(MOTIVACOES)
            streak = st.session_state.get('streak_atual', 0)
            if streak > 0:
                frase_mot = f"Você está há {streak} dias consecutivos estudando. {frase_mot}"
            st.markdown(f"<div class='card' style='height:120px;display:flex;align-items:center;'><em>💡 {frase_mot}</em></div>", unsafe_allow_html=True)

        # DASHBOARD
        st.markdown("### 📊 Dashboard")
        q = st.session_state.questoes_respondidas
        c_q = st.session_state.questoes_certas
        e_q = q - c_q
        taxa = int(c_q/max(q,1)*100)
        xp = st.session_state.pontuacao_total
        horas = st.session_state.get('horas_acumuladas', 0)
        resumos = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Resumo')
        flashcards = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Flashcard')
        simulados = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Simulado')
        cronogramas = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Plano')

        d1,d2,d3,d4,d5,d6 = st.columns(6)
        d1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('streak_atual',0)}</div><div>Dias seguidos</div></div>", unsafe_allow_html=True)
        d2.markdown(f"<div class='stat-box'><div class='stat-numero'>{horas:.0f}h</div><div>Horas acumuladas</div></div>", unsafe_allow_html=True)
        d3.markdown(f"<div class='stat-box'><div class='stat-numero'>{q}</div><div>Questões</div></div>", unsafe_allow_html=True)
        d4.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa}%</div><div>Acertos</div></div>", unsafe_allow_html=True)
        d5.markdown(f"<div class='stat-box'><div class='stat-numero'>{resumos}</div><div>Resumos</div></div>", unsafe_allow_html=True)
        d6.markdown(f"<div class='stat-box'><div class='stat-numero'>{xp}</div><div>XP Total</div></div>", unsafe_allow_html=True)

        d7,d8,d9,d10,d11,d12 = st.columns(6)
        d7.markdown(f"<div class='stat-box'><div class='stat-numero'>{flashcards}</div><div>Flashcards</div></div>", unsafe_allow_html=True)
        d8.markdown(f"<div class='stat-box'><div class='stat-numero'>{simulados}</div><div>Simulados</div></div>", unsafe_allow_html=True)
        d9.markdown(f"<div class='stat-box'><div class='stat-numero'>{cronogramas}</div><div>Planos</div></div>", unsafe_allow_html=True)
        d10.markdown(f"<div class='stat-box'><div class='stat-numero'>{c_q}</div><div>Certas</div></div>", unsafe_allow_html=True)
        d11.markdown(f"<div class='stat-box'><div class='stat-numero'>{e_q}</div><div>Erradas</div></div>", unsafe_allow_html=True)
        d12.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('maior_streak',0)}</div><div>Recorde dias</div></div>", unsafe_allow_html=True)

        # MISSÃO DO DIA
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_miss, col_meta = st.columns(2)
        with col_miss:
            st.markdown("### ⚡ Missão do Dia")
            if not st.session_state.get('missao_hoje'):
                if st.button("⚡ GERAR MISSÃO DO DIA", key="tutorcon4"):
                    with st.spinner("Gerando missão personalizada..."):
                        materia_critica = st.session_state.maior_dificuldade or st.session_state.materias_foco or "a matéria mais importante do seu concurso"
                        missao_prompt = (
                            f"Crie uma missão de estudo para hoje para o aluno preparando {st.session_state.concurso_foco or 'concurso público'}.\n"
                            f"Horas disponíveis: {st.session_state.horas_disponiveis}h. Maior dificuldade: {materia_critica}.\n"
                            f"Formato:\n\n"
                            f"⚡ MISSÃO DO DIA\n\n"
                            f"[3-4 tarefas específicas com tempo estimado cada]\n\n"
                            f"⏱️ Tempo total previsto: [X]h[Y]min\n"
                            f"🏆 Recompensa: +[XP] XP\n\n"
                            f"💡 Por que essa missão hoje: [1 linha explicando a estratégia]"
                        )
                        missao = tutor_ia(missao_prompt)
                        st.session_state.missao_hoje = missao
                        st.rerun()
            else:
                st.markdown(f"<div class='missao-box'>{st.session_state.missao_hoje}</div>", unsafe_allow_html=True)
                col_ok, col_re = st.columns(2)
                with col_ok:
                    if st.button("✅ MISSÃO CONCLUÍDA!", key="missao_ok"):
                        xp_g, novas = ganhar_xp('missao_dia')
                        st.success(f"🏆 +{xp_g} XP! Excelente trabalho!")
                        st.session_state.missao_hoje = None
                        st.rerun()
                with col_re:
                    if st.button("🔄 Nova missão", key="missao_re"):
                        st.session_state.missao_hoje = None
                        st.rerun()

        with col_meta:
            st.markdown("### 📆 Meta Semanal")
            h_prev = st.session_state.get('meta_semanal_h', 10)
            h_feito = st.session_state.get('horas_semana', 0)
            q_prev = st.session_state.get('meta_semanal_q', 100)
            q_feito = st.session_state.get('questoes_semana', 0)
            pct_h = min(int(h_feito/max(h_prev,1)*100), 100)
            pct_q = min(int(q_feito/max(q_prev,1)*100), 100)
            st.markdown(f"**⏱️ Horas:** {h_feito}/{h_prev}h ({pct_h}%)")
            st.progress(pct_h/100)
            st.markdown(f"**❓ Questões:** {q_feito}/{q_prev} ({pct_q}%)")
            st.progress(pct_q/100)
            col_ma, col_mb = st.columns(2)
            with col_ma:
                if st.button("➕ +1h estudada", key="tutorcon5"):
                    st.session_state.horas_semana = h_feito + 1
                    st.session_state.horas_acumuladas = st.session_state.get('horas_acumuladas',0) + 1
                    st.rerun()
            with col_mb:
                if st.button("⚙️ Definir metas", key="def_metas"):
                    st.session_state.pagina = "Progresso"; st.rerun()

        # ÚLTIMAS ATIVIDADES
        if st.session_state.historico_estudos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🕐 Últimas Atividades")
            for item in reversed(st.session_state.historico_estudos[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item.get('materia', '')[:80]}</small></div>", unsafe_allow_html=True)


        # ──────────────────────────────────────────
        # PAINEL EXECUTIVO
        # ──────────────────────────────────────────

    with _tab_Questoes:
        st.header("❓ Simulado de Questões")
        st.markdown("Questões no estilo da banca — com gabarito comentado e explicação detalhada.")

        col1, col2 = st.columns(2)
        with col1:
            materia_q  = st.text_input("Matéria:", placeholder="ex: Português, Matemática, Direito...", key="tutorcon30")
            tema_q     = st.text_input("Tema:", placeholder="ex: Análise Sintática, Regra de Três, CF/88...", key="tutorcon31")
            concurso_q = st.text_input("Estilo de banca:", value=st.session_state.concurso_foco,
                placeholder="ex: CESPE, FCC, Vunesp, ENEM...", key="tutorcon14_d2")
        with col2:
            qtd_q   = st.slider("Quantidade de questões:", 3, 10, 5, key="tutorcon1")
            nivel_q = st.selectbox("Nível de dificuldade:", ["Fácil","Médio","Difícil","Misto"], key="tutorcon32")
            tipo_q  = st.radio("Tipo:", ["Múltipla escolha (A-E)","Certo ou Errado"], horizontal=True, key="tutorcon33")

        if st.button("❓ GERAR SIMULADO", key="tutorcon34"):
            if materia_q.strip():
                with st.spinner("Gerando suas questões..."):
                    estilo = "no estilo CERTO ou ERRADO" if "Certo" in tipo_q else "de múltipla escolha com 5 alternativas (A, B, C, D, E)"
                    prompt = (
                        f"Crie {qtd_q} questões {estilo} sobre '{tema_q or materia_q}' da matéria {materia_q}.\n"
                        f"Banca/estilo: {concurso_q}. Nível: {nivel_q}.\n\n"
                        f"Para CADA questão use EXATAMENTE este formato:\n\n"
                        f"QUESTÃO [N]\n"
                        f"[Enunciado da questão]\n"
                        + ("[A) opção\nB) opção\nC) opção\nD) opção\nE) opção\n" if "múltipla" in tipo_q else "[  ] CERTO  [  ] ERRADO\n")
                        + f"GABARITO: [letra ou CERTO/ERRADO]\n"
                        f"EXPLICAÇÃO: [resolução detalhada — por que o gabarito está certo e por que as outras estão erradas]\n"
                        f"DICA: [macete para não errar esse tipo de questão]\n\n"
                        f"---\n\n"
                        f"REGRAS:\n"
                        f"- Questões realistas, no estilo de provas reais\n"
                        f"- Varie os assuntos dentro do tema\n"
                        f"- Inclua pelo menos 1 pegadinha típica de banca\n"
                        f"- Explicações claras e educativas"
                    )
                    res = tutor_ia(prompt)
                    salvar_estudo("Simulado", f"{materia_q} — {tema_q}", res)
                    st.session_state.questoes_respondidas += qtd_q
                    st.session_state['simulado_temp'] = res
                    st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Preencha a matéria antes de gerar o simulado.")

        if st.session_state.get('simulado_temp'):
            col_acerto, col_dl, col_sv = st.columns(3)
            with col_acerto:
                acertos_input = st.number_input("Quantas você acertou?", min_value=0, max_value=qtd_q if 'qtd_q' in dir() else 10, value=0, key="tutorcon35")
                if st.button("✅ Registrar acertos", key="tutorcon36"):
                    st.session_state.questoes_certas += acertos_input
                    st.success(f"✅ {acertos_input} acertos registrados! Taxa geral: {round(st.session_state.questoes_certas/max(1,st.session_state.questoes_respondidas)*100)}%")
            with col_dl:
                st.download_button("📋 Baixar simulado (.txt)", data=st.session_state['simulado_temp'],
                    file_name="simulado.txt", mime="text/plain", use_container_width=True, key="tutorcon13_d2")
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", key="sv_sim", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo': 'Simulado', 'materia': f"{materia_q} — {tema_q}",
                        'conteudo': st.session_state['simulado_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

        # ========================
        # TÉCNICAS DE MEMORIZAÇÃO
        # ========================

    with _tab_Redacao:
        st.header("✍️ Redação para Concursos")
        _aba_r1, _aba_r2 = st.tabs(["📚 Como Fazer", "⏱️ Prática Cronometrada"])

        with _aba_r1:
            st.markdown("### 📚 Guia de Redação para Concursos")
            _tipo_guia = st.selectbox("Tipo:", ["Dissertativo-argumentativa","Carta argumentativa","Redação administrativa"], key="tc_tipo_guia")
            if st.button("📚 GERAR GUIA", key="tc_btn_guia", use_container_width=True):
                with st.spinner("Gerando guia..."):
                    try:
                        from groq import Groq as _Gr1
                        _r1 = _Gr1(api_key=st.session_state.api_key).chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":f"Crie um guia completo de redação {_tipo_guia} para concursos públicos. Inclua: estrutura, técnicas de argumentação, critérios das bancas, erros comuns e exemplo comentado."}],
                            max_tokens=2500
                        )
                        st.markdown(f"<div class='card'>{_r1.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e1: st.error(f"Erro: {_e1}")

        with _aba_r2:
            import time as _tm

            # ── ETAPA 1: Gerar tema ──
            if not st.session_state.get('red_ativo') and not st.session_state.get('red_entregue'):
                st.markdown("### 🎯 Prática com Tempo Real")
                st.markdown("Clique para receber um tema aleatório de concurso. Você terá **30 minutos** para escrever.")
                _banca = st.selectbox("Banca:", ["CESPE/CEBRASPE","FCC","VUNESP","FGV","Qualquer"], key="tc_banca_red")
                if st.button("🎲 GERAR TEMA E INICIAR", key="tc_iniciar_red", use_container_width=True):
                    with st.spinner("Gerando tema..."):
                        try:
                            from groq import Groq as _Gr2
                            _r2 = _Gr2(api_key=st.session_state.api_key).chat.completions.create(
                                model="openai/gpt-oss-120b",
                                messages=[{"role":"user","content":f"Gere um tema realista de redação para concurso público banca {_banca}. Inclua: TEMA (1 linha), CONTEXTO (2-3 linhas de motivação) e PROPOSTA (o que o candidato deve redigir). Seja direto e objetivo."}],
                                max_tokens=600
                            )
                            st.session_state['red_tema']     = _r2.choices[0].message.content
                            st.session_state['red_inicio']   = _tm.time()
                            st.session_state['red_ativo']    = True
                            st.session_state['red_entregue'] = False
                            st.session_state['red_texto']    = ''
                            st.session_state['red_correcao'] = ''
                            st.rerun()
                        except Exception as _e2: st.error(f"Erro: {_e2}")

            # ── ETAPA 2: Escrever com timer ──
            elif st.session_state.get('red_ativo') and not st.session_state.get('red_entregue'):
                _elapsed  = _tm.time() - st.session_state.get('red_inicio', _tm.time())
                _restante = max(0, 1800 - int(_elapsed))
                _mins     = _restante // 60
                _segs     = _restante % 60
                _cor      = "#22C55E" if _restante > 900 else ("#F59E0B" if _restante > 300 else "#EF4444")

                # Timer grande
                st.markdown(f"<div style='text-align:center;font-size:3em;font-weight:700;color:{_cor};background:#F8F9FA;border-radius:14px;padding:12px;margin-bottom:12px;'>⏱️ {_mins:02d}:{_segs:02d}</div>", unsafe_allow_html=True)

                # Tema
                with st.expander("📋 Ver Tema", expanded=True):
                    st.markdown(st.session_state.get('red_tema',''))

                # Campo de escrita
                _texto = st.text_area(
                    "✍️ Escreva sua redação aqui:",
                    height=350,
                    value=st.session_state.get('red_texto',''),
                    key="tc_texto_red",
                    placeholder="Comece sua redação aqui..."
                )
                st.session_state['red_texto'] = _texto

                _palavras = len(_texto.split()) if _texto.strip() else 0
                st.caption(f"📝 {_palavras} palavras")

                # Encerrou o tempo — entregar automaticamente
                if _restante <= 0:
                    st.session_state['red_ativo']    = False
                    st.session_state['red_entregue'] = True
                    st.warning("⏰ Tempo esgotado! Sua redação foi entregue.")
                    st.rerun()
                else:
                    # Auto-refresh a cada segundo
                    _tm.sleep(1)
                    st.rerun()

            # ── ETAPA 3: Correção e nota ──
            elif st.session_state.get('red_entregue'):
                st.success("✅ Redação entregue!")

                _texto_final = st.session_state.get('red_texto','').strip()
                _tema_final  = st.session_state.get('red_tema','')
                _tempo_usado = int(1800 - max(0, 1800 - int(_tm.time() - st.session_state.get('red_inicio', _tm.time()))))
                _mins_usado  = min(30, _tempo_usado // 60)

                if not st.session_state.get('red_correcao'):
                    with st.spinner("📊 Gerando nota e recomendações..."):
                        try:
                            from groq import Groq as _Gr3
                            _prompt_corr = f"""Você é corretor de redação de concurso público. Corrija a redação abaixo com rigor de banca.

TEMA:
{_tema_final}

REDAÇÃO DO CANDIDATO (tempo usado: {_mins_usado} minutos):
{_texto_final if _texto_final else "[Candidato não escreveu nada ou o tempo esgotou sem texto]"}

Forneça:

📊 NOTA FINAL: __/100

Critérios (0-20 cada):
• Adequação ao tema: __/20
• Estrutura e coesão: __/20
• Qualidade dos argumentos: __/20
• Domínio da norma culta: __/20
• Proposta de intervenção: __/20

✅ PONTOS FORTES (cite 2-3 aspectos positivos)

❌ ERROS ENCONTRADOS (cite trechos exatos e como corrigir)

💡 RECOMENDAÇÕES (3 dicas práticas para a próxima redação)

📈 PARECER FINAL (1 parágrafo motivador e honesto)"""

                            _r3 = _Gr3(api_key=st.session_state.api_key).chat.completions.create(
                                model="openai/gpt-oss-120b",
                                messages=[{"role":"user","content":_prompt_corr}],
                                max_tokens=2000
                            )
                            _corr = _r3.choices[0].message.content
                            st.session_state['red_correcao'] = _corr

                            # Salvar no histórico
                            if 'historico_redacoes' not in st.session_state:
                                st.session_state['historico_redacoes'] = []
                            import datetime as _dt
                            st.session_state['historico_redacoes'].append({
                                'data':     _dt.datetime.now().strftime('%d/%m %H:%M'),
                                'tema':     _tema_final[:80],
                                'texto':    _texto_final[:200],
                                'correcao': _corr,
                                'tempo':    _mins_usado
                            })
                            st.rerun()
                        except Exception as _e3: st.error(f"Erro na correção: {_e3}")
                else:
                    st.markdown(f"<div class='card'>{st.session_state['red_correcao']}</div>", unsafe_allow_html=True)
                    st.download_button("📥 Baixar correção", data=st.session_state['red_correcao'], file_name="correcao_redacao.txt", key="tc_dl_corr")

                st.markdown("---")
                if st.button("🔄 Nova Redação", key="tc_nova_red", use_container_width=True):
                    for _k in ['red_ativo','red_entregue','red_tema','red_inicio','red_texto','red_correcao']:
                        st.session_state.pop(_k, None)
                    st.rerun()

                if st.session_state.get('historico_redacoes'):
                    with st.expander(f"📊 Histórico ({len(st.session_state['historico_redacoes'])} redações)"):
                        for _item in reversed(st.session_state['historico_redacoes'][-5:]):
                            st.markdown(f"**{_item.get('data','')}** — {_item.get('tema','')[:50]}... ({_item.get('tempo',0)}min)")

    with _tab_Simulado:
        st.header("🎯 Simulado — Quiz de Concurso")
        st.markdown("*Questões no estilo de banca, com placar e histórico de acertos.*")

        if 'quiz_banco' not in st.session_state: st.session_state['quiz_banco'] = []
        if 'quiz_idx' not in st.session_state: st.session_state['quiz_idx'] = 0
        if 'quiz_acertos' not in st.session_state: st.session_state['quiz_acertos'] = 0
        if 'quiz_erros' not in st.session_state: st.session_state['quiz_erros'] = []
        if 'quiz_respondida' not in st.session_state: st.session_state['quiz_respondida'] = False
        if 'quiz_resposta_atual' not in st.session_state: st.session_state['quiz_resposta_atual'] = None
        if 'historico_simulados' not in st.session_state: st.session_state['historico_simulados'] = []

        _tab_quiz1, _tab_quiz2 = st.tabs(["🎯 Simulado", "📊 Meu Desempenho"])

        with _tab_quiz1:
            if not st.session_state['quiz_banco']:
                # Configurar simulado
                _col1, _col2 = st.columns(2)
                with _col1:
                    _mat_quiz = st.text_input("Matéria:", placeholder="ex: Português, Direito Constitucional...", key="tc_quiz_mat")
                    _banca_quiz = st.selectbox("Banca:", ["CESPE/CEBRASPE","FCC","VUNESP","FGV","IBFC","Qualquer"], key="tc_quiz_banca")
                with _col2:
                    _qtd_quiz = st.selectbox("Quantidade de questões:", [5, 10, 15, 20], index=1, key="tc_quiz_qtd")
                    _nivel_quiz = st.selectbox("Nível:", ["Fácil","Médio","Difícil","Misto"], index=1, key="tc_quiz_nivel")

                if st.button("🚀 INICIAR SIMULADO", key="tc_quiz_iniciar", use_container_width=True):
                    if _mat_quiz.strip():
                        with st.spinner(f"Gerando {_qtd_quiz} questões de {_mat_quiz}..."):
                            try:
                                from groq import Groq as _GrQ
                                _cli = _GrQ(api_key=st.session_state.api_key)
                                _r = _cli.chat.completions.create(
                                    model="openai/gpt-oss-120b",
                                    messages=[{"role":"user","content":f"""Gere exatamente {_qtd_quiz} questões de {_mat_quiz} no estilo {_banca_quiz}, nível {_nivel_quiz}.

Responda APENAS em JSON válido, sem texto extra:
{{"questoes": [{{"enunciado": "texto da questão", "alternativas": {{"A": "texto A", "B": "texto B", "C": "texto C", "D": "texto D", "E": "texto E"}}, "gabarito": "A", "explicacao": "Por que A está correta..."}}]}}"""}],
                                    max_tokens=4000
                                )
                                import json as _json
                                _raw = _r.choices[0].message.content
                                _s = _raw.find('{'); _e = _raw.rfind('}')
                                _dados = _json.loads(_raw[_s:_e+1])
                                st.session_state['quiz_banco'] = _dados['questoes']
                                st.session_state['quiz_idx'] = 0
                                st.session_state['quiz_acertos'] = 0
                                st.session_state['quiz_erros'] = []
                                st.session_state['quiz_respondida'] = False
                                st.session_state['quiz_resposta_atual'] = None
                                st.rerun()
                            except Exception as _e2:
                                st.error(f"Erro ao gerar questões: {_e2}")
                    else:
                        st.warning("Informe a matéria.")
            else:
                _banco = st.session_state['quiz_banco']
                _idx = st.session_state['quiz_idx']
                _total = len(_banco)

                if _idx >= _total:
                    # Resultado final
                    _acertos = st.session_state['quiz_acertos']
                    _pct = round(_acertos/_total*100)
                    _cor = "#22C55E" if _pct >= 70 else ("#F59E0B" if _pct >= 50 else "#EF4444")
                    st.markdown(f"<h2 style='text-align:center;color:{_cor};'>✅ Simulado Concluído!</h2>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='text-align:center;font-size:3em;color:{_cor};'>{_acertos}/{_total} — {_pct}%</h1>", unsafe_allow_html=True)

                    _c1,_c2,_c3 = st.columns(3)
                    _c1.metric("✅ Acertos", _acertos)
                    _c2.metric("❌ Erros", _total-_acertos)
                    _c3.metric("📊 Aproveitamento", f"{_pct}%")

                    if st.session_state['quiz_erros']:
                        st.markdown("### ❌ Questões que você errou — Revise:")
                        for _err in st.session_state['quiz_erros']:
                            with st.expander(f"Q{_err['num']}: {_err['enunciado'][:60]}..."):
                                st.markdown(f"**Sua resposta:** {_err['sua']} — **Gabarito:** {_err['gabarito']}")
                                st.markdown(f"**Explicação:** {_err['explicacao']}")

                    # Salvar no histórico
                    import datetime as _dt
                    st.session_state['historico_simulados'].append({
                        'data': _dt.datetime.now().strftime('%d/%m %H:%M'),
                        'acertos': _acertos,
                        'total': _total,
                        'pct': _pct
                    })

                    if st.button("🔄 Novo Simulado", key="tc_quiz_novo_final", use_container_width=True):
                        st.session_state['quiz_banco'] = []
                        st.rerun()
                else:
                    # Questão atual
                    _q = _banco[_idx]
                    st.markdown(f"**Questão {_idx+1} de {_total}** | ✅ {st.session_state['quiz_acertos']} acertos")

                    # Barra de progresso
                    st.progress(_idx/_total)

                    st.markdown(f"<div class='card'>{_q.get('enunciado','')}</div>", unsafe_allow_html=True)

                    _alts = _q.get('alternativas', {})
                    _gabarito = _q.get('gabarito','A')

                    if not st.session_state['quiz_respondida']:
                        for _letra, _texto in _alts.items():
                            if st.button(f"{_letra}) {_texto}", key=f"tc_quiz_alt_{_idx}_{_letra}", use_container_width=True):
                                st.session_state['quiz_resposta_atual'] = _letra
                                st.session_state['quiz_respondida'] = True
                                if _letra == _gabarito:
                                    st.session_state['quiz_acertos'] += 1
                                else:
                                    st.session_state['quiz_erros'].append({
                                        'num': _idx+1,
                                        'enunciado': _q.get('enunciado',''),
                                        'sua': _letra,
                                        'gabarito': _gabarito,
                                        'explicacao': _q.get('explicacao','')
                                    })
                                st.rerun()
                    else:
                        _resp = st.session_state['quiz_resposta_atual']
                        for _letra, _texto in _alts.items():
                            if _letra == _gabarito:
                                st.success(f"✅ {_letra}) {_texto}")
                            elif _letra == _resp and _resp != _gabarito:
                                st.error(f"❌ {_letra}) {_texto} ← sua resposta")
                            else:
                                st.markdown(f"&nbsp;&nbsp;{_letra}) {_texto}")

                        st.markdown(f"**💡 Explicação:** {_q.get('explicacao','')}")

                        if st.button("➡️ PRÓXIMA QUESTÃO" if _idx+1 < _total else "🏁 VER RESULTADO", key=f"tc_quiz_prox_{_idx}", use_container_width=True):
                            st.session_state['quiz_idx'] += 1
                            st.session_state['quiz_respondida'] = False
                            st.session_state['quiz_resposta_atual'] = None
                            st.rerun()

        with _tab_quiz2:
            st.markdown("### 📊 Meu Histórico de Simulados")
            if st.session_state['historico_simulados']:
                for i, _item in enumerate(reversed(st.session_state['historico_simulados'][-10:])):
                    _pct2 = _item.get('pct',0)
                    _cor2 = "#22C55E" if _pct2>=70 else ("#F59E0B" if _pct2>=50 else "#EF4444")
                    st.markdown(f"<div class='hist-item'><b>{_item.get('data','')}</b> — {_item.get('acertos',0)}/{_item.get('total',0)} questões — <span style='color:{_cor2};font-weight:700;'>{_pct2}%</span></div>", unsafe_allow_html=True)

                _total_sim = len(st.session_state['historico_simulados'])
                _media_pct = sum(s.get('pct',0) for s in st.session_state['historico_simulados']) / _total_sim
                st.markdown(f"**📈 Média geral:** {_media_pct:.0f}% em {_total_sim} simulados")
            else:
                st.info("Faça seu primeiro simulado para ver o histórico aqui.")

    with _tab_Cronograma:
        st.header("📅 Cronograma de Estudos")
        st.markdown("*Monte seu cronograma personalizado para o concurso.*")
        _prompt_cronograma = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_cronograma_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_cronograma_btn", use_container_width=True):
            if _prompt_cronograma.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_cronograma}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Flashcards:
        st.header("🃏 Flashcards Inteligentes")
        st.markdown("*Estude com flashcards gerados pela IA.*")
        _prompt_flashcards = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_flashcards_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_flashcards_btn", use_container_width=True):
            if _prompt_flashcards.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_flashcards}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Progresso:
        st.header("📈 Meu Progresso de Estudos")

        total       = len(st.session_state.historico_estudos)
        bib         = len(st.session_state.biblioteca_materiais)
        respondidas = st.session_state.questoes_respondidas
        certas      = st.session_state.questoes_certas
        taxa        = round(certas / respondidas * 100) if respondidas > 0 else 0
        tipos = {}
        for e in st.session_state.historico_estudos:
            tipos[e['tipo']] = tipos.get(e['tipo'], 0) + 1

        # Cor da taxa de acerto
        cor_taxa = "#059669" if taxa >= 70 else ("#B45309" if taxa >= 50 else "#B91C1C")
        msg_taxa = "🟢 Ótimo!" if taxa >= 70 else ("🟡 Melhorando..." if taxa >= 50 else "🔴 Precisa praticar mais")

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Materiais gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{respondidas}</div><div>Questões feitas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero' style='color:{cor_taxa} !important;'>{taxa}%</div><div>Taxa de acerto {msg_taxa}</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Resumo',0)}</div><div>Resumos</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{bib}</div><div>Na biblioteca</div></div>", unsafe_allow_html=True)

        # Ajuste manual de questões
        with st.expander("✏️ Ajustar contagem de questões"):
            col_r, col_c = st.columns(2)
            with col_r:
                nova_r = st.number_input("Total de questões respondidas:", min_value=0, value=respondidas, key="tutorcon46")
            with col_c:
                nova_c = st.number_input("Total de acertos:", min_value=0, max_value=nova_r, value=min(certas, nova_r), key="tutorcon47")
            if st.button("Salvar contagem", key="tutorcon48"):
                st.session_state.questoes_respondidas = nova_r
                st.session_state.questoes_certas      = nova_c
                st.success("✅ Contagem atualizada!")
                st.rerun()

        if st.session_state.historico_estudos:
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro = st.selectbox("Filtrar:", ["Todos"] + list(tipos.keys()), key="tutorcon49")
            with col_ex:
                historico_txt = "\n\n".join(
                    f"[{e['data']}] {e['tipo']} — {e['materia']}\n{e['conteudo']}\n{'─'*40}"
                    for e in st.session_state.historico_estudos
                )
                st.download_button("⬇️ Exportar TXT", data=historico_txt,
                    file_name="historico_estudos.txt", mime="text/plain", key="tutorcon6_d2")

            for i, item in enumerate(reversed(st.session_state.historico_estudos)):
                if filtro != "Todos" and item['tipo'] != filtro:
                    continue
                idx_real = len(st.session_state.historico_estudos) - 1 - i
                with st.expander(f"[{item['tipo']}] {item.get('materia', '')} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_sv, col_del = st.columns([3, 1])
                    with col_sv:
                        if st.button("💾 Salvar na Biblioteca", key=f"sv_hist_{i}"):
                            st.session_state.biblioteca_materiais.append(item.copy())
                            st.success("Salvo!")
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}"):
                            st.session_state.historico_estudos.pop(idx_real)
                            st.rerun()

            if st.button("🗑️ Limpar Todo o Histórico", key="tutorcon50"):
                st.session_state.historico_estudos = []
                st.rerun()
        else:
            st.info("Nenhum material gerado ainda. Comece pelo Plano de Estudos!")


        # ──────────────────────────────────────────
        # SIMULADO INTELIGENTE
        # ──────────────────────────────────────────

    with _tab_Legislacao:
        st.header("⚖️ Legislação")
        st.markdown("*Estude a legislação específica do seu concurso.*")
        _prompt_legislacao = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_legislacao_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_legislacao_btn", use_container_width=True):
            if _prompt_legislacao.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_legislacao}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Informatica:
        st.header("💻 Informática")
        st.markdown("*Questões e teoria de informática para concursos.*")
        _prompt_informatica = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_informatica_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_informatica_btn", use_container_width=True):
            if _prompt_informatica.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_informatica}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Portugues:
        st.header("📖 Português")
        st.markdown("*Gramática, interpretação e redação em português.*")
        _prompt_portugues = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_portugues_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_portugues_btn", use_container_width=True):
            if _prompt_portugues.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_portugues}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Matematica:
        st.header("🔢 Matemática/Raciocínio")
        st.markdown("*Matemática e raciocínio lógico para concursos.*")
        _prompt_matematica = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_matematica_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_matematica_btn", use_container_width=True):
            if _prompt_matematica.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_matematica}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Atualidades:
        pass

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Tutor de Concursos IA — Mentor Estratégico · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
