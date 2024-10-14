<template>
  <div>
    <h1>Arquivos CSV disponíveis</h1>
    <table class="tabela-arquivos">
      <thead>
        <tr>
          <th>Nome do Arquivo</th>
          <th>URL</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="arquivo in lista_de_arquivos" :key="arquivo.nome">
          <td>{{ arquivo.nome }}</td>
          <td>
            <a :href="arquivo.url" target="_blank" rel="noopener noreferrer">
              {{ arquivo.url }}
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    data() {
      return {
        lista_de_arquivos: []
      };
    },
    created() {
      this.recuperar_arquivos();
    },
    methods: {
      async recuperar_arquivos() {
        try {
          const response = await axios.get('http://localhost:8000/ListaDeCSVs');
          this.lista_de_arquivos = response.data.lista_de_arquivos;
        } catch (error) {
          console.error('Erro ao recuperar arquivos:', error);
        }
      }
    }
  };
</script>

<style scoped>
.tabela-arquivos {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 18px;
}

.tabela-arquivos th, .tabela-arquivos td {
  padding: 12px 15px;
  border: 1px solid #ddd;
  text-align: left;
}

.tabela-arquivos th {
  background-color: #f2f2f2;
}

.tabela-arquivos tr:nth-child(even) {
  background-color: #f9f9f9;
}

.tabela-arquivos tr:hover {
  background-color: #f1f1f1;
}
</style>
