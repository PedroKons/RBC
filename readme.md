# Sistema RBC - Diagnóstico de Covid ou Dengue

Este é um sistema de Raciocínio Baseado em Casos (RBC) desenvolvido para auxiliar no diagnóstico diferencial entre Covid-19 e Dengue, utilizando uma interface web interativa construída com Streamlit.

## Sobre o Projeto

O sistema utiliza um algoritmo de similaridade para comparar casos novos com uma base de dados de casos conhecidos. O diagnóstico é baseado em diversos sintomas e características, incluindo:

- Temperatura corporal
- Fadiga
- Tipo de tosse
- Dor no corpo
- Náusea/Vômito
- Tipo de dor de cabeça
- Idade
- Perda de paladar/Olfato

O sistema calcula a similaridade entre o caso atual e os casos na base de dados, apresentando um ranking dos casos mais similares.

## Requisitos

Para executar o projeto, você precisará ter instalado:

- Python 3.7 ou superior
- Streamlit
- Pandas
- NumPy

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências necessárias:

```bash
pip install streamlit pandas numpy
```

## Como Executar

LINK Demo : https://rbc-ia-pedro-kons.streamlit.app/

1. Certifique-se de que o arquivo `database.csv` está presente no mesmo diretório do `app.py`
2. Abra o terminal na pasta do projeto
3. Execute o comando:

```bash
streamlit run app.py
```

4. O navegador será aberto automaticamente com a aplicação (geralmente em http://localhost:8501)

## Como Usar

1. Na seção "Configuração de Pesos", ajuste a importância de cada sintoma usando os sliders (1-5)
2. Na seção "Informações do Caso de Entrada", preencha os dados do paciente:
   - Temperatura corporal (35.0°C - 42.0°C)
   - Fadiga (Leve, Moderada, Intensa)
   - Tipo de tosse (Seca, Com Catarro, Ausente)
   - Dor no corpo (Leve, Moderada, Forte)
   - Náusea/Vômito (Sim, Não)
   - Tipo de dor de cabeça (Frontal, Generalizada, Nenhuma)
   - Idade (0-120 anos)
   - Perda de paladar/Olfato (Sim, Não)
3. Clique em "Calcular Similaridade" para ver os resultados
4. Os casos mais similares serão exibidos em ordem decrescente de similaridade
5. Você pode baixar os resultados em formato CSV clicando no botão "Baixar Resultado em CSV"

## Estrutura do Projeto

- `app.py`: Código principal da aplicação
- `database.csv`: Base de dados com casos conhecidos

## Funcionalidades

- Interface interativa para entrada de dados
- Cálculo de similaridade baseado em diferentes tipos de atributos
- Ranking de casos similares
- Exportação de resultados em CSV
- Configuração personalizada de pesos para cada sintoma

## Observações

- O sistema utiliza diferentes funções de similaridade para diferentes tipos de dados (numéricos, ordinais, binários)
- Os resultados são apresentados em porcentagem de similaridade
- A base de dados pode ser atualizada adicionando novos casos ao arquivo `database.csv`
