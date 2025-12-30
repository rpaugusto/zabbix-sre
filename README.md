# Zabbix SRE

Aplicação em **Python + Flask** para integração com **Zabbix**, fornecendo funcionalidades para monitoramento e automação voltadas para equipes de SRE.

---

## ✅ Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/) (para rodar localmente)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 📦 Instalação e execução

### **1. Clonar o repositório**
```bash
git clone https://github.com/rpaugusto/zabbix-sre.git
cd zabbix-sre
```

### **2. Configurar variáveis de ambiente**
Copie o arquivo de exemplo e edite conforme necessário:
```bash
cp .env.exemple .env
```

Exemplo de variáveis:
```
ZABBIX_URL=https://seu-zabbix
ZABBIX_USER=usuario
ZABBIX_PASSWORD=senha
PORT=5000
```

---

## 🚀 Executando com Docker Compose (recomendado)
```bash
docker compose up -d --build
```

Acesse em:  
```
http://localhost:5000
```

---

## 🐳 Executando com Docker (manual)
```bash
docker build -t zabbix-sre:latest .
docker run -d --name zabbix-sre   --env-file .env   -p 5000:5000   zabbix-sre:latest
```

---

## 🔍 Estrutura do projeto
```
zabbix-sre/
├─ app.py
├─ config.py
├─ .env
├─ requirements.txt
├─ helpers.py
├─ routes.py
├─ controllers/
│  ├─ home_controller.py
│  ├─ zabbix_controller.py
│  ├─ config_controller.py
│  ├─ hosts_controller.py
│  ├─ templates_controller.py
│  ├─ groups_controller.py
│  └─ items_controller.py
├─ services/
│  ├─ zabbix_service.py        # cliente JSON-RPC (chamada bruta)
│  ├─ service_hosts.py         # lógica/transformação de hosts
│  ├─ service_templates.py     # lógica/transformação de templates
│  ├─ service_groups.py        # lógica/transformação de grupos
│  └─ service_items.py         # lógica/transformação de items (ex.: agents)
├─ templates/
│  ├─ base.html
│  ├─ home.html
│  ├─ hosts.html
│  ├─ templates_page.html
│  ├─ groups.html
│  ├─ routes.html
│  ├─ env.html
│  ├─ health.html
│  └─ config.html
└─ static/
   └─ css/styles.css
```

---

## 🤝 Contribuindo
1. Faça um fork do projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit suas alterações: `git commit -m 'Minha feature'`
4. Push: `git push origin minha-feature`
5. Abra um Pull Request

---

## 📄 Licença
Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
