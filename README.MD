# Elasticsearch

## Production Deploy

- Vim .env

```bash
COMPOSE_PROJECT_NAME=es
CERTS_DIR=/usr/share/elasticsearch/config/certificates
VERSION=7.17.9
ELASTIC_PASSWORD=hi1234es
KIBANA_PASSWORD=hi1234es

```

- Generate certificate once

```bash
$ docker-compose -f certificates/create-certs.yml run --rm create_certs
```

- Deploy
  - IF LINUX
    ```bash
    $ sudo sysctl -w vm.max_map_count=262144
    ```
  ```bash
  $ docker-compose up -d
  $ chmod 775 data0*
  ```
- Check if ES is healthy

```bash
$ curl -u elastic:hi1234es http://localhost:52200
```

- Check if the connection

```bash
GET http://0.0.0.0:52200//_cat/nodes?v=true&pretty
```
