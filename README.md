# Astrologer API - Solução 100% Open Source

Uma API de astrologia de código aberto que fornece cálculos extensos de astrologia, projetada para integração perfeita em projetos. Oferece um conjunto rico de gráficos e dados astrológicos, tornando-se uma ferramenta valiosa para desenvolvedores e entusiastas de astrologia.

**🎉 Migrada do RAPIDAPI para solução totalmente open-source!**

## 🚀 Recursos

- ✨ Cálculos astrológicos precisos usando a biblioteca Kerykeion
- 📊 Geração de gráficos natais, de sinastria, trânsito e compostos
- 🗺️ Integração com Geonames (open-source) para dados geográficos
- 🇧🇷 Otimizações específicas para o público brasileiro
- 🌍 Suporte multilíngue
- 📐 Geração de gráficos SVG com múltiplos temas
- 🔄 Sistema de rotação de credenciais
- ⚡ Rate limiting inteligente
- 📖 Documentação em português e inglês

## 📋 Pré-requisitos

- Python 3.11+
- Conta gratuita no Geonames (https://www.geonames.org/login/)

## 🔧 Instalação Local

### 1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/astrologer-api.git
cd astrologer-api
```

### 2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências:
```bash
pip install pipenv
pipenv install
```

### 4. Configure as variáveis de ambiente:

Crie um arquivo `.env` na raiz do projeto:

```bash
# Obrigatório
GEONAMES_USERNAME=seu_usuario_geonames

# Opcional
ENV_TYPE=dev  # ou 'production'
LOG_LEVEL=10  # 10=DEBUG, 20=INFO, 30=WARNING
```

### 5. Execute a aplicação:
```bash
# Modo desenvolvimento
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Acesse: http://localhost:8000/docs
```

## ☁️ Deploy na Vercel

### Deploy com um clique:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/seu-usuario/astrologer-api)

### Deploy manual:

1. **Instale a CLI da Vercel:**
```bash
npm i -g vercel
```

2. **Faça login:**
```bash
vercel login
```

3. **Deploy:**
```bash
vercel
```

4. **Configure as variáveis de ambiente na Vercel:**
   - Acesse seu projeto no dashboard da Vercel
   - Vá em Settings → Environment Variables
   - Adicione:
     - `GEONAMES_USERNAME`: seu username do Geonames
     - `ENV_TYPE`: `production`

5. **Deploy para produção:**
```bash
vercel --prod
```

### Configuração do Geonames (Gratuito)

1. Crie uma conta em: https://www.geonames.org/login/
2. Ative sua conta via email
3. Ative os serviços web em: https://www.geonames.org/manageaccount
4. Use seu username nas variáveis de ambiente

**Limites gratuitos do Geonames:**
- 20.000 créditos/dia
- 1.000 créditos/hora
- 30 requests/segundo

## 🌍 Configurações para o Público Brasileiro

- ✅ Nomes de cidades em português
- ✅ Fuso horário padrão do Brasil (BRT/BRST)
- ✅ Dados otimizados para localidades brasileiras
- ✅ Endpoint dedicado: `/api/v4/geonames/brazilian-search`
- ✅ Documentação em português

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI (Interativa):** http://localhost:8000/docs
- **ReDoc (Documentação):** http://localhost:8000/redoc

### Endpoints Principais:

#### Saúde e Status
- `GET /` - Status da API
- `GET /api/v4/health` - Health check
- `GET /api/v4/now` - Dados astrológicos atuais

#### Gráficos Natais
- `POST /api/v4/birth-data` - Dados natais (sem gráfico)
- `POST /api/v4/birth-chart` - Gráfico natal com SVG
- `POST /api/v4/natal-aspects-data` - Aspectos natais

#### Sinastria (Compatibilidade)
- `POST /api/v4/synastry-chart` - Gráfico de sinastria com SVG
- `POST /api/v4/synastry-aspects-data` - Aspectos de sinastria
- `POST /api/v4/relationship-score` - Pontuação de compatibilidade

#### Trânsitos
- `POST /api/v4/transit-chart` - Gráfico de trânsitos com SVG
- `POST /api/v4/transit-aspects-data` - Aspectos de trânsitos

#### Compósito
- `POST /api/v4/composite-chart` - Gráfico composto com SVG
- `POST /api/v4/composite-aspects-data` - Aspectos compostos

#### Geonames (Dados Geográficos)
- `GET /api/v4/geonames/status` - Status do serviço
- `GET /api/v4/geonames/search` - Busca de locais
- `GET /api/v4/geonames/timezone` - Fuso horário
- `GET /api/v4/geonames/brazilian-search` - Busca em português (Brasil)
- `GET /api/v4/geonames/country-info` - Informações de países

## 🔐 Gestão de Credenciais

O sistema inclui gerenciamento inteligente de credenciais do Geonames:

- ✅ Rotação automática de credenciais
- ✅ Monitoramento de uso
- ✅ Validação de credenciais
- ✅ Proteção contra exceder limites

## 📊 Limites de Taxa

Para garantir disponibilidade contínua:

- **Geonames:** 2000 requests/minuto, 10000 requests/hora
- **Configurável** via rate limiter personalizado

## 🛠️ Tecnologias Utilizadas

### 100% Open-Source:
- **FastAPI** - Framework web moderno
- **Kerykeion** - Biblioteca de cálculos astrológicos
- **Geonames API** - Dados geográficos (free tier)
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validação de dados
- **pytz** - Gerenciamento de fusos horários

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a **AGPL-3.0** - veja o arquivo [LICENSE](https://www.gnu.org/licenses/agpl-3.0.html) para detalhes.

## 📞 Contato

- **Nome:** Kerykeion Astrology
- **Email:** kerykeion.astrology@gmail.com
- **Site:** https://www.kerykeion.net/
- **GitHub:** https://github.com/g-battaglia/Astrologer-API

## 🎯 Migração do RAPIDAPI

Esta API foi migrada do RAPIDAPI para uma solução 100% open-source:

### ✅ O que foi removido:
- Middleware de autenticação RAPIDAPI
- IPs whitelisted do RAPIDAPI
- Dependências do header `X-RapidAPI-Proxy-Secret`
- Configurações proprietárias

### ✅ O que foi adicionado:
- Deploy direto na Vercel
- Configuração simplificada
- Documentação completa de deployment
- Sem custos de marketplace

### 🚀 Vantagens da Migração:
- **100% Open-Source** - sem dependências proprietárias
- **Deploy Gratuito** - Vercel free tier + Geonames free tier
- **Controle Total** - você hospeda onde quiser
- **Sem Intermediários** - acesso direto à API
- **Documentação Completa** - em português e inglês

## 🌟 Suporte

Se você gostou deste projeto, considere:
- ⭐ Dar uma estrela no GitHub
- 🐛 Reportar bugs e sugerir melhorias
- 📖 Contribuir com documentação
- 💬 Compartilhar com outros desenvolvedores

---

**Desenvolvido com ❤️ pela comunidade open-source**
