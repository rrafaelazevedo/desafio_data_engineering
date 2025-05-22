# Modelagem Entidade-Relacionamento (E-R)

Este documento descreve as principais entidades e seus relacionamentos no banco de dados criado a partir dos arquivos CSV.

## Tabelas principais

- **empresas**: contém CNPJ, nome empresarial, natureza jurídica, etc.
- **socios**: lista os sócios por empresa, com qualificações e tipo de pessoa.
- **cnaes**: cadastro nacional de atividades econômicas (códigos e descrições).
- **empresas_cnaes**: relacionamento N:N entre empresas e atividades secundárias.
- **municipios**: municípios normalizados por código IBGE.
- **ufs**: unidades federativas (estados).
- **naturezas_juridicas**: tipos jurídicos de empresas.
- **qualificacoes**: classificações de papel do sócio (ex: administrador, titular).

## Diagrama

![Diagrama Entidade-Relacionamento](diagrama_mer.JPG)
