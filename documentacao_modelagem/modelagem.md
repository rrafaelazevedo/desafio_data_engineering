# Modelagem Entidade-Relacionamento (E-R)

## **Descrição de Entidades e Relacionamentos (ER)**

---

### **empresas**

* **Chave primária (PK):** `id_empresa`
* **Atributos:** `id_empresa`, `nome_fantasia`, `cnpj`, `data_fundacao`
* **Relacionamentos:**
  * `receitas.id_empresa` → uma empresa pode ter várias receitas → **1:N**
  * `despesas.id_empresa` → uma empresa pode ter várias despesas → **1:N**
  * `orcamentos.id_empresa` → uma empresa pode ter vários orçamentos → **1:N**
  * `transferencias.id_empresa_origem` → uma empresa pode ser origem de várias transferências → **1:N**
  * `transferencias.id_empresa_destino` → uma empresa pode ser destino de várias transferências → **1:N**

---

### **clientes**

* **Chave primária (PK):** `id_cliente`
* **Atributos:** `id_cliente`, `nome`, `email`, `cpf`
* **Relacionamentos:**
  * `receitas.id_cliente` → um cliente pode estar associado a várias receitas → **1:N**
  * `despesas.id_cliente` → um cliente pode estar associado a várias despesas → **1:N**

---

### **receitas**

* **Chave primária (PK):** `id_receita`
* **Chaves estrangeiras (FKs):**
  * `id_empresa` → **empresas(id_empresa)**
  * `id_cliente` → **clientes(id_cliente)** *(opcional)*
* **Atributos:** `id_receita`, `id_empresa`, `id_cliente`, `categoria`, `valor`, `data`, `descricao`
* **Relacionamentos:**
  * `id_empresa` → uma receita pertence a uma empresa → **N:1**
  * `id_cliente` → uma receita pode estar vinculada a um cliente → **N:1 (opcional)**

---

### **despesas**

* **Chave primária (PK):** `id_despesa`
* **Chaves estrangeiras (FKs):**
  * `id_empresa` → **empresas(id_empresa)**
  * `id_cliente` → **clientes(id_cliente)** *(opcional)*
* **Atributos:** `id_despesa`, `id_empresa`, `id_cliente`, `categoria`, `valor`, `data`, `descricao`
* **Relacionamentos:**
  * `id_empresa` → uma despesa pertence a uma empresa → **N:1**
  * `id_cliente` → uma despesa pode estar vinculada a um cliente → **N:1 (opcional)**

---

### **orcamentos**

* **Chave primária (PK):** `id_orcamento`
* **Chave estrangeira (FK):**
  * `id_empresa` → **empresas(id_empresa)**
* **Atributos:** `id_orcamento`, `id_empresa`, `ano`, `mes`, `tipo`, `valor_estimado`
* **Relacionamentos:**
  * `id_empresa` → um orçamento pertence a uma empresa → **N:1**

---

### **transferencias**

* **Chave primária (PK):** `id_transferencia`
* **Chaves estrangeiras (FKs):**
  * `id_empresa_origem` → **empresas(id_empresa)**
  * `id_empresa_destino` → **empresas(id_empresa)**
* **Atributos:** `id_transferencia`, `id_empresa_origem`, `id_empresa_destino`, `tipo`, `valor`, `data`, `descricao`
* **Relacionamentos:**
  * `id_empresa_origem` → uma transferência tem uma empresa de origem → **N:1**
  * `id_empresa_destino` → uma transferência tem uma empresa de destino → **N:1**

---

![Diagrama Entidade-Relacionamento](diagrama_mer.JPG)
