zabbix_helper_flask/
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