# Astrologer API - Solução Open Source

Uma API de astrologia de código aberto que fornece cálculos extensos de astrologia, projetada para integração perfeita em projetos. Oferece um conjunto rico de gráficos e dados astrológicos, tornando-se uma ferramenta valiosa para desenvolvedores e entusiastas de astrologia.

## 🚀 Recursos

- Cálculos astrológicos precisos
- Geração de gráficos natais, de sinastria e de trânsito
- Integração com Geonames para dados geográficos
- Otimizações específicas para o público brasileiro
- Documentação em português

## 📋 Pré-requisitos

- Python 3.11+
- Conta gratuita no Geonames (https://www.geonames.org/login/)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/astrologer-api.git
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install pipenv
pipenv install
```

4. Configure as variáveis de ambiente:
```bash
export GEONAMES_USERNAME="seu_usuario_geonames"
```

## 🌍 Configurações para o Público Brasileiro

- Nomes de cidades em português
- Fuso horário padrão do Brasil (BRT/BRST)
- Dados otimizados para localidades brasileiras
- Documentação em português

## 🔐 Gestão de Credenciais

- Sistema seguro de gerenciamento de chaves Geonames
- Rotação automática de credenciais
- Monitoramento de uso para evitar exceder limites

## 📊 Limites de Taxa

Para garantir disponibilidade contínua e evitar exceder os limites da API Geonames:
- 2000 solicitações por minuto
- 10000 solicitações por hora

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- Nome: Kerykeion Astrology
- Email: kerykeion.astrology@gmail.com
- Site: https://www.kerykeion.net/